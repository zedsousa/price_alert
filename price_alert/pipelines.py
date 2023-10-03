# pipelines.py

import time
import psycopg2
import requests

class SaveToPostgresPipeline:

    def __init__(self):
        ## Connection Details
        hostname = 'containers-us-west-131.railway.app'
        username = 'postgres'
        password = '6ZrstQAhzDWB1ObnJeVf'
        database = 'railway'
        port = '6073'

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, port=port, user=username, password=password, dbname=database)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()

        ## Start Telegram bot
        
        

    def send_telegram_message(self, item, last_price):
        CHAT_ID = '-4029718995'
        API_KEY_TOKEN = '6692849053:AAFnjXhkCRmU-FUOnP6_2UWQTLM0HC07kLE'
        last_price = f'R${last_price:.2f}'
        price = f"R${item['price']:.2f}"
        last_price = last_price.replace('.', ',')
        price = price.replace('.', ',')

        message = f"{item['title']}\n\n 📉Custava: {last_price} \n💰Valor à Vista: {price}🔥\n {item['best_offer']}\n\n 🔗https://www.amazon.com.br/-/dp/{item['asin']}\n\n ⚠️ Preços sujeitos à alteração sem aviso prévio."
        
        requests.post("https://api.telegram.org/bot" + API_KEY_TOKEN + "/sendPhoto", {"photo": item['image'], "chat_id": CHAT_ID, "caption": message})
    

    def process_item(self, item, spider):

        self.cur.execute("""
            SELECT price
            FROM prices
            WHERE asin = %s
            ORDER BY created_at DESC
            LIMIT 1
        """, (item['asin'],))

        last_price = self.cur.fetchone()
        
        if last_price and (float(last_price[0]) - item['price']) > 10:
            ## Send Telegram message
            self.send_telegram_message(item, last_price[0])

        if last_price:
            last_price = last_price[0]
        else:
            last_price = item['price']

                ## Define insert statement
        self.cur.execute("""
            INSERT INTO prices (asin, title, image, last_price, price, best_offer, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            item["asin"],
            item["title"],
            item["image"],
            last_price,
            item["price"],
            item["best_offer"],
            time.strftime("%Y-%m-%d %H:%M:%S")
        ))

        ## Execute insert of data into database
        self.connection.commit()
        return item

    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()
