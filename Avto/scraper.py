import re
import random
from time import sleep
from requests import request
from parsel import Selector

from constantes import INFORMATION, EXCEPT
from log import logger


class Scraper:

    def __init__(self):
        self.headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) "
                          "Version/11.0 Mobile/15A5341f Safari/604.1"
        }
        self.url = 'https://auto.ria.com/uk/legkovie/?page='

    def get_cars_links(self, number: "int количество пагинации") -> "list список ссылок на карточки авто":
        all_links = []
        for i in range(number):
            url = self.url + str(i+1)
            response = request(method='GET', url=url, headers=self.headers)
            tree = Selector(text=response.text)
            links = tree.xpath('//div[@class="content-bar"]/a/@href').extract()
            for link in links:
                all_links.append(link)
            logger.info(f'созданы ссылки для результатов поиска на {i + 1} странице')
            sleep(random.randrange(2, 4))
        logger.info('создание ссылок для работы с карточками по поиску б/у легковые машины завершено')
        return all_links

    @staticmethod
    def converter_in_int(information: "dict информация про авто") -> "dict преобразованная в int":
        for key, value in information.items():
            if key == 'img_total_count' or key == 'phone_number' or key == 'usd_price':
                information[key] = int(re.sub("[^0-9]", '', value))
        return information

    @staticmethod
    def execute(information: "dict xpath query", tree: 'DOM карточки авто') -> "dict извлечение из xpath":
        converter_information = {}
        for key, value in information.items():
            converter_information[key] = tree.xpath(value).extract_first()
        return converter_information

    @staticmethod
    def validator_none(information: "dict информация про авто") -> bool:
        result = True
        for key, value in information.items():
            if value is None and key not in EXCEPT:
                result = False
                logger.warning("Карточка машины не содержит всех данных")
                break
        return result

    def get_information_about_cars(self, number: 'количество пагинации') -> "list из диктов по каждому авто":
        links = Scraper.get_cars_links(self, number)
        cars = []
        logger.info('Начало работы с карточками машин')
        for number, link in enumerate(links):
            try:
                response = request(method='GET', url=link, headers=self.headers)
                tree = Selector(text=response.text)
                information = Scraper.execute(INFORMATION, tree)
                information['url'] = link
                validation = Scraper.validator_none(information)
                if validation:
                    information = Scraper.converter_in_int(information)
                    cars.append(information)
                    logger.info(f" Завершена обработка {number + 1}-ой машины")
                    sleep(random.randrange(2, 4))
            except Exception as err:
                logger.exception(err)
        logger.info(cars)
        return cars
