import os.path
import re

from bs4 import BeautifulSoup
import requests
import pandas as pd

name_broker = []
urls = []
for_broker = []
against_broker = []
status = []
type_company = []
regulation = []
leverage = []
account = []
advisor = []

info = []
account_1 = []

path = r'./info'
if not os.path.exists(path):
    os.mkdir(r'./info')


class Parser:
    def __init__(self):
        self.name_broker = name_broker
        self.urls = urls
        self.for_broker = for_broker
        self.against_broker = against_broker
        self.status = status
        self.type_company = type_company
        self.regulation = regulation
        self.leverage = leverage
        self.account = account
        self.advisor = advisor
        self.dellist = info
        self.account_1 = account_1

        self._get_html()

    def _get_html(self):
        url = 'https://www.forex-ratings.com/'

        response = requests.get(url=url)

        try:
            assert response.status_code == 200
            html_source = response.text
            self._get_info(html_source)
        except AssertionError as e:
            print(f'ERROR: {repr(e)}')
            print(response.status_code)

    def _get_info(self, html_source):
        pages_info = BeautifulSoup(html_source, 'html.parser')

        names_broker_and_url = pages_info.find_all('a', class_='rating-link')
        for name in names_broker_and_url:
            self.name_broker.append(name.text)
            self.urls.append(f"https://www.forex-ratings.com/{name['href']}")

        for_brokers = pages_info.find_all('span', class_='text-success')
        for broker in for_brokers:
            self.for_broker.append(broker.text)

        against_brokers = pages_info.find_all('span', class_='text-danger')
        for against_brok in against_brokers:
            self.against_broker.append(against_brok.text)

        status_broker = None or pages_info.find_all('a', title='Recommended Forex Broker', href=True)
        for status_brok in status_broker:
            self.status.append(status_brok)

        types_company = pages_info.find_all('td', class_='small text-muted')
        for type_comp in types_company[0::3]:
            self.type_company.append(type_comp.text)

        regulations = pages_info.find_all('td', class_='small text-muted')
        for regulations_type in regulations[1::3]:
            self.regulation.append(regulations_type.text)

        leverages = pages_info.find_all('td', string=re.compile('[0-9]'))

        for type_leverages in leverages[:]:
            self.leverage.append(type_leverages.text)
            youi = [int(i) for i in leverage if i.isdigit()]
            self.dellist.append(youi)

        accounts = pages_info.find_all('td', string=re.compile('[0-9]'))

        for type_accounts in accounts[:]:
            self.account.append(type_accounts.text)
            rejaf = [str(ip) for ip in account if ip.isdigit() == False if '$' in ip]
            self.account_1.append(rejaf)

        advisors = pages_info.find_all('td', class_='small text-muted')
        for advisors_type in advisors[2::3]:
            self.advisor.append(advisors_type.text)

        print(f"Самая частая: {max(set(regulation))}")


if __name__ == '__main__':
    parse = Parser()
    data_frame = pd.DataFrame({'Имя брокеров': name_broker,
                             'Оценка положительная': for_broker,
                             'Оценка отрицaтельная': against_broker,
                             'Тип': type_company,
                             'Регуляции': regulation,
                             'Использовать': info[169],
                             'Счёт': account_1[169],
                             'Советники': advisor,
                             'Ссылка': urls})
    data_frame.to_excel(r'./info/parser.xlsx')

