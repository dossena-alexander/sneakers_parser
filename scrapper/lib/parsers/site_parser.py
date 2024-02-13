from bs4 import BeautifulSoup
from bs4 import Tag

from scrapper.lib.parsers.common.downloader import Downloader
from scrapper.lib.parsers.product_parser import ProductParser

from scrapper.settings import URL    


def make_link(string: str) -> str:
    if not string.startswith('/'):
        string = URL + '/' + string
    return URL + string


class ProductGridParser():
    def __init__(self, main_page_soup: BeautifulSoup) -> None:
        self.main_page = main_page_soup


    def get_products_cards_on_page(self):
        # Находим сетку товаров
        products_grip = self.main_page.find('div', {"id": "browse-grid"})
        # Получаем все карточки товаров 
        products_cards = products_grip\
            .find_all('div', {"class": "css-111hzm2-GridProductTileContainer"})
        return products_cards

    
class Parser():
    url: str
    category: str
    parse_object: str


    def __init__(self, 
                 downloader: Downloader,
                 url: str,
                 category: str) -> None:
        self.downloader = downloader
        self.url = url
        self.category = category
        self.parse_object = self.url+'/'+self.category


    def _make_soup(self, html):
        soup = BeautifulSoup(html, "html.parser")
        return soup
    

    def _get_pages_count(self, category_page: BeautifulSoup):
        pages = int(
            category_page.find('div', {"data-testid": "pagination-wrapper"}
                           ).find_all('a')[-2].contents[0])
        return pages
    

    def _get_products_names_from_grid(self, grid: tuple[Tag]) -> list[str]:
        products_names = []
        for tag in grid:
            if (div_tag := tag.find('div')) is not None:
                if  (a_tag := div_tag.find('a')) is not None:
                    products_names.append(a_tag['href'])
                

        return products_names
    

    def _get_soup_from_url(self, url: str) -> BeautifulSoup:
        downloader = self.downloader
        html = downloader.get_html(url)
        category_page = self._make_soup(html)
        return category_page


    def _get_products_names(self, url: str):
        category_page = self._get_soup_from_url(url)
        grid = ProductGridParser(category_page)

        products_cards = grid.get_products_cards_on_page()
        products_names = self._get_products_names_from_grid(products_cards)
        return products_names


    def get_product(self, link: str) -> dict:
        productParser = ProductParser(self.downloader, link)
        product = productParser.get_product()

        return product

    
    def _get_links_from_page(self, 
                             url: str,
                             page_number: int = 1) -> list[str]:
        url += '?page='+str(page_number)
        products_names = self._get_products_names(url)
        links = [make_link(name) for name in products_names]
        return links
    

    def get_links_from_page(self,
                            page_number: int = 1,
                            filter: str = None) -> list[str]:
        url = self.parse_object
        if filter is not None:
            url += '/'+filter
        links = self._get_links_from_page(
            url=url, page_number=page_number
        )
        return links
    

    def get_links(self, 
                  pages_count: int = 1,
                  filter: str = None) -> list[str]:
        url = self.parse_object
        if filter is not None:
            url += '/'+filter
        links = []
        for page in range(1, pages_count+1):
            page_links = self._get_links_from_page(url, page)
            links += page_links

        return links