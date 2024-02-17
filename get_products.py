import logging
from scrapper import get_products

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")

if __name__ == '__main__':
    get_products()