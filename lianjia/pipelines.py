# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from lianjia.items import LianjiaHouseItem
from lianjia.items import LianjiaHouseImageItem
# from scrapy import log
import logging


class LianjiaMongoPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.db = db
        self.defaultCollection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        isExist = False
        collection = self.defaultCollection
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if isinstance(item, LianjiaHouseItem):
            isExist = collection.find_one({'lianjia_id': item['lianjia_id']})
        if isinstance(item, LianjiaHouseImageItem):
            collection = self.db['house_images']
            isExist = collection.find_one({'lianjia_id': item['lianjia_id']})
        if not isExist:
            # log.msg(str(item) + ' need insert', level=log.DEBUG)
            collection.insert(dict(item))
        else:
            logging.debug(item['lianjia_id'] + ' is exist')
        return item
