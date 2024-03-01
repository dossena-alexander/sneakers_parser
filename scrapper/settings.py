URL = 'https://stockx.com'
CATEGORY = 'sneakers'
PDT_TIME_TO_SLEEP = 30
LNK_TIME_TO_SLEEP = 10
PARSER_LIMIT = 10
# ДЛЯ ОТКЛЮЧЕНИЯ ЛИМИТА ПАРСИНГА ТОВАРОВ РАСКОММЕНТИРОВАТЬ СТРОКУ НИЖЕ
# PARSER_LIMIT = None 




class PATH():
    scrapped = 'Data/scrapped'
    all_links = 'Data/links/All-links.txt'

# WINDOWS PATH's / Uncomment this if windows
# class PATH():
#     scrapped = 'Data\scrapped'
#     all_links = "Data\links\All-links.txt"


class Filters():
    featured = 'featured'
    most_popular = 'most-popular'
    recent_asks = 'recent-asks'
    recent_bids = 'recent-bids'
    most_expensive = 'most-expensive'
    top_selling = 'top-selling'
    price_volatility = 'price-volatility'
    price_premium = 'price-premium'
    last_sale = 'last-sale'
    lowest_ask = 'lowest-ask'
    highest_bid = 'highest-bid'
    release_date = 'release-date'
    all = [
        'featured', #just a main page of a category
        'most-popular',
        'recent-asks',
        'recent-bids',
        'most-expensive',
        'top-selling',
        'price-volatility',
        'price-premium',
        'last-sale',
        'lowest-ask',
        'highest-bid',
        'release-date'
    ]

    
HEADERS = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    },
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    },
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    },
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    },
    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    },
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    },
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
]