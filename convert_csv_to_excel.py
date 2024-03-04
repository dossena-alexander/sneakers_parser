import pandas
from scrapper import settings


def convert_to_excel():
    with open(f'{settings.PATH.scrapped}/products-table.csv', 'r') as f:
        df = pandas.read_csv(f)
    
    df.to_excel()

if __name__ == '__main__':
    convert_to_excel()