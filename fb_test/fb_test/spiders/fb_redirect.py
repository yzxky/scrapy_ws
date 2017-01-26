#!/usr/bin/python
#-*- coding: utf-8 -*-

import scrapy
import parsel
import sys

from urlparse import urljoin

#from scarpy import Item, Field
#from scrapy.http import Request

class LoginSpider(scrapy.Spider):
    name = 'fb_url'
    url_base = "https://www.facebook.com/"
    start_urls = []    
    end_urls = []
    download_delay = 0.5
    usr = '' #email
    pwd = '' #password

    def __init__(self, category=None, *args, **kwargs):
        super(LoginSpider, self).__init__(*args, **kwargs)
        self.read_urls("list1.txt")

    def start_requests(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')        
        return [scrapy.Request('https://www.facebook.com/login.php', meta = {'cookiejar' : 1}, callback = self.post_login)]

    def post_login(self, response):
        print 'Preparing login'
        lsd = scrapy.Selector(response).xpath('//input[@name="lsd"]/@value').extract_first()
        print lsd
        lgnrnd = scrapy.Selector(response).xpath('//input[@name="lgnrnd"]/@value').extract_first()
        print lgnrnd
        return scrapy.FormRequest.from_response(
            response,
            meta = {'cookiejar' : response.meta['cookiejar']},
            formdata = {
                'lsd': lsd, 
                'email':self.usr, 
                'pass':self.pwd,
                'lgnrnd':lgnrnd},
            callback = self.after_login
        )

    def after_login(self, response):
        for url in self.start_urls:
            print url
            yield scrapy.Request(url, 
                meta = {'cookiejar' : response.meta['cookiejar'], 'url_old' : url},
                callback = self.parse_comment)
        return

    def parse_comment(self, response):
        str1 = response.selector.xpath('//meta[@http-equiv="refresh"]/@content').extract_first()        
        abbrv = str1.split('/')[1:]
        url_new = urljoin(self.url_base, ''.join(abbrv))
        self.end_urls.append(url_new)
        print(url_new)
        f = open('list_new.txt', 'a')
        f.write('{' + response.meta['url_old'] + '}, {' + url_new + '}\n')
        f.close()
        f = open('list_new_pure', 'a')
        f.write(url_new + '\n')
        f.close()
        return

    def read_urls(self, filename):
        f = open(filename)
        for line in f:
            self.start_urls.append(urljoin(self.url_base,line[0:-1]))
        f.close()
        




