import re
import random
from time import sleep

from requests import request
from parsel import Selector

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) "
                  "Version/11.0 Mobile/15A5341f Safari/604.1"
}

def get_cars_links(number):
    url_ = 'https://auto.ria.com/uk/legkovie/?page='
    all_links = []
    print('Старт сбора информации по машинам в категории б/у, легковые на сайте avto.ria')
    for i in range(number):
        url = url_ + str(i+1)
        response = request(method='GET', url=url, headers=headers)
        tree = Selector(text=response.text)
        links = tree.xpath('//div[@class="content-bar"]/a/@href').extract()
        for link in links:
            all_links.append(link)
        print(f'созданы ссылки для результатов поиска на {i + 1} странице')
        sleep(random.randrange(2, 4))
    print('создание ссылок для работы с карточками по поиску б/у легковые машины завершено')
    return all_links


def get_information_about_cars(number):
    links = get_cars_links(number)
    cars = []
    print('Начало работы с карточками машин')
    for number, link in enumerate(links):
        try:
            response = request(method='GET', url=link, headers=headers)
            tree = Selector(text=response.text)
            information = {}
            information['url'] = link
            information['title'] = tree.xpath('//h1[@class="head"]/text()').extract_first()
            information['usd_price'] = int(re.sub("[^0-9]", '',
                                                  tree.xpath('//span[@class="price_value bold"]/text()').extract_first()))
            information['mileage'] = tree.xpath('//div[@class="mb-10 bold dhide"]/text()').extract_first()
            information['username'] = tree.xpath('//h4[@class="seller_info_name bold"]/text()').extract_first()
            information['phone_number'] = int(re.sub("[^0-9]", '', tree.xpath('//div[@class="phones_item "]'
                                                                             '/span/@data-phone-number').extract_first()))
            information['img_url'] = tree.xpath('//img[@class="outline m-auto"]/@src').extract_first()
            information['img_total_count'] = int(re.sub("[^0-9]", '',
                                         tree.xpath('//span[@class="count"]/span[@class="dhide"]/text()').extract_first()))
            try:
                information['car_number'] = tree.xpath('//span[@class="state-num ua"]/text()').extract_first()
            except Exception:
                information['car_number'] = None
            try:
                information['car_vin_code'] = tree.xpath('//span[@class="vin-code"]/text()').extract_first()
            except Exception:
                information['car_vin_code'] = None
        except Exception:
            print(f"ошибка обработки {number + 1}-ой машины")
            continue
        sleep(random.randrange(2, 4))
        cars.append(information)
        print(f" Завершена обработка {number + 1}-ой машины")
    print(cars)
    return cars
