#!/usr/bin/python3  
# -*- coding: utf-8 -*- 
import requests
from lxml import etree
import os
import time
import json
import file_io,my_selenium,crawler_function


def function(file_path,header,top_url,main_url):
    #爬取top页面，保存url
    work_list_path = file_path + '\\' + 'work_list.txt'
    work_list = crawler_function.crawler_top_works(header,top_url,main_url)
    file_io.write_all_lines(work_list_path, work_list)
    #读取url，爬取页面
    work_list = file_io.read_all_lines(work_list_path)
    crawler_function.crawler_top_work(header, main_url,work_list,file_path)

def main(main_url, file_path):
    header = my_selenium.steal_library_header(url=main_url)
    type_video = ['video_censored','video_uncensored','video_western','video_fc2']
    type_period = ['daily','weekly','monthly']
    for x in type_video:
        for y in type_period:
            file_path = file_path + '\\' + x + '\\' + y
            top_url = 'https://javdb4.com/rankings/' + x + '?period=' + y
            print('file_path:',file_path)
            print('top_url:',top_url)
            function(file_path,header,top_url,main_url)
            print('-'*20)

if __name__ == '__main__':
    main_url = 'https://javdb4.com'
    file_path = r'C:\javdb\top'
    main(main_url, file_path)

