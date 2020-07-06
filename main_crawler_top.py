#!/usr/bin/python3  
# -*- coding: utf-8 -*- 

# from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
from lxml import etree
import os
import time
import json
import file_io,my_selenium,crawler_function


def function(file_path,browser,top_url,main_url):
    #爬取top页面，保存url
    work_list_path = file_path + '\\' + 'work_list.txt'
    work_list = crawler_function.crawler_top_works(browser,top_url,main_url)
    file_io.write_all_lines(work_list_path, work_list)

    #读取url，爬取页面
    work_list = file_io.read_all_lines(work_list_path)
    crawler_function.crawler_top_work(browser, main_url,work_list,file_path)



def main(main_url, file_path):
    # 定义浏览器，不加载图片，跳过认证
    # options = webdriver.ChromeOptions()
    # prefs = {
        # 'profile.default_content_setting_values': {
            # 'images': 2
        # }
    # }
    # options.add_experimental_option('prefs', prefs)
    #设置代理，不需要的可以注释掉
    #options.add_argument('--proxy-server=http://192.168.2.1:1282') 
    # capa = DesiredCapabilities.CHROME
    # capa["pageLoadStrategy"] = "none" #懒加载模式，不等待页面加载完毕
    # browser = webdriver.Chrome(chrome_options=options,desired_capabilities=capa)
    #跳过验证
    # my_selenium.i_am_robot(browser, main_url)


    #爬取youma_top
    youma_top_url = 'https://javdb4.com/rankings/video_daily'
    youma_file_path = file_path + '\\' + 'youma'
    function(youma_file_path,browser,youma_top_url,main_url)
    #爬取wuma_top
    wuma_top_url = 'https://javdb4.com/rankings/video_uncensored?period=daily'
    wuma_file_path = file_path + '\\' + 'wuma'
    function(wuma_file_path,browser,wuma_top_url,main_url)
    #爬取oumei_top
    oumei_top_url = 'https://javdb4.com/rankings/video_western?period=daily'
    oumei_file_path = file_path + '\\' + 'oumei'
    function(oumei_file_path,browser,oumei_top_url,main_url)
    #爬取FC2_top
    FC2_top_url = 'https://javdb4.com/rankings/video_fc2?period=daily'
    FC2_file_path = file_path + '\\' + 'FC2'
    function(FC2_file_path,browser,FC2_top_url,main_url)





if __name__ == '__main__':
    main_url = 'https://javdb4.com'
    file_path = r'file\\top'
    main(main_url, file_path)

