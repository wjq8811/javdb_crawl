#!/usr/bin/python3  
# -*- coding: utf-8 -*- 

# from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import file_io,my_selenium,crawler_function,main_crawler_one_artor_works

import requests
import os

def main(main_url,file_path):
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

    # try:
    #抓取所有演员地址并保存
    actors_list_path = file_path + '\\' + 'actors_list.txt'
    if os.path.exists(actors_list_path):
        print('actors_list已存在，如需更新请删除后重新开始。')
        actors_list = file_io.read_all_lines(actors_list_path)
    else:
        actors_list = crawler_function.crawler_all_actros(browser, main_url)
        file_io.write_all_lines(actors_list_path, actors_list)

    for tmp in actors_list:
        actor_name,actor_url = tmp.split('|')
        main_crawler_one_artor_works.function(browser,main_url,actor_url,file_path)
    # except Exception as e:
    #     browser.quit()
    #     main(main_url,file_path)
        



if __name__ == '__main__':
    main_url = 'https://javdb4.com'
    file_path = r'C:\javdb\all'
    main(main_url,file_path)