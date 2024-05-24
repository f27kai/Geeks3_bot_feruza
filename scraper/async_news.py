import httpx
from parsel import Selector
import asyncio

class AsyncNewsScraper:
    URL = "https://dorama.land/2024"
    HEADERS = {
        "Accept": "text / html, application / xhtml + xml, application / xml; q = 0.9, image / avif, image / webp, * / *;q = 0.8",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0"
    }

    DORAM_LINK_XPATH = '//div[@class="short-cinematic short-cinematic--episode"]/a/@href'

    async def fetch(self, client):
        response = await client.get(self.URL, headers=self.HEADERS)
        return Selector(response.text)

    async def scrape_data(self):
        async with httpx.AsyncClient(headers=self.HEADERS) as client:
            html = await self.fetch(client)
            doram_links = html.xpath(self.DORAM_LINK_XPATH).getall()
            print(doram_links)
            return doram_links[:5]



if __name__ == "__main__":
    scraper = AsyncNewsScraper()
    asyncio.run(scraper.scrape_data())