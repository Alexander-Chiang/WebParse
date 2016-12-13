'''
Created on 2016-12-13

@author: Sawatari
'''

import re
import time
import urllib

def getHtml(url):
    time.sleep(2)
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getImg(html):
    reg = r'url="(.+?\.jpg)"'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    x = 0
    for imgurl in imglist:
        time.sleep(2)
        urllib.urlretrieve(imgurl, '%s.jpg' % x)
        x += 1

urls = ['http://sj.enterdesk.com/tag-%E4%B8%AA%E6%80%A7/{}.html'.format(str(i)) for i in range(1, 4)]

for single_url in urls:
    html = getHtml(single_url)
    print getImg(html)