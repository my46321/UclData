# -*- coding: cp936 -*-
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
#!/usr/bin/python
#-*-coding:utf-8-*-

import time
from pprint import pprint
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from srtpProject.items import SrtpprojectItem
from srtpProject.utils.select_result import list_first_item,strip_null,deduplication,clean_url
from bs4 import BeautifulSoup

class Spider1(BaseSpider):
    name = "xinhua"
    start_urls = (
            #'http://www.woaidu.org/sitemap_1.html',
            #'http://www.news.cn/politics/',
            #'http://www.news.cn/fortune/',
            'http://www.sznews.com/photo/node_150826.htm',
            'http://www.sznews.com/photo/node_150830.htm'
    )

 
    title = "title"
    summary = "summary"
    picture = "img_url"
    news_url = "news_url"
    content = "content"
    
    def parse(self,response):
        soup = BeautifulSoup(response.text, "lxml")
        domain='http://www.sznews.com/photo/'
        for tag in soup('div',class_='list-pt'):
            title=tag.find(u'h3').string
            summary=tag.find(u'p',class_='info').string
            picture=domain+tag.find(u'img')['src']
            news_url=domain+tag.find(u'a')['href']
            detail_link=news_url
            
            detail_link = clean_url(response.url,detail_link,response.encoding)
            yield Request(url=detail_link, meta={'title':title,'news_url':news_url,'summary':summary,'picture':picture}, callback=self.parse_detail)

    def parse_detail(self, response):
        news_item=SrtpprojectItem()
        soup = BeautifulSoup(response.text, "lxml") 
        news_item['title']=response.meta['title']
        news_item['summary']=response.meta['summary']
        news_item['picture']=response.meta['picture']
        news_item['news_url']=response.meta['news_url']
        news_item['content']=soup.find('h1',class_='con_title').string+u'测试'
        print news_item['content']
        return news_item
