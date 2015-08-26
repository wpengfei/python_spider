# -*- coding:utf-8 -*-
import urllib
import urllib2
import re


class qb_spider:
    def __init__(self):
        self.pageNum = 1
        self.url = 'http://www.qiushibaike.com/text/page'
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': user_agent}
        self.pageContent = None
        str = '<div class="author">.*?<a .*?>.*?<img .*?/>\n(.*?)\n</a>.*?</div>.*?<div class="content">(.*?)<!(.*?)>.*?</div>.*?<i class="number">(.*?)</i>'
        self.pattern = re.compile(str, re.S)

    def get_page(self,pageNum):
        try:
            request = urllib2.Request(self.url + str(pageNum), headers=self.headers)
            response = urllib2.urlopen(request)
            self.pageContent = response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason

    def get_items(self):
        items = re.findall(self.pattern, self.pageContent)
        print items.__len__()
        for item in items:
            print '\n\n', item[1], '\n author:', item[0], 'time:', item[2], 'likes:',item[3]

    def start(self):
        print'press "q" to exit, or any key to continue...'
        self.get_page(self.pageNum)
        self.get_items()
        self.pageNum += 1
        while 1:
            if raw_input() == 'q':
                break
            else:
                self.get_page(self.pageNum)
                self.get_items()
                self.pageNum += 1


myspider = qb_spider()
myspider.start()