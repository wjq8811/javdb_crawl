#!/usr/bin/python3  
# -*- coding: utf-8 -*- 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import requests
from lxml import etree
import os
import time

def i_am_robot(browser, main_url):
    browser.get(main_url)
    try:
        WebDriverWait(browser, 20).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div[2]/footer/a[1]')))
    except Exception as e:
        print('无法正确打开首页，10秒后重试。')
        # browser.close()
        time.sleep(10)
        i_am_robot(browser, main_url)
    else:
        browser.find_elements_by_xpath(
            "/html/body/div[1]/div[2]/footer/a[1]")[0].click()
        main_html_source = browser.page_source
        browser.execute_script("window.stop();")
        print('已正确打开首页。')
        print('-' * 20)
        time.sleep(5)

def get_html(browser, url, xpath_):
    wait = WebDriverWait(browser, 10)  # 等待的最大时间20s
    browser.get(url)
    html = ''
    try:
        WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath_)))
    except Exception as e:
        print('无法按时打开网页，五秒后重试。')
        # browser.close()
        time.sleep(5)
        get_html(browser, url, xpath_)
    else:
        browser.execute_script("window.stop();")
        html = browser.page_source

    if '暫無內容' in html:
        time.sleep(2)
        html_xpath = etree.HTML(html)
        return html, html_xpath
    if 'javdb' not in html:
        print('html中找不到javdb，五秒后重试。')
        time.sleep(5)
        html, html_xpath = get_html(browser, url, xpath_)
    if html == '':
        print('html为空，五秒后重试。')
        time.sleep(5)
        html, html_xpath = get_html(browser, url, xpath_)
    html_xpath = etree.HTML(html)
    if html_xpath.xpath(xpath_) is None:
        print('html_xpath为空，五秒后重试。')
        time.sleep(5)
        html, html_xpath = get_html(browser, url, xpath_)
    time.sleep(2)
    return html, html_xpath


if __name__ == '__main__':
    main()