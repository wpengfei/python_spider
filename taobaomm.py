__author__ = 'wpf'
# -*- coding:utf-8 -*-

import urllib
import urllib2
import tool
import re
import os
import time
import cookielib

class Spider:

    def __init__(self):
        self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': user_agent, 'Referer':'http://mm.taobao.com'}
        self.tool = tool.Tool()
        self.t1 = 0
        self.t2 = 60

    def getPage(self,pageIndex):
        url = self.siteURL + "?page=" + str(pageIndex)
        print 'whole url = ', url
        request = urllib2.Request(url, headers=self.headers)
        response = urllib2.urlopen(request)
        #print response.read().decode('gbk')
        return response.read().decode('gbk')

    def getContents(self,pageIndex):
        page = self.getPage(pageIndex)
        str = '<div class="list-item">.*?"pic-word".*?<a href="(.*?)".*?<img src="(.*?)".*?</a>.*?"lady-name".*?_blank.*?>(.*?)</a>'
        str2 = '.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>.*?<em>(.*?)</em>.*?</div>.*?"pic w610".*?<a href="(.*?)".*?>'
        pattern = re.compile(str + str2, re.S)
        items = re.findall(pattern,page)
        for item in items:
            print item[0],item[1],item[2],item[3],item[4],item[5],item[6]#,item[7]
        return items


    #获取MM个人详情页面
    def getPersonalPage(self,infoURL):
        request = urllib2.Request(infoURL, headers=self.headers)
        response = urllib2.urlopen(request)
        return response.read().decode('gbk')

    #获取个人文字简介
    def getBrief(self,page):
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        result = re.search(pattern,page)
        print "个人文字简介====================" ,result
        return self.tool.replace(result.group(1))

    def saveBrief(self,content,name):
        fileName = name + "/" + name + ".txt"
        f = open(fileName,"w+")
        print u"正在偷偷保存她的个人信息为",fileName
        f.write(content.encode('utf-8'))

     #获取页面所有图片
    def getAllImg(self,page):
        str = '//gtd.alicdn.com/imgextra/(.*?)_620x10000'
        patternImg = re.compile(str,re.S)
        images = re.findall(patternImg, page)
        for i in images:
            print 'images ====:', i
        return images

    #传入图片地址，文件名，保存单张图片
    def saveImg(self,imageURL,fileName):
        request = urllib2.Request(imageURL, headers=self.headers)
        u = urllib2.urlopen(request)
        #u = urllib.urlopen(imageURL)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        f.close()


    #保存多张写真图片
    def saveImgs(self,images,name):
        number = 1
        print name, "共有",len(images),"张照片"
        for imageURL in images:
            time.sleep(self.t1)
            splitPath = imageURL.split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = "jpg"
            fileName = name + "/" + str(number) + "." + fTail
            print '保存图片...',fileName
            self.saveImg(imageURL,fileName)
            number += 1
        print name, '照片保存完毕'
    # 保存头像
    def saveIcon(self,iconURL,name):
        splitPath = iconURL.split('.')
        fTail = splitPath.pop()
        fileName = name + "/icon." + fTail
        self.saveImg(iconURL,fileName)
        print name, '头像保存完毕'

    def mkdir(self,path):
        path = path.strip()
        isExists=os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            return True
        else:
            return False
    #将一页淘宝MM的信息保存起来
    def savePageInfo(self,pageIndex):

        contents = self.getContents(pageIndex)
        for item in contents:
            time.sleep(self.t2)
            #item[0]个人主页URL,item[1]头像URL,item[2]姓名,item[3]年龄,item[4]居住地,item[5]职业，item[6]个性域名
            print "发现一位MM,名字叫",item[2],"年龄:",item[3],",位置:",item[4], "职业:", item[5]
            print "她的个人地址是",item[6]
            #个人详情页面的URL
            personalURL = 'http:' +item[6]
            iconURL = 'http:' + item[1]
            personalPage = self.getPersonalPage(personalURL)
            images = self.getAllImg(personalPage)
            if self.mkdir(item[2]):
                print '创建目录成功'
                self.saveIcon(iconURL,item[2])
                self.saveImgs(images,item[2])
            else:
                print '目录已经存在'

            #获取个人简介
            #brief = self.getBrief(detailPage)
            #保存个人简介
            #self.saveBrief(brief,item[3])


    def main(self,start,end):
        print '处理范围：第%d页 - 第%d页' %(start, end)
        for page in range(start,end+1):
            print '正在处理第%d页...' %(page)
            self.savePageInfo(page)

spider = Spider()
#spider.getContents(1)
spider.main(1,10)

