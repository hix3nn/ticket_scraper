from typing import TextIO

from bs4 import BeautifulSoup
from selenium import webdriver
import csv

#Variáveis Globais
num_adults = 2
year = 19
month_list = {'Janeiro':'01','Fevereiro':'02','Março':'03','Abril':'04','Maio':'05','Junho':'06','Julho':'07','Agosto':'08','Setemebro':'09','Outubro':'10','Novembro':'11','Dezembro':'12',}
tax = 440

#
print('===== Ticket Searcher ====')
#arp_1=input('Digite o Aeroporto de Saida: ')
#arp_2=input('Digite o Aeroporto de Chegada: ')
m1_input=input(" - Digite o nome do mês inicial: ")
m2_input=input(" - Digite o nome do mês final: ")
month_1 = month_list[m1_input]
month_2 = month_list[m2_input]


csv_file= open('tickets.csv', "a", newline='')
csv_writer=csv.writer(csv_file)
csv_writer.writerow(['Ano','Mês ida','Dia Ida','Preço Ida','Mês Volta','Dia Volta','Preço Volta','Total'])

def get_source_code(day_1):
    if (int(day_1) <= 9):
        day_1='0'+str(day_1)

    url = ('https://www.skyscanner.com.br/transporte/voos/gig/mad/?adults=' + str(
        num_adults) + '&cabinclass=economy&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home&oym=' + str(
        year) + str(month_1) + '&selectedoday=' +str(day_1) + '&iym=' + str(year) + str(
        month_2) + '&selectediday='+str(day_1)+'&locale=pt-BR&currency=BRL&market=BR')

    driver = webdriver.Chrome()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html5lib')
    driver.quit()
    return soup


def get_outbound(day_1): #ida , driver.get
    soup = get_source_code(day_1)
    ida = soup.find('div', class_="month-view-calendar outbound-calendar")
    for each_day in ida.find_all('td', class_='bpk-calendar-grid__date-3CZvx'):
        if 'R$' in each_day.find('div', class_='price').text:
            day_outbound = each_day.find('div', class_='date').text
            price_outbound = each_day.find('div', class_='price').text
            print('===========')
            print('Dia Ida: ' + day_outbound)
            print('Preço: ' + price_outbound)
            get_inbound(each_day.find('div', class_='date').text,price_outbound)

def get_inbound(day_outbound,price_outbound): #volta

    source_code = get_source_code(day_outbound)
    volta = source_code.find('div', class_='month-view-calendar inbound-calendar')
    for each_day_2 in volta.find_all('td', class_='bpk-calendar-grid__date-3CZvx'):
        if 'R$' in each_day_2.find('div', class_='price').text:
            day_inbound = each_day_2.find('div', class_='date').text
            price_inbound = each_day_2.find('div', class_='price').text
            print('\n' + 'Dia Volta: ' + day_inbound)
            print('Preço: ' + price_inbound)
            total= (int(price_inbound.replace('R$ ','').replace('.','')) + int(price_outbound.replace('R$ ','').replace('.','')) + tax)

            csv_writer.writerow([str(year), str(month_1), str(day_outbound), str(price_outbound),str(month_2), str(price_inbound), str(price_inbound),str("R$ "+total)])
    print('===========')

def Main():
    get_outbound(1)

    csv_file.close
Main()
