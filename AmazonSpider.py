import scrapy
from bs4 import BeautifulSoup


class AmazonspiderSpider(scrapy.Spider):
    name = "AmazonSpider"
    allowed_domains = ["amazon.com.br"]
    start_urls = ["https://www.amazon.com.br/gp/bestsellers/electronics/16243890011/ref=zg_bs_pg_1_electronics?ie=UTF8&pg=1"]

    def get_product_asins(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        asins = []
        products = soup.findAll('div', {'class': 'data-asin'})
        for product in products:
            asin = product['s-asin']
            asins.append(asin)
            print(asin)


    def parse(self, response):
        responseHtml = response.body
        if response.status == 200:
            product_asins = list(set(self.get_product_asins(responseHtml)))
        print(product_asins)
        
        