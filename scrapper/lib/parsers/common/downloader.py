import httpx

import scrapper.settings as settings


class Downloader():
    headers: list[dict]


    def __init__(self, 
                 proxy: str | None = None, 
                 headers: str | None = None
    ) -> None:
        self.proxy = proxy
        self.headers = headers

    def set_proxy(self, proxy_url: str):
        self.proxy = proxy_url

    def set_headers(self, headers: set):
        self.headers = headers

    def make_response(self, url):
        response = httpx.get(
                            url,
                            proxies=self.proxy,
                            headers=self.headers,
                            verify=False,
                            timeout=60
        )
        return response

    def get_html(self, url: str):
        response = self.make_response(url)
        return response.text
    
    def get_img(self, url: str):
        response = self.make_response(url)
        return response.content