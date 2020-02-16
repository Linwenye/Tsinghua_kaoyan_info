import socket
from urllib import request
import traceback
import logging
import time
from bs4 import BeautifulSoup
from mail import send_mail
from dbhelper import insert_db, exists


def inner_page_read(myurl, f_log):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    }
    socket.setdefaulttimeout(20)

    my_request = request.Request(myurl, None, headers)
    html = None
    soup = None
    try:
        html = request.urlopen(my_request, timeout=10)
    except Exception as e:
        logging.error(traceback.format_exc())
        print("can't open")
    try:
        html = html.read()
        soup = BeautifulSoup(html, "lxml")
    except Exception as e:
        logging.error(traceback.format_exc())
        f_log.write(myurl + ": can't open imdb\n")
        return
    return soup


def page_read(myurl, f_log):
    i = 0
    soup = inner_page_read(myurl, f_log)
    while not soup and i < 5:
        i += 1
        print(myurl + 'try open again')
        soup = inner_page_read(myurl, f_log)
    return soup


def inner_page_read_nolog(myurl):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    }
    socket.setdefaulttimeout(10)

    my_request = request.Request(myurl, None, headers)
    html = None
    soup = None
    try:
        html = request.urlopen(my_request, timeout=10)
    except Exception as e:
        logging.error(traceback.format_exc())
    try:
        html = html.read()
        soup = BeautifulSoup(html, "lxml")
    except Exception as e:
        logging.error(traceback.format_exc())
        print(myurl + ": can't open imdb\n")
        return
    return soup


def page_read_nolog(myurl):
    i = 0
    soup = inner_page_read_nolog(myurl)
    while not soup and i < 5:
        i += 1
        print(myurl + 'try open again')
        soup = inner_page_read_nolog(myurl)
    return soup


def page_read_power(myurl):
    soup = inner_page_read_nolog(myurl)
    while not soup:
        print(myurl + 'try open again')
        soup = inner_page_read_nolog(myurl)
    return soup


def getitem(url):
    soup = page_read_nolog(url)
    lines = soup.select('.bs_infor')[0].select('.infor_t')
    itemlist = [(line.a['title'], line.select('.t')[0].text, line.a['href']) for line in lines]
    return itemlist


if __name__ == '__main__':
    itemlist = getitem('http://yz.tsinghua.edu.cn/publish/yjszs/8549/index.html')
    itemlist += getitem('http://yz.tsinghua.edu.cn/publish/yjszs/8550/index.html')
    to_insert = []
    for item in itemlist:
        if item not in exists:
            to_insert.append(item)
    if to_insert:
        print(to_insert)
        send_mail(to_insert)
        insert_db(to_insert)
