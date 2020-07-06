#!/usr/bin/python3  
# -*- coding: utf-8 -*- 
import requests
from lxml import etree
import os
import time

def steal_library_header(url):
    print('\n正在尝试通过', url, '的5秒检测...')
    for retry in range(10):
        try:
            cookie_value, user_agent = get_cookie_string(url, timeout=15)
            print('通过5秒检测！\n')
            return {'User-Agent': user_agent, 'Cookie': cookie_value}
        except:
            print('通过失败，重新尝试...')
            continue
    print('>>无法通过javlibrary的5秒检测：', url)
    print('-'*20)


def get_html_by_requests(header,url, xpath_):
    try:
        html = requests.get(url,headers=header)
    except Exception as e:
        print('无法按时打开网页，五秒后重试。')
        time.sleep(5)
        html, html_xpath = get_html_by_requests(header,url, xpath_)

    # print(url)
    # print(html)
    if html.status_code == 200:
        html = html.text
        if '暫無內容' in html:
            time.sleep(1)
            html_xpath = etree.HTML(html)
            return html, html_xpath
        if 'javdb' not in html:
            print('html中找不到javdb，五秒后重试。')
            time.sleep(5)
            html, html_xpath = get_html_by_requests(header,url, xpath_)
        if html == '':
            print('html为空，五秒后重试。')
            time.sleep(5)
            html, html_xpath = get_html_by_requests(header,url, xpath_)
        html_xpath = etree.HTML(html)
        if html_xpath.xpath(xpath_) is None:
            print('html_xpath为空，五秒后重试。')
            time.sleep(5)
            html, html_xpath = get_html_by_requests(header,url, xpath_)
        time.sleep(2)
    else:
        print('无法按时打开网页，五秒后重试。')
        time.sleep(5)
        html, html_xpath = get_html_by_requests(header,url, xpath_)
    return html, html_xpath

if __name__ == '__main__':
    url = 'https://javdb4.com'
    xpath_ = '//*[@id="magnets-content"]'
    header = steal_library_header(url=url)
    html, html_xpath = get_html_by_requests(header,url, xpath_)
    print(html)