#!/usr/bin/python3  
# -*- coding: utf-8 -*- 
import requests
from lxml import etree
import os
import time
import json
import file_io,my_selenium,crawler_function



def existing_censored(file_path,work_list_path):
    for artor in os.listdir(file_path):
        artor_path = os.path.join(file_path,artor)
        if os.path.isdir(artor_path):
            for fanhao in os.listdir(artor_path):
                fanhao_path = os.path.join(artor_path,fanhao)
                if os.path.isdir(fanhao_path):
                    print(artor,fanhao)
                    tmp = artor+'|'+fanhao
                    file_io.write_all_text_add(work_list_path,tmp)

def find_out(work_list):
    for x in work_list:
        fanhao,fanhao_url = x.split('|')



def main(main_url, file_path):
    #https://javdb4.com/tags?page=100 目前观察只有80页
    my_work_list_path = file_path + '\\' + 'up_censored.txt'
    up_work_list_path = file_path + '\\' + 'up_censored.txt'

    if os.path.exists(my_work_list_path):
        #删掉
        os.remove(my_work_list_path)
    existing_censored(file_path,my_work_list_path)

    header = my_selenium.steal_library_header(url=main_url)
    new_censored_url = 'https://javdb4.com/tags' + x
    if os.path.exists(up_work_list_path):
        print('work_list.txt已存在，如需更新，请删除后重新开始。')
        #读取url，爬取页面
        work_list = file_io.read_all_lines(up_work_list_path)
    else:
        #爬取页面，保存url
        work_list = crawler_function.crawler_serise_works(header,new_censored_url,main_url)
        file_io.write_all_lines(work_list_path, up_work_list_path)

    


if __name__ == '__main__':
    main_url = 'https://javdb4.com'
    file_path = r'C:\javdb\censored'
    work_list_path = file_path + '\\' + 'up_censored.txt'
    main(main_url, file_path)

