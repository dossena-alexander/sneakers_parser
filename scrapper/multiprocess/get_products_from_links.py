import time
import json
import pandas as pd
import logging
# from multiprocessing import Pool, current_process
from multiprocessing import Process, current_process
from functools import partial

from scrapper.parsers.downloader import Downloader
from scrapper.parsers.product_parser import ProductParser
import settings


def get_links() -> list[str]:
    with open(settings.PATH.all_links, 'r') as f:
        links = [line.rstrip() for line in f]

    return links


class ProxyRotator:
    def __init__(self, proxies):
        self.proxies = proxies
        self.current_proxy_index = hash(current_process().name)

    def get_next_proxy(self):
        proxy = self.proxies[self.current_proxy_index % len(self.proxies)]
        self.current_proxy_index += 1
        return proxy


def process_links_chunk(links_chunk, downloader, proxy_rotator, failed_links, process_name, results):
    logging.info(f'Процесс {process_name} начал обработку')

    for link in links_chunk:
        try:
            proxy = proxy_rotator.get_next_proxy()
            downloader.set_proxy(proxy)

            p = ProductParser(downloader=downloader, link=link, file=False)
            product = p.get_product()
            logging.info(f'Продукт для ссылки {link} получен')
            results.append(product)
        except Exception as e:
            logging.error(f'Произошла ошибка при обработке ссылки {link} с использованием прокси {proxy}')
            logging.error(e)
            failed_links.append(link)

    logging.info(f'Процесс {process_name} завершил обработку')


def read_proxies_from_csv(file_path):
    df = pd.read_csv(file_path)
    proxies = [f'{row["ip"]}:{row["port"]}' for index, row in df.iterrows()]
    return proxies


def sync_get_products(downloader: Downloader, proxies_file):
    logging.basicConfig(level=logging.INFO)
    
    links = get_links()
    results = []
    all_products = {'all': []}
    failed_links = []

    proxies = read_proxies_from_csv(proxies_file)
    proxy_rotator = ProxyRotator(proxies)

    processes = []
    chunk_size = len(links) // 1
    link_chunks = [links[i:i + chunk_size] for i in range(0, len(links), chunk_size)]

    for i, links_chunk in enumerate(link_chunks):
        process_name = f"Process-{i + 1}"
        process = Process(target=process_links_chunk, args=(links_chunk, downloader, proxy_rotator, failed_links, process_name, results))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    all_products['all'].extend(filter(None, results))

    with open('products.json', 'w') as file:
        json.dump(all_products, file, indent=2)

    df = pd.DataFrame(all_products['all'])
    df.to_csv("products-table.csv", index=False)

    with open('failed_links.txt', 'w') as failed_file:
        failed_file.write('\n'.join(failed_links))


def multiprocess_get_products():
    downloader = Downloader(headers=settings.HEADERS[0])
    proxies_file = 'proxies.csv'  # Укажите путь к вашему файлу с прокси
    sync_get_products(downloader, proxies_file)


if __name__ == "__main__":
    multiprocess_get_products()

