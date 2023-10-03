# pipelines.py

import psycopg2
import time

class SaveToPostgresPipeline:

    def __init__(self):
        ## Connection Details
        hostname = 'localhost'
        username = 'postgres'
        password = 'postgres'
        database = 'price_alert'

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()


    def process_item(self, item, spider):

        self.cur.execute("""
            SELECT price
            FROM prices
            WHERE asin = %s
            ORDER BY created_at DESC
            LIMIT 1
        """, (item['asin'],))

        last_price = self.cur.fetchone()

        if last_price:
            last_price = last_price[0]
        else:
            last_price = item['price']


                ## Define insert statement
        self.cur.execute(""" insert into books (asin, title, image) values ('A','A','A')""")

        ## Execute insert of data into database
        self.connection.commit()
        return item

    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()
