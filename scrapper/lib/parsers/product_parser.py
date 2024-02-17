import logging
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
        """
        Возращает продукт (variable) и его варианты (variation)
        """
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

        if gender == 'men':
            gender = 'Мужская'
        elif gender == 'women':
            gender = 'Женская'
        else:
            gender = 'Детская'

        variable = {
            'id': 0,
            'Тип': 'variable',
            'Артикул': styleId,
            'Имя': title,
            'Опубликован': '',
            'Рекомендуемый?': '',
            'Видимость в каталоге': '',
            'Краткое описание': '',
            'Описание': description,
            'Дата начала действия скидки': '',
            'Дата окончания действия скидки': '',
            'Статус налога': '',
            'Налоговый класс': '',
            'Наличие': '',
            'Запасы': '',
            'Величина малых запасов': '',
            'Возможен ли предзаказ?': '',
            'Продано индивидуально?': '',
            'Вес (кг)': '',
            'Длина (см)': '',
            'Ширина (см)': '',
            'Высота (см)': '',
            'Разрешить отзывы от клиентов?': '',
            'Примечание к покупке': '',
            'Акционная цена': '',
            'Базовая цена': '',
            'Категории': '',
            'Метки': '',
            'Класс доставки': '',
            'Изображения': img_link,
            'Лимит загрузок': '',
            'Дней срока загрузки': '',
            'Родительский': '',
            'Сгруппированные товары': '',
            'Апсэлы': '',
            'Кросселы': '',
            'Мета: woovina_disable_breadcrumbs': 'off',
            'Текст кнопки': '',
            'Позиция': '',
            'Название атрибута 1': 'Размер',
            'Значения атрибутов 1': [],
            'Видимость атрибута 1': '1',
            'Глобальный атрибут 1': '1',
            'Название атрибута 2': 'Бренд',
            'Значения атрибутов 2': brand,
            'Видимость атрибута 2': '1',
            'Глобальный атрибут 2': '1',
            'Название атрибута 3': 'Дата выхода',
            'Значения атрибутов 3': date,
            'Видимость атрибута 3': '1',
            'Глобальный атрибут 3': '1',
            'Название атрибута 4': 'Сетка',
            'Значения атрибутов 4': gender,
            'Видимость атрибута 4': '1',
            'Глобальный атрибут 4': '1',
            "sizes": {},
            "variations": []

        }

        for variant in variants:
            size: str = variant['traits']['size']
            try:
                lowestAsk = variant['market']['state']['lowestAsk']
                amount = lowestAsk['amount']
            except TypeError:
                amount = ''
            variable['Значения атрибутов 1'].append(size)
            variable['sizes'][size] = amount

        variable['Значения атрибутов 1'] = ','.join([f'US{size}' for size in variable['Значения атрибутов 1']])

        for size, amount in variable['sizes'].items():
            variable['variations'].append(
                {
                    'id': 0,
                    'Тип': 'variation',
                    'Артикул': styleId,
                    'Имя': title,
                    'Опубликован': '',
                    'Рекомендуемый?': '',
                    'Видимость в каталоге': '',
                    'Краткое описание': '',
                    'Описание': description,
                    'Дата начала действия скидки': '',
                    'Дата окончания действия скидки': '',
                    'Статус налога': '',
                    'Налоговый класс': '',
                    'Наличие': '',
                    'Запасы': '',
                    'Величина малых запасов': '',
                    'Возможен ли предзаказ?': '',
                    'Продано индивидуально?': '',
                    'Вес (кг)': '',
                    'Длина (см)': '',
                    'Ширина (см)': '',
                    'Высота (см)': '',
                    'Разрешить отзывы от клиентов?': '',
                    'Примечание к покупке': '',
                    'Акционная цена': '',
                    'Базовая цена': amount,
                    'Категории': '',
                    'Метки': '',
                    'Класс доставки': '',
                    'Изображения': img_link,
                    'Лимит загрузок': '',
                    'Дней срока загрузки': '',
                    'Родительский': '',
                    'Сгруппированные товары': '',
                    'Апсэлы': '',
                    'Кросселы': '',
                    'Мета: woovina_disable_breadcrumbs': 'off',
                    'Текст кнопки': '',
                    'Позиция': '',
                    'Название атрибута 1': 'Размер',
                    'Значения атрибутов 1': f'US{size}',
                    'Видимость атрибута 1': '',
                    'Глобальный атрибут 1': '1',
                    'Название атрибута 2': 'Бренд',
                    'Значения атрибутов 2': brand,
                    'Видимость атрибута 2': '1',
                    'Глобальный атрибут 2': '1',
                    'Название атрибута 3': 'Дата выхода',
                    'Значения атрибутов 3': '',
                    'Видимость атрибута 3': '',
                    'Глобальный атрибут 3': '',
                    'Название атрибута 4': 'Сетка',
                    'Значения атрибутов 4': '',
                    'Видимость атрибута 4': '',
                    'Глобальный атрибут 4': ''
                }
            )

        variable.pop('sizes')

        return variable