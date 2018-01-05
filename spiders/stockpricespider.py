# -*- coding:utf-8 -*-
import re
import json
import urllib2

import requests
from bs4 import BeautifulSoup
import csv, codecs
import datetime
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

header = {"Accept": "text/html,application/xhtml+xml,application/xml;",
          "Accept-Encoding": "gzip, deflate",
          "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
          "Referer": "http://www.taikoohui.com/zh-CN/Shopping",
          "Content-Type": "application/json; charset=utf-8",
          "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
          }

print (datetime.datetime(1983, 1, 1, 12, 0, 0) - datetime.datetime.now()).days / 20


def get_content_by_url(url):
    try:
        req = urllib2.Request(url)
        source_code = urllib2.urlopen(req, timeout=10).read()
        plain_text = unicode(source_code)
        soup = BeautifulSoup(plain_text, "html.parser")
        return soup
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e
        exit(-1)
    except Exception, e:
        print e
        exit(-1)


out = codecs.open('stockPrice.csv', 'a', 'utf_8_sig')
csv_write = csv.writer(out, dialect='excel')

for i in range(1, 442):
    url = "https://info.finance.yahoo.co.jp/history/?code=4540.T&sy=1983&sm=1&sd=1&ey=2018&em=1&ed=5&tm=d&p=" + str(i)
    soup = get_content_by_url(url)
    table = soup.find('table', class_="boardFin yjSt marB6")
    tr_list = table.find_all('tr')
    for tr in tr_list:
        if len(tr.find_all('td')) != 0:
            td_list = tr.find_all('td')
            content = []
            for td in td_list:
                content.append(td.text)
                print "Text: " + td.text
            csv_write.writerow(content)
        else:
            print "excute " + str(i) + "page~"
out.close()
