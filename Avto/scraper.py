import re
import random
from time import sleep
from requests import request
from parsel import Selector


class Scraper:

    def __init__(self):
        self.headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) "
                          "Version/11.0 Mobile/15A5341f Safari/604.1"
        }
        self.url = 'https://auto.ria.com/uk/legkovie/?page='

    def get_cars_links(self, number):
        all_links = []
        print('Старт сбора информации по машинам в категории б/у, легковые на сайте avto.ria')
        for i in range(number):
            url = self.url + str(i+1)
            response = request(method='GET', url=url, headers=self.headers)
            tree = Selector(text=response.text)
            links = tree.xpath('//div[@class="content-bar"]/a/@href').extract()
            for link in links:
                all_links.append(link)
            print(f'созданы ссылки для результатов поиска на {i + 1} странице')
            sleep(random.randrange(2, 4))
        print('создание ссылок для работы с карточками по поиску б/у легковые машины завершено')
        return all_links

    @staticmethod
    def converter_in_int(information: dict):
        for key, value in information.items():
            if key == 'img_total_count' or key == 'phone_number' or key == 'usd_price':
                if key:
                    information[key] = int(re.sub("[^0-9]", '', value))
        return information

    @staticmethod
    def execute(information: dict, tree):
        converter_information = {}
        for key, value in information.items():
            converter_information[key] = tree.xpath(value).extract_first()
        return converter_information

    @staticmethod
    def validator_none(information: dict):
        result = True
        for key, value in information.items():
            if key == 'car_number' or key == 'car_vin_code':
                pass
            else:
                if value == None:
                    result = False
                    print("Карточка машины не содержит всех данных")
                    break
        return result

    def get_information_about_cars(self, number: 'количество страниц для поиска'):
        links = Scraper.get_cars_links(self, number)
        cars = []
        print('Начало работы с карточками машин')
        for number, link in enumerate(links):
            response = request(method='GET', url=link, headers=self.headers)
            tree = Selector(text=response.text)
            information = Scraper.execute({
                'title': '//h1[@class="head"]/text()',
                'mileage': '//div[@class="mb-10 bold dhide"]/text()',
                'username': '//h4[@class="seller_info_name bold"]/text()',
                'img_url': '//img[@class="outline m-auto"]/@src',
                'car_number': '//span[@class="state-num ua"]/text()',
                'car_vin_code': '//span[@class="vin-code"]/text()',
                'img_total_count': '//span[@class="count"]/span[@class="dhide"]/text()',
                'phone_number': '//span/@data-phone-number',
                'usd_price': '//span[@class="price_value bold"]/text()'
            }, tree)
            information['url'] = link
            validation = Scraper.validator_none(information)
            if validation:
                information = Scraper.converter_in_int(information)
                cars.append(information)
                print(f" Завершена обработка {number + 1}-ой машины")
                sleep(random.randrange(2, 4))
        print(cars)
        return cars
