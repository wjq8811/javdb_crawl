#!/usr/bin/python3  
# -*- coding: utf-8 -*- 
import file_io,my_selenium,crawler_function,main_crawler_one_artor_works
import requests
import os

def main(main_url,file_path):
    header = my_selenium.steal_library_header(url=main_url)
    # try:
    #抓取所有演员地址并保存
    actors_list_path = file_path + '\\' + 'actors_list.txt'
    if os.path.exists(actors_list_path):
        print('actors_list已存在，如需更新请删除后重新开始。')
        actors_list = file_io.read_all_lines(actors_list_path)
    else:
        actors_list = crawler_function.crawler_all_actros(header, main_url)
        file_io.write_all_lines(actors_list_path, actors_list)

    for tmp in actors_list:
        actor_name,actor_url = tmp.split('|')
        main_crawler_one_artor_works.function(header,main_url,actor_url,file_path)
    # except Exception as e:




if __name__ == '__main__':
    main_url = 'https://javdb4.com'
    file_path = r'C:\javdb\all'
    main(main_url,file_path)