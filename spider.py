# coding=utf-8
import urllib
import urllib2
import cookielib
import re
from bs4 import BeautifulSoup

def save_cookie():
    print 'func--create_cookie()'
    # 声明一个CookieJar对象实例来保存cookie
    cookie = cookielib.CookieJar()
    # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
    handler = urllib2.HTTPCookieProcessor(cookie)
    # 通过handler来构建opener
    opener = urllib2.build_opener(handler)
    # 此处的open方法同urllib2的urlopen方法，也可以传入request
    response = opener.open('http://www.baidu.com')
    for item in cookie:
        print 'Name = ' + item.name
        print 'Value = ' + item.value

def save_cookie_to_file():
    #设置保存cookie的文件，同级目录下的cookie.txt
    filename = 'cookie.txt'
    #声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
    cookie = cookielib.MozillaCookieJar(filename)
    #利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
    handler = urllib2.HTTPCookieProcessor(cookie)
    #通过handler来构建opener
    opener = urllib2.build_opener(handler)
    #创建一个请求，原理同urllib2的urlopen
    response = opener.open("http://www.baidu.com")
    #保存cookie到文件
    cookie.save(ignore_discard=True, ignore_expires=True)
    print 'save cookie to file finished!'

def load_cookie_from_file():
    #创建MozillaCookieJar实例对象
    cookie = cookielib.MozillaCookieJar()
    #从文件中读取cookie内容到变量
    cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
    #创建请求的request
    req = urllib2.Request("http://www.baidu.com")
    #利用urllib2的build_opener方法创建一个opener
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    response = opener.open(req)
    print response.read()
    print 'load cookie from file finished'

def set_proxy():
    enable_proxy = True
    proxy_handler = urllib2.ProxyHandler({"http" : 'http://some-proxy.com:8080'})
    null_proxy_handler = urllib2.ProxyHandler({})
    if enable_proxy:
        opener = urllib2.build_opener(proxy_handler)
    else:
        opener = urllib2.build_opener(null_proxy_handler)
    urllib2.install_opener(opener)

def cookie_test():
    print 'cookie test'
    filename = 'cookie.txt'
    #声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
    cookie = cookielib.MozillaCookieJar(filename)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    postdata = urllib.urlencode({
               'username':'allwithwinds',
               'password':'4202065'
           })
    #登录教务系统的URL
    loginUrl = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
    #模拟登录，并把cookie保存到变量
    result = opener.open(loginUrl,postdata)
    print 'first open', result.read()
    #保存cookie到cookie.txt中
    cookie.save(ignore_discard=True, ignore_expires=True)
    #利用cookie请求访问另一个网址，
    print 'use cookie==================================================================================='
    gradeUrl = 'https://passport.csdn.net/account/login?from=http://my.csdn.net/my/fans'
    #请求访问成绩查询网址
    result = opener.open(gradeUrl)
    print result.read()

def test():
    # Debug log
    httpHandler = urllib2.HTTPHandler(debuglevel=1)
    httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
    opener = urllib2.build_opener(httpHandler, httpsHandler)
    urllib2.install_opener(opener)

    values = {"username": "allwithwinds", "password": "4202065"}
    data = urllib.urlencode(values)

    url = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"

    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent, 'Referer': 'http://www.zhihu.com/articles'}

    request = urllib2.Request(url, data, headers)

    try:
        response = urllib2.urlopen('http://blog.csdn.net/cqcre')
        # response = urllib2.urlopen(request, timeout = 10)
        print response.read()
    except urllib2.HTTPError, e:
        if hasattr(e, "code"):
            print e.code
    except urllib2.URLError, e:
        if hasattr(e, "reason"):
            print e.reason
    else:
        print "ok"

def match_string():
    pattern = re.compile(r'hello')
    result1 = re.match(pattern,'hello')
    result2 = re.match(pattern,'helloo CQC!')
    result3 = re.match(pattern,'helo CQC!')
    result4 = re.match(pattern,'hello CQC!')
    #如果1匹配成功
    if result1:
        # 使用Match获得分组信息
        print result1.group()
    else:
        print '1匹配失败！'

    #如果2匹配成功
    if result2:
        # 使用Match获得分组信息
        print result2.group()
    else:
        print '2匹配失败！'

    #如果3匹配成功
    if result3:
        # 使用Match获得分组信息
        print result3.group()
    else:
        print '3匹配失败！'

    #如果4匹配成功
    if result4:
        # 使用Match获得分组信息
        print result4.group()
    else:
        print '4匹配失败！'

def beautiful_soup():
    print'bs'
    html = """
    <html><head><title>The Dormouse's story</title></head>
    <body>
    <p class="title" name="dromouse"><b>The Dormouse's story</b></p>
    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>
    <p class="story">...</p>
    """

    soup = BeautifulSoup(html)
    #print soup.prettify()
    print soup.title
    print soup.head
    print soup.a
    print soup.b
    print soup.p.string
#save_cookie()
#save_cookie_to_file()
#load_cookie_from_file()
#cookie_test()
#match_string()
beautiful_soup()