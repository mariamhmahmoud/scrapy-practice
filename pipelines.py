# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3 
from itemadapter import ItemAdapter


class ScrapePracticePipeline:

    def __init__(self):
        self.make_connection()
        self.make_table()

    def make_connection(self):
        self.connection = sqlite3.connect('books.db')
        self.cursor = self.connection.cursor()

    def make_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS books_tb""")
        self.cursor.execute("""CREATE TABLE books_tb(
            title text,
            price text,
            rating text
        )""")
    
    def process_item(self, item, spider):
        self.store_data(item)
        return item

    def store_data(self, item):
        self.cursor.execute("""INSERT INTO books_tb values (?, ?, ?) """,(
            item['title'],
            item['price'],
            item['rating']
        ))
        self.connection.commit()
