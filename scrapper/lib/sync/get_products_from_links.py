from tqdm import tqdm
import logging
import time
import pandas as pd
import os

import scrapper.settings as settings
from scrapper.lib.parsers.common.downloader import Downloader
from scrapper.lib.parsers.product_parser import ProductParser
from scrapper.lib.sync.products_table import write_variable, write_headers


def sleep_time():
    mylist = [i for i in range(1, settings.PDT_TIME_TO_SLEEP+1)]
    for item in tqdm(mylist, 'Ожидание'):
        time.sleep(1)


failed_links = []
products = {'all': []}


def get_links() -> list[str]:
    with open(settings.PATH.all_links, 'r') as f:
        links = [line.rstrip() for line in f]

    return links


def save_failed_link(link):
    with open(f'{settings.PATH.scrapped}/failed-links.txt', 'a') as f:
        f.write(link)
        f.write('\n')


def sync_get_products():
    # x = 'https://stockx.com/air-jordan-4-retro-bred-reimagined'
    # downloader = Downloader(headers=settings.HEADERS[0])
    # pp = ProductParser(downloader, x)
    # with open('some.html', 'w') as f:
    #     f.write(pp._get_html())
    # variable = pp.get_product()
    # print(variable)
    # return
    write_headers()
    links = get_links()
    limit = settings.PARSER_LIMIT
    if limit is None:
        arange = links
    else:
        arange = links[:limit]
    for c, link in enumerate(tqdm(arange, 'Парсинг ссылок')):
        if c >= 0 and c < 300:
            print(f'Меняю Headers -- {0}')
            downloader = Downloader(headers=settings.HEADERS[0])
        elif c >= 300 and c < 600:
            print(f'Меняю Headers -- {1}')
            downloader = Downloader(headers=settings.HEADERS[1])
        elif c >= 600 and c < 1200:
            print(f'Меняю Headers -- {2}')
            downloader = Downloader(headers=settings.HEADERS[2])
        elif c >= 1200 and c < 1600:
            print(f'Меняю Headers -- {3}')
            downloader = Downloader(headers=settings.HEADERS[3])
        elif c >= 1600 and c < 2000:
            print(f'Меняю Headers -- {4}')
            downloader = Downloader(headers=settings.HEADERS[4])
        elif c >= 2000 and c < 2300:
            print(f'Меняю Headers -- {5}')
            downloader = Downloader(headers=settings.HEADERS[5])
        else:
            print(f'Меняю Headers -- {6}')
            downloader = Downloader(headers=settings.HEADERS[6])
        print(f'\nОбработка {link}')
        logging.info(f'Обработка {link}')
        try:
            print('Скачивание')
            logging.info('Скачивание')
            pp = ProductParser(downloader, link)
            print('Скачивание завершено')
            logging.info('Скачивание завершено')
            logging.info('Парсинг')
            print('Парсинг')
            variable = pp.get_product()
            logging.info('Парсинг завершен')
            print('Парсинг завершен')
            write_variable(variable)
            print('Variable записан')

        except Exception as e:
            logging.info(e)
            print(e)
            print('Продукт не был получен. Ссылка записана в файл Data/scrapped/failed-links.txt')
            save_failed_link(link)
        sleep_time()
        os.system('cls' if os.name == 'nt' else 'clear')


def parse():
    sync_get_products()