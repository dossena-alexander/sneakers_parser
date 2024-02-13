from scrapper.lib.sync.get_products_from_links import sync_get_products
from scrapper.lib.sync.make_links_for_all_products import sync_make_links_for_all_products


def get_products():
    return sync_get_products()

def get_links():
    return sync_make_links_for_all_products()