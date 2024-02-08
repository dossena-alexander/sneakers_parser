"""
Скрипт для сбора ссылок товаров с сайта

Работает в синхронном режиме
на 12 фильтров, в каждом из которых 25 страниц, уходит около 13 минут времени
2,6с на страницу

Отлично работает с использованием одного VPN
"""
import time
import json
import settings as settings
from scrapper.parsers.downloader import Downloader
from scrapper.parsers.s_parser import Parser


def save(links: set) -> None:
    with open('all-links.txt', 'w') as f:
        for link in links:
            f.writelines(link)
            f.writelines('\n')


def prepare():
    """
    Стадия подготовки
    сбор ссылок на все все товары
    """
    print('начинаем собирать ссылки на товары')
    downloader = Downloader()
    parser = Parser(
        downloader=downloader,
        url=settings.URL, 
        category='sneakers')

    page_links = []
    links_set = list()

    for filter in settings.Filters.all:
        print(f'Текущий фильтр -- {filter}')
        for page_number in range(1, 25+1):
            time.sleep(1)
            print(f'Сбор ссылок на странице: {page_number}')
            try:
                page_links = parser.get_links_from_page(
                    page_number=page_number,
                    filter=filter
                )
                links_set.extend(page_links)
            except Exception as e:
                print(f'Сбор ссылок на странице {page_number} незавершен')
                print('Ошибка')
                print(e)
                break
            print(f'завершен успешно')
    print(links_set)


    save(set(links_set))


def sync_make_links_for_all_products():
    t0= time.time() 
    prepare()
    t1 = time.time() - t0
    print(f'Время выполнения: {t1}с')


if __name__ == '__main__':
    sync_make_links_for_all_products()