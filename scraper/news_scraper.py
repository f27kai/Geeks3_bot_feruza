import requests
from parsel import Selector

class NewsScraper:
    URL = "https://dorama.land/2024"
    HEADERS = {
        "Accept": "text / html, application / xhtml + xml, application / xml; q = 0.9, image / avif, image / webp, * / *;q = 0.8",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0"
    }

    DORAM_LINK_XPATH = '//div[@class="short-cinematic short-cinematic--episode"]/a/@href'

    def scrape_data(self):
        response = requests.get(self.URL, headers=self.HEADERS)
        tree = Selector(response.text)
        doram_link = tree.xpath(self.DORAM_LINK_XPATH).getall()
        return doram_link[:5]


if __name__ == "__main__":
    scraper = NewsScraper()
    scraper.scrape_data()