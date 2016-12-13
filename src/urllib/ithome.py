#-*- coding:utf-8 -*-
'''
Created on 2016-12-13

@author: Sawatari
'''

import re
import sys
import time
import urllib2

def write_to_file(str):
    f = open('forum.txt', 'a')
    f.write(str + '\n')
    f.close()

def get_posts(url):
    time.sleep(2)
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
    headers = {'User-Agent': user_agent}
    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req)
    the_page = response.read().decode('utf-8').encode(sys.getfilesystemencoding())
    reg = r'<a target="_blank" href=".*?" class="t_cate_title">(.*?)</a>'
    postre = re.compile(reg, re.S)
    postlist = re.findall(postre, the_page)
    # 直接输出list不会以gbk编码输出
    for post in postlist:
        write_to_file(post)


urls = ['http://quan.ithome.com/talk/{}/'.format(str(i)) for i in range(1, 4)]
for single_url in urls:
    get_posts(single_url)