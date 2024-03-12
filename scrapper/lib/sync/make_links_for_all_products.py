"""
Скрипт для сбора ссылок товаров с сайта

Работает в синхронном режиме
на 12 фильтров, в каждом из которых 25 страниц, уходит около 13 минут времени
2,6с на страницу

Отлично работает с использованием одного VPN
"""
import time
import scrapper.settings as settings
from scrapper.lib.parsers.common.downloader import Downloader
from scrapper.lib.parsers.site_parser import Parser
from scrapper.lib.sync.links_set import save_links, discard_dup


def prepare():
    """
    Стадия подготовки
    сбор ссылок на все все товары
    """

    print('начинаем собирать ссылки на товары')
    downloader = Downloader(headers=settings.HEADERS[0])
    parser = Parser(
        downloader=downloader,
        url=settings.URL, 
        category=settings.CATEGORY)

    page_links = []

    for filter in settings.Filters.all:
        print(f'Текущий фильтр -- {filter}')
        for page_number in range(1, 25+1):
            print(f'Сбор ссылок на странице: {page_number}')
            try:
                page_links = parser.get_links_from_page(
                    page_number=page_number,
                    filter=filter
                )
                save_links(page_links)
                print(f'В файл записано {len(page_links)} ссылок')
            except Exception as e:
                print(f'Сбор ссылок на странице {page_number} незавершен')
                print('Ошибка')
                print(e)
                break
            print(f'завершен успешно')
            time.sleep(settings.LNK_TIME_TO_SLEEP)
            
    discard_dup()
    


def sync_make_links_for_all_products():
    t0= time.time() 
    prepare()
    t1 = time.time() - t0
    print(f'Время выполнения: {t1}с')


if __name__ == '__main__':
    sync_make_links_for_all_products()