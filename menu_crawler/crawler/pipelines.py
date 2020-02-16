# -*- coding: utf-8 -*-

# Define your item pipelines here
# item pipelines의 커스텀 모듈을 정의하는 곳. pipeline은 item이 다른 저장소로 저장될 때 거치는 통로다.
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class CrawlerPipeline(object):
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = sqlite3.connect("menus.db")
        self.curr = self.conn.cursor()
    
    def create_table(self, item):
        create_table = """CREATE TABLE IF NOT EXISTS menu{}(
                            restaurant_name TEXT,
                            restaurant_tel TEXT,
                            menu_name TEXT NOT NULL UNIQUE,
                            price TEXT,
                            no_pork INTEGER,
                            is_vege INTEGER,
                            is_halal INTEGER,
                            menu_date TEXT,
                            time_for TEXT
                        )""".format(item['date'])

        self.curr.execute(create_table)

    def process_item(self, item, spider):
        if '0' in item['price']:
            self.create_table(item)
            self.store_db(item)
        return item

    def store_db(self, item):
        insert_table = """INSERT INTO menu{} VALUES (?,?,?,?,?,?,?,?,?)""".format(item['date'])

        # insert_table = """INSERT INTO menu{} VALUES (?,?,?,?,?,?,?,?,?)
        # SELECT menu_name FROM menu{}
        # WHERE NOT EXISTS(
        #     SELECT 1 FROM menu{}
        #     WHERE menu_name = {}
        #     )
        # """.format(item['date'], item['date'], item['date'], item['name'])

        self.curr.execute(insert_table, (
            item['restaurant_name'],
            item['restaurant_tel'],
            item['name'],
            item['price'],
            item['no_pork'],
            item['is_vege'],
            item['is_halal'],
            item['date'],
            item['time_for'],
        ))

        self.conn.commit()
