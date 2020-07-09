#!/usr/bin/python3  
# -*- coding: utf-8 -*- 
from lxml import etree
import os
import time
import json
import file_io,my_selenium,crawler_function

def function(header,main_url,actor_url,file_path):
    work_list = crawler_function.crawler_actro_works(header, main_url,actor_url)
    actor_name = work_list[0].split('|')[0]
    work_list_path = file_path + '\\' + actor_name +'\\' + actor_name + '_work_list.txt'
    file_io.write_all_lines(work_list_path, work_list)
    #读取本地所有作品地址并保存
    work_list = file_io.read_all_lines(work_list_path)
    crawler_function.crawler_work(header, main_url,work_list,file_path)


def main(main_url,actor_url,file_path):
    header = my_selenium.steal_library_header(url=main_url)
    function(header,main_url,actor_url,file_path)





if __name__ == '__main__':
    main_url = 'https://javdb4.com'
    actor_url = 'https://javdb4.com/actors/x4MV'
    file_path = r'C:\javdb\all'
    main(main_url,actor_url,file_path)