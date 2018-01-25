#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from scrapy.selector import Selector
import MySQLdb

conn = MySQLdb.connect(host="127.0.0.1",user="root",passwd="1234",db="mysql_test_01",charset='utf8')
cursor = conn.cursor()

user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"

headers = {
    'User-Agent': user_agent
}


def crawl_ip(url,headers):
    reg = requests.get(url,headers=headers)
    response = Selector(text=reg.text)
    list_all = []
    a = []
    html = response.css("#ip_list tr")
    trs = html.css('tr')

    for meg in trs:

        speeder = meg.xpath("//div")
        speeders = speeder.css('::attr(title)').extract()
        a.append(speeders)
        title = meg.css("td::text").extract()

        if title:
            if title[5]=='HTTP' or title[5]=='HTTPS':
                p = title[5]
            else:
                p = ''

            list_all.append((title[0],title[1],p))


    for i in list_all:
        cursor.execute(
            """INSERT INTO text_02(ip, port, proxy_type) VALUES ('{0}','{1}','{2}')""".format(i[0],i[1],i[2])
        )
        conn.commit()

if __name__ == '__main__':
    for i in range(100):
        url = "http://www.xicidaili.com/nn/{0}".format(i)
        crawl_ip(url,headers)

    conn.close()


