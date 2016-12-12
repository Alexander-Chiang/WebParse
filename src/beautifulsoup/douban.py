'''
Created on 2016-12-12

@author: Sawatari
'''

from bs4 import BeautifulSoup
import requests
import time

''' 本地
with open("C:/Users/Sawatari/Desktop/豆瓣读书.html", 'r', encoding='utf-8') as wb_data:
    Soup = BeautifulSoup(wb_data, 'lxml')
    images = Soup.select('#content > div > div.article > div.section.popular-books > div.bd > ul > li > div.cover > a > img')
    authors = Soup.select('#content > div > div.article > div.section.popular-books > div.bd > ul > li > div.info > p.author')
    scores = Soup.select('#content > div > div.article > div.section.popular-books > div.bd > ul > li > div.info > p.entry-star-small > span.average-rating')
#    print(images, authors, scores, sep='\n------------------------\n')
'''

url = 'https://book.douban.com/top250'
urls = ['https://book.douban.com/top250?start={}'.format(str(i)) for i in range(0, 150, 25)]
headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
        'Cookie':'ll="108288"; bid=5kIixMwX4eA; gr_user_id=0d0042d6-3180-4429-8297-fa794562f288; gr_cs1_5b706ed5-3913-45da-9261-34a8c440445d=user_id%3A0; ps=y; dbcl2="154949417:YGiHfoCW3Cw"; ck=3Z-H; __utmt_douban=1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=c3e9f862-0ab3-4671-a533-8c7f2ee2bb64; gr_cs1_c3e9f862-0ab3-4671-a533-8c7f2ee2bb64=user_id%3A1; ap=1; _vwo_uuid_v2=CAB018BF0B80BAA0D726ECDA308CDABB|4bc5421e64b4787a4495f1846bf84b91; push_noty_num=0; push_doumail_num=0; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1481525065%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DIFWhCDnoh_5jHm2RNdyPPGXUW2W0NNySnvlSrv52hkiNDfpUJgYmcMRdNMXdrVxRgz2PXC391D3uHb-ZQT8Lza%26wd%3D%26eqid%3D8fd42892000595d300000003584ace8b%22%5D; _pk_id.100001.8cb4=b57a12f43932644a.1480348431.5.1481525065.1481297557.; _pk_ses.100001.8cb4=*; __utmt=1; __utma=30149280.605662500.1479551835.1481521153.1481525025.8; __utmb=30149280.9.9.1481525065077; __utmc=30149280; __utmz=30149280.1481525025.8.6.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/phone/bind; __utmv=30149280.15494'
    }
url_save = 'https://www.douban.com/people/154949417/'

def get_books(url, data=None):
    info = []
    wb_data = requests.get(url)
    time.sleep(2)
    Soup = BeautifulSoup(wb_data.text, 'lxml')
    # except tbody
    names = Soup.select(
        '#content > div > div.article > div > table > tr > td:nth-of-type(2) > div.pl2 > a')
    images = Soup.select(
        '#content > div > div.article > div > table > tr > td:nth-of-type(1) > a > img')
    authors = Soup.select(
        '#content > div > div.article > div > table > tr > td:nth-of-type(2) > p.pl')
    scores = Soup.select(
        '#content > div > div.article > div > table > tr > td:nth-of-type(2) > div.star.clearfix > span.rating_nums')
    for name, image, author, score in zip(names, images, authors, scores):
        data = {
            'name': name.get('title'),
            'image': image.get('src'),
            'detail': author.get_text(),
            'score': score.get_text(),
        }
        info.append(data)
    # print(data)

    # sifting
    for i in info:
        if float(i['score']) > 8.5:
            print('书名：' + i['name'], '封面：' + i['image'], '详细信息：' + i['detail'], '评分：' + i['score'])

def get_fav(headers, url_save, data=None):
    wb_data = requests.get(url_save, headers=headers)
    Soup = BeautifulSoup(wb_data.text, 'lxml')
    names = Soup.select('#book > div > ul > li > a > img')
    images = Soup.select('#book > div > ul > li > a > img')

    #for must have two or more data
    for name, image in zip(names, images):
        data = {
            'title': name.get('alt'),
            'img': image.get('src')
        }
        print(data)

# get_books(url)
for single_url in urls:
    get_books(single_url)