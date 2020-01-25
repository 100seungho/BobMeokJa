# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# 크롤링할 데이터를 저장하는 기능을 하는 객체의 클래스를 정의하는 곳.
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MealItem(scrapy.Item):
    restaurant_name = scrapy.Field()
    restaurant_tel = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    no_pork = scrapy.Field()
    is_vege = scrapy.Field()
    is_halal = scrapy.Field()
    date = scrapy.Field()
    time_for = scrapy.Field()