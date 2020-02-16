# -*- coding: utf-8 -*-

# Define your item pipelines here
# item pipelines의 커스텀 모듈을 정의하는 곳. pipeline은 item이 다른 저장소로 저장될 때 거치는 통로다.
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class CrawlerPipeline(object):
    def process_item(self, item, spider):

        return item
