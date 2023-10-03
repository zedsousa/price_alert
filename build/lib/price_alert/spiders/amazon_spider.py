# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup

from urllib.parse import urlencode
from urllib.parse import urljoin
import re
import json
from price_alert.items import AmazonItem

API = '2fc415458a228ed3ba18ff5cd363a92b'                       

def get_url(url):
    payload = {'api_key': API, 'url': url, 'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


class AmazonSpider(scrapy.Spider):
    name = 'amazon'

    def start_requests(self):
        url = 'https://www.amazon.com.br/gp/bestsellers/electronics/16243890011/ref=zg_bs_pg_1_electronics?ie=UTF8&pg=1'
        yield scrapy.Request(url=get_url(url), callback=self.parse_asin)

    def parse_asin(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'html.parser')
        products = soup.findAll('div', {'class': 'p13n-sc-uncoverable-faceout'})

        for product in products:
            asin = product['id']
            product_url = f"https://www.amazon.com.br/-/dp/{asin}"
            yield scrapy.Request(url=get_url(product_url), callback=self.parse_product, meta={'asin': asin})
            

    def parse_product(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'html.parser')
        
        product = AmazonItem()

        product['asin'] = response.meta['asin']
        product['title'] = soup.find('span', {'id': 'productTitle'}).get_text()
        product['image'] = re.search('"large":"(.*?)"',response.text).groups()[0]
        product['price'] = float(soup.findAll('span', {'class': 'priceToPay'})[0].findAll('span')[0].get_text().replace('R$','').replace('.','').replace(',','.'))
        product['best_offer'] = soup.find('span', {'class': 'best-offer-name'}).get_text()
       
        yield product

        



