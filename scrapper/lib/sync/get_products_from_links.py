import logging
import time
import json
import pandas as pd
import csv

from scrapper.lib.parsers.common.downloader import Downloader
from scrapper.lib.parsers.product_parser import ProductParser
import scrapper.settings as settings


failed_links = []
products = {'all': []}

class CatchEnd(object):
    def __enter__(self):
        pass

    def __exit__(self, type, value, trace):
        print("Заканчиваю работу...")
        print('Сохраняю продукты')
        save(products)
        print('Продукты сохранены')


def get_links() -> list[str]:
    with open(settings.PATH.all_links, 'r') as f:
        links = [line.rstrip() for line in f]

    return links


def save(d):
    with open(f'{settings.PATH.scrapped}/products.json', 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=4, ensure_ascii=False)

    with open(f'{settings.PATH.scrapped}/products-table.csv', 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=\
            ['id', 
             'Тип',
             'Артикул', 
             'Имя',
             'Опубликован', 
             'Рекомендуемый?',
             'Видимость в каталоге', 
             'Краткое описание', 
             'Описание', 
             'Дата начала действия скидки',
             'Дата окончания действия скидки',
             'Статус налога',
             'Налоговый класс',
             'Наличие',
             'Запасы',
             'Величина малых запасов',
             'Возможен ли предзаказ?',
             'Продано индивидуально?',
             'Вес (кг)',
             'Длина (см)',
             'Ширина (см)', 
             'Высота (см)', 
             'Разрешить отзывы от клиентов?',
             'Примечание к покупке',
             'Акционная цена', 
             'Базовая цена', 
             'Категории', 
             'Метки',
             'Класс доставки', 
             'Изображения', 
             'Лимит загрузок',
             'Дней срока загрузки', 
             'Родительский', 
             'Сгруппированные товары', 
             'Апсэлы', 
             'Кросселы', 
             'Мета: woovina_disable_breadcrumbs', 
             'Текст кнопки', 
             'Позиция',
             'Название атрибута 1', 
             'Значения атрибутов 1',
             'Видимость атрибута 1', 
             'Глобальный атрибут 1', 
             'Название атрибута 2',
             'Значения атрибутов 2',
             'Видимость атрибута 2',
             'Глобальный атрибут 2',
             'Название атрибута 3', 
             'Значения атрибутов 3',
             'Видимость атрибута 3', 
             'Глобальный атрибут 3',
             'Название атрибута 4',
             'Значения атрибутов 4',
             'Видимость атрибута 4', 
             'Глобальный атрибут 4'])
        writer.writeheader()
        for product in d['all']:
            variations = product.pop('variations')
            writer.writerow(product)
            writer.writerows(variations)

    with open(f'{settings.PATH.scrapped}/failed-links.txt', 'w') as f:
        for line in failed_links:
            f.write(line)
            f.write('\n')


def sync_get_products():
    downloader = Downloader(headers=settings.HEADERS[0])
    links = get_links()
    for link in links[:10]:
        print(f'Обработка {link}')
        logging.info(f'Обработка {link}')
        try:
            logging.info('Скачивание')
            pp = ProductParser(downloader, link)
            logging.info('Скачивание завершено')
            logging.info('Парсинг')
            variable = pp.get_product()
            logging.info('Парсинг завершен')
            products['all'].append(variable)
            print(f'Продукт получен')
        except Exception as e:
            logging.error(e)
            print(e)
            print('Продукт не был получен. Ссылка записана в файл Data/scrapped/failed-links.txt')
            failed_links.append(link)
        time.sleep(settings.TIME_TO_SLEEP)

    save(products)


def parse():
    # with CatchEnd():
        # sync_get_products()

    sync_get_products()


if __name__ == "__main__":
    sync_get_products()
