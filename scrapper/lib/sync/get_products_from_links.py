import time
import json
import pandas as pd

from scrapper.lib.parsers.common.downloader import Downloader
from scrapper.lib.parsers.product_parser import ProductParser
import scrapper.settings as settings


failed_links = []


def get_links() -> list[str]:
    with open(settings.PATH.all_links, 'r') as f:
        links = [line.rstrip() for line in f]

    return links


def save(d):
    with open(f'{settings.PATH.scrapped}/products.json', 'w') as f:
        json.dump(d, f, indent=4)

    df = pd.DataFrame(d['all'])
    df.to_csv(f'{settings.PATH.scrapped}/products-table.csv', index=False)

    with open(f'{settings.PATH.scrapped}/failed-links.txt', 'w') as f:
        for line in failed_links:
            f.write(line)
            f.write('\n')


def sync_get_products():
    downloader = Downloader(headers=settings.HEADERS[0])
    links = get_links()
    products = {'all': []}
    for link in links[:1]:
        print(f'Обработка {link}')
        try:
            pp = ProductParser(downloader, link)
            product = pp.get_product()
            products['all'].append(product)
            print(f'Продукт получен')
        except Exception as e:
            print(e)
            print('Продукт не был получен. Ссылка записана в файл Data/scrapped/failed-links.txt')
            failed_links.append(link)
        time.sleep(settings.TIME_TO_SLEEP)

    save(products)


def parse():
    sync_get_products()


if __name__ == "__main__":
    sync_get_products()
