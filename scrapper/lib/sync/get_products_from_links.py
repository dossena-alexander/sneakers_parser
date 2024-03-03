import progress
import logging
import time
import pandas as pd
from progress.bar import IncrementalBar
import os

import scrapper.settings as settings
from scrapper.lib.parsers.common.downloader import Downloader
from scrapper.lib.parsers.product_parser import ProductParser
from scrapper.lib.sync.table import write_variable, write_headers


def sleep_time():
    mylist = [i for i in range(1, settings.PDT_TIME_TO_SLEEP+1)]
    bar = IncrementalBar('Ожидание', max=len(mylist))
    for item in mylist:
        bar.next()
        time.sleep(1)
    bar.finish()


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
    write_headers()
    downloader = Downloader(headers=settings.HEADERS[0])
    links = get_links()
    limit = settings.PARSER_LIMIT
    if limit is None:
        arange = links
    else:
        arange = links[:limit]
    bar = IncrementalBar('Парсинг ссылок', max=len(arange))
    for link in arange:
        bar.next()
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
            logging.error(e)
            print(e)
            print('Продукт не был получен. Ссылка записана в файл Data/scrapped/failed-links.txt')
            save_failed_link(link)
        sleep_time()
        os.system('cls' if os.name == 'nt' else 'clear')
    bar.finish


def parse():
    sync_get_products()