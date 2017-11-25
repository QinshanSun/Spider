# -*- coding:utf-8 -*-
import re
import json
import requests
from bs4 import BeautifulSoup
import csv
import codecs
import urllib2
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

basic_url = 'http://hk.centadata.com/TransactionHistory.aspx?type=3&code=OVDUURFSRJ&info=basicinfo'
home_url = 'http://hk.centadata.com/'


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


def get_house_info_url(url, content):
    post_url = home_url + url
    soup = get_content_by_url(post_url)
    table = soup.find("table", class_="table1")
    tr_list = table.find_all("tr")
    for tr in tr_list:
        td_list = tr.find_all("td")
        print td_list[0].string
        if td_list[1].find("a") is not None:
            print td_list[1].find("a").string
            content.append(remove_space_and_line_break_in_string(td_list[1].find("a").string))
        else:
            print td_list[1].string
            content.append(remove_space_and_line_break_in_string(td_list[1].string))
    return content


def remove_space_and_line_break_in_string(string):
    if string is not None:
        return string.replace(' ', '').replace('\r\n', '')
    else:
        return ""


def get_basic_info_by_basic_url():
    soup = get_content_by_url(basic_url)
    table = soup.find("table", class_="unitTran-left-a")
    td_list = table.find_all("td")
    for td in td_list:
        if td.find("a") is not None:
            td_url = td.find("a")
            print td_url["href"]
            td_name = td.find("div")
            if td_name is not None:
                print td_name.string
                column2 = remove_space_and_line_break_in_string(td_name.string)
            out = codecs.open('houseInfo.csv', 'a', 'utf_8_sig')
            csv_write = csv.writer(out, dialect='excel')
            content = []
            content.append(column1)
            content.append(column2)
            get_house_info_url(td_url["href"], content)
            csv_write.writerow(content)
        else:
            td_name = td.find("div")
            if td_name is not None:
                print td_name.string
                column1 = remove_space_and_line_break_in_string(td_name.string)
    out.close()


def get_detailed_info_by_basic_url():
    soup = get_content_by_url(basic_url)
    table = soup.find("table", class_="unitTran-left-a")
    td_list = table.find_all("td")
    for td in td_list:
        if td.find("a") is not None:
            td_url = td.find("a")
            print td_url["href"]
            td_name = td.find("div")
            if td_name is not None:
                print td_name.string
            get_house_info_by_house_url(td_url["href"],td_name.string)


def get_house_info_by_house_url(url, name):
    post_url = home_url + url
    soup = get_content_by_url(post_url)
    out = codecs.open(name+'.csv', 'a', 'utf_8_sig')
    csv_write = csv.writer(out, dialect='excel')

    table = soup.find(id="unitTran-main-table")
    tr_list = table.find_all("tr")
    # first row
    td_list = tr_list[0].find_all("td", class_="unitTran-main-table-td")
    sub_table_list = tr_list[1].find_all("table", class_="unitTran-sub-table")

    for i in range(0, len(td_list)):
        tr_list = sub_table_list[i].find_all("tr")
        for tr in tr_list:
            if tr.find_all("td") is not None:
                content = []
                content.append(remove_space_and_line_break_in_string(td_list[i].find("b").string))
                data_td_list = tr.find_all("td")
                for data_td in data_td_list:
                    if data_td.find("span") is None:
                        if data_td.find("input") is not None:
                            print remove_space_and_line_break_in_string(data_td.text)
                            content.append(remove_space_and_line_break_in_string(data_td.text))
                        else:
                            print remove_space_and_line_break_in_string(data_td.string)
                            content.append(remove_space_and_line_break_in_string(data_td.string))
                    else:
                        attrs = data_td.find("span").attrs
                        if attrs.get("class") is not None:
                            if attrs.get("class") == "up":
                                print remove_space_and_line_break_in_string(str("+")+data_td.find("span").string)
                                content.append(remove_space_and_line_break_in_string(str("+")+data_td.find("span").string))
                            else:
                                print remove_space_and_line_break_in_string(str("-")+data_td.find("span").string)
                                content.append(remove_space_and_line_break_in_string(str("-") + data_td.find("span").string))
                        else:
                            content.append(
                                remove_space_and_line_break_in_string(data_td.find("span").string))
                csv_write.writerow(content)
    out.close()

get_detailed_info_by_basic_url()
