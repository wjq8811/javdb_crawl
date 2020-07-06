#!/usr/bin/python3  
# -*- coding: utf-8 -*- 

# from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from lxml import etree
import os
import time
import json
import file_io,my_selenium,crawler_function

def function(browser,main_url,actor_url,file_path):
    work_list = crawler_function.crawler_actro_works(browser, main_url,actor_url)
    actor_name = work_list[0].split('|')[0]
    work_list_path = file_path + '\\' + actor_name + '_work_list.txt'
    file_io.write_all_lines(work_list_path, work_list)
    #读取本地所有作品地址并保存
    work_list = file_io.read_all_lines(work_list_path)
    crawler_function.crawler_work(browser, main_url,work_list,file_path)


def main(main_url,actor_url,file_path):
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

    function(browser,main_url,actor_url,file_path)





if __name__ == '__main__':
    main_url = 'https://javdb4.com'
    actor_url = 'https://javdb4.com/actors/x4MV'
    file_path = r'file\\all'
    main(main_url,actor_url,file_path)