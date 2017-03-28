import re
import scrapy
from bs4 import BeautifulSoup
import sys
from scrapy.http import Request
from lianjia.items import LianjiaHouseItem
from lianjia.items import LianjiaHouseImageItem
from bs4 import BeautifulSoup
import json
reload(sys)
sys.setdefaultencoding("utf-8")


class Myspider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['dg.lianjia.com']
    bash_url = 'http://dg.lianjia.com/ershoufang/'
    image_urls = []

    def start_requests(self):
        # yield Request(self.bash_url, self.parse)
        detail_url = 'http://dg.lianjia.com/ershoufang/DG0002394497.html'
        yield Request(detail_url, self.parse_hosue_detail)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        page_num_list = soup.find('div', {'class': 'house-lst-page-box'}).attrs['page-data']
        jsonstr = json.loads(page_num_list)
        # print jsonstr
        # print jsonstr['totalPage']
        max_page_num = jsonstr['totalPage']
        for num in range(1, int(max_page_num) + 1):
            url = self.bash_url + 'pg' + str(num) + '/'
            print url
            yield Request(url, callback=self.parse_houselist)

        # http://dg.lianjia.com/ershoufang/pg75/
        # .find('div', class_='house-lst-page-box')

    def parse_houselist(self, response):
        # print(response.text)
        print 'parse start'
        soup = BeautifulSoup(response.text, 'lxml')
        house_list = soup.find('ul', {'class': 'sellListContent'}).findAll('li')
        for house in house_list:
            # print house
            # print type(house)
            infoDiv = house.find('div', {'class': 'info'})
            # print infoDiv
            titleDiv = infoDiv.find('a')
            # print titleDiv
            priceDiv = infoDiv.find('div', {'class': 'priceInfo'})
            # print priceDiv
            house_price = priceDiv.find('div', {'class': 'totalPrice'}).text
            # print house_price
            house_unit_price = priceDiv.find('div', {'class': 'unitPrice'}).attrs['data-price']

            addressDiv = infoDiv.find('div', {'class': 'address'})
            # print addressDiv
            # print house_unit_price.text
            house_title = titleDiv.text
            house_link = house.find('a')['href']
            # print house_link
            tmp_start = house_link.rfind('/') + 1
            tmp_end = house_link.find('.html')
            house_id = house_link[tmp_start:tmp_end]
            # print 'house_id: ' + house_id
            house_obj = {'id': house_id, 'title': house_title, 'link': house_link,
                         'price': house_price, 'unit_price': house_unit_price}
            # print house_obj
            house = LianjiaHouseItem()
            house['lianjia_id'] = house_id
            house['title'] = house_title
            house['link'] = house_link
            house['price'] = house_price
            house['unit_price'] = house_unit_price
            yield house

    def parse_hosue_detail(self, response):
        print 'parse_hosue_detail start'
        soup = BeautifulSoup(response.text, 'lxml')
        house_img_list = soup.find('ul', {'class': 'smallpic'}).findAll('li')
        imageArr = []
        for house_img in house_img_list:
            print house_img

            print house_img.attrs['data-src']
            imageArr.append(house_img.attrs['data-src'])
            # item['image_urls'] = house_img.attrs['data-src']
            # print item['image_urls']
            # yield item
            self.image_urls.append(house_img.attrs['data-src'])
        print self.image_urls
        item = LianjiaHouseImageItem()
        item['image_urls'] = imageArr
        return item
        # yield item
