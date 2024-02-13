import json
from bs4 import BeautifulSoup

from scrapper.lib.parsers.common.downloader import Downloader


class ProductParser():
    def __init__(self, 
                 downloader: Downloader, 
                 link: str = None, 
                 file: str = False) -> None:
        self.downloader = downloader
        self.link = link
        self.file = file


    def _get_html_file(self) -> str:
        with open(self.link, 'r') as file:
            s = file.read()
        return s


    def _get_html(self) -> str:
        downloader = self.downloader
        html = downloader.get_html(self.link)
        return html
    

    def _get_soup(self) -> BeautifulSoup:
        if self.file:
            html = self._get_html_file()
        else:
            html = self._get_html()
        soup = BeautifulSoup(html, "html.parser")
        return soup
    

    def _get_script_json(self) -> dict:
        soup = self._get_soup()
        script_json = soup.find('script', {'id': '__NEXT_DATA__'}).contents[0]
        return json.loads(str(script_json))


    def get_product(self) -> dict:
        json = self._get_script_json()
        product = json['props']['pageProps']['req']['appContext']['states']['query']['value']['queries'][2]['state']['data']['product']
        soup = self._get_soup()
        div = soup.find('div', {'data-component': 'ProductDescription'})
        if div is None:
            description = 'No description'
        else:
            description = div.find('p').contents[0]

        brand = product['brand']
        title = product['title']
        try:
            date = product['Onytraits'][3]['value']
        except KeyError:
            date = product['traits'][3]['value']
        styleId = product['styleId']
        condition = product['condition']
        gender = product['gender']
        img_link = product['media']['smallImageUrl']
        variants = product['variants']

        p = {
            "brand": brand,
            "name": title,
            "date": date,
            "styleId": styleId,
            "condition": condition,
            "gender": gender,
            "img_link": img_link,
            "description": description,
            "sizes": {}
        }

        # p.update(dict.fromkeys([str(size/2) for size in range(2, 41)]))

        for variant in variants:
            size: str = variant['traits']['size']
            # if var_size.endswith('W'):
            #     var_size = var_size[:-1]
            # size = str(float(var_size))
            try:
                lowestAsk = variant['market']['state']['lowestAsk']
                amount = lowestAsk['amount']
            except TypeError:
                amount = '0'
            p['sizes'][size] = amount

        return p
    

# class SingleProductParser():
