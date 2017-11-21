# -*- coding:utf-8 -*-
import re
import json
import requests
from bs4 import BeautifulSoup
import csv, codecs
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# set cookie to make sure get chinese page
cookie = "bbbbbbbbbbbbbbb=JMHBPIBLIHFCDLJPBMFBPDNCEMONFEEJAPOLDKFDDCODJOBFJCNIEGNANFEAMAGJMKFEKBHPFDJCDLPLNBNCCHEDPLFDICAMMHDNEEDMCPLLCEMOOJGBDNHOHHMFHGFH; tkh#lang=zh-CN; ASP.NET_SessionId=fg2poi2kksejcnzvote3isqc; bbbbbbbbbbbbbbb=MCBLBDNGJBKKJHCAFLEMOOPBJBEMOEHDPGMHJLCFNEIDFBHIMBGHGGAMLBFAFDFNJCHABCNPAHGKONLHBBIAJIIGMOMIFOOPMAABGDLCNLOICNJMPOBKHJOADBBHPDCK; SC_ANALYTICS_GLOBAL_COOKIE=2dcfb33135444c049490bc74d6538474|False; _ga=GA1.2.1927393436.1511265335; _gid=GA1.2.1176506950.1511265335; sc_expview=0; Hm_lvt_6a4eb147fb4178d3487ad8d5aacb2e49=1511265335; Hm_lpvt_6a4eb147fb4178d3487ad8d5aacb2e49=1511267615"

header = {"Accept": "text/html,application/xhtml+xml,application/xml;",
          "Accept-Encoding": "gzip, deflate",
          "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
          "Referer": "http://www.taikoohui.com/zh-CN/Shopping",
          "Content-Type": "application/json; charset=utf-8",
          "Cookie": cookie,
          "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
          }
# total page number is 26
for i in range(1, 27):
    url = "http://www.taikoohui.com/files/taikoohui/ajax/AjaxShopping.ashx?method=getData&itemPath=%2Fsitecore%2Fcontent%2FHome%2FTaikooHui%2FShopping&pageIndex=" \
          + str(i) + "&firstQueryConditions=Brand&secondQueryConditions=All&isMobile=1"
    cont = requests.get(url, headers=header).content
    con = json.loads(cont, 'utf-8')
    html = con['storeList']
    soup = BeautifulSoup(html, "html.parser")
    span_list = soup.find_all('span')
    out = codecs.open('shopinfo.csv', 'a', 'utf_8_sig')
    csv_write = csv.writer(out, dialect='excel')
    content = []
    length = len(span_list)
    # write the related information into csv file
    for index in range(0, length):
        if index % 5 <= 1:
            if index % 5 == 0:
                content.append(span_list[index].find('a').text.split(' ')[0])
            else:
                content.append(span_list[index].find('a').text)
        else:
            if index % 5 == 4:
                content.append(span_list[index].text)
                csv_write.writerow(content)
                content = []
            else:
                content.append(span_list[index].text)
    out.close()
