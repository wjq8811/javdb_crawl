#!/usr/bin/python3  
# -*- coding: utf-8 -*- 
import requests
from lxml import etree
import os
import time
import json
import file_io,my_selenium,crawler_function

def main(main_url, file_path):
    header = my_selenium.steal_library_header(url=main_url)
    type_video = ['LUXU','ARA','SIRO','GANA','MIUM']
    for x in type_video:
        serise_path = file_path + '\\' + x
        file_io.create_dir_if_not_exist(serise_path)
        serise_url = 'https://javdb4.com/video_codes/' + x
        work_list_path = serise_path + '\\' + 'work_list.txt'
        if os.path.exists(work_list_path):
            print('work_list.txt已存在，如需更新，请删除后重新开始。')
            #读取url，爬取页面
            work_list = file_io.read_all_lines(work_list_path)
        else:
            pass
            print('work_list.txt不存在')
            #爬取页面，保存url
            work_list = crawler_function.crawler_serise_works(header,serise_url,main_url)
            file_io.write_all_lines(work_list_path, work_list)

        crawler_function.crawler_top_work(header, main_url,work_list,serise_path)
        print('文件保存在：'+serise_path)
        print('-'*20)

if __name__ == '__main__':
    main_url = 'https://javdb4.com'
    file_path = r'C:\javdb\serise'
    main(main_url, file_path)

