#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import MySQLdb
import time
from scrapy import Selector
from utils.common import get_md5




user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"

headers = {
    'User-Agent': user_agent
}


def crawl_ip(url):
    response = requests.get(url,headers=headers)
    a = []
    d = []
    responses = Selector(text=response.text)
    all_node = responses.css('#ip_list tr')
    for i in all_node:
        l = i.css('td::text').extract()
        b = len(l)
        if b != 0:
            a.append((l[0], l[1], l[5]))
        h = i.css('.bar::attr(title)').extract()
        c = len(h)
        if c != 0:
            d.append((h[0].replace('秒', '')))
    return a,d


def mysql_store(a,d):
    print(type(a),type(d))
    pass
    conn = MySQLdb.connect(host="127.0.0.1",user="root",passwd="1234",db="mysql_test_01",charset='utf8')
    cursor = conn.cursor()

    for i in range(100):
        cursor.execute(
            """INSERT INTO text_02(ip, port, proxy_type,ip_haxi,speed) VALUES ('{0}','{1}','{2}','{3}','{4}')""".format(a[i][0],a[i][1],a[i][2],get_md5(a[i][0]+a[i][1]+str(time.time())+a[i][2]),d[i])
        )
        conn.commit()
    conn.close()


if __name__ == '__main__':

    for i in range(1999):
        url = "http://www.xicidaili.com/nn/{0}".format(i+1)
        q,h = crawl_ip(url)
        mysql_store(q,h)











