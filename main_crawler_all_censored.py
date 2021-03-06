#!/usr/bin/python3  
# -*- coding: utf-8 -*- 
import file_io,my_selenium,crawler_function,main_crawler_one_artor_works
import requests
import os

def main(main_url,file_path):
    header = my_selenium.steal_library_header(url=main_url)
    # try:
    #抓取所有演员地址并保存
    print('文件保存在：'+file_path)
    actors_list_path = file_path + '\\' + 'actors_list.txt'
    if os.path.exists(actors_list_path):
        print('actors_list已存在，如需更新请删除后重新开始。')
        actors_list = file_io.read_all_lines(actors_list_path)
    else:
        actors_list = crawler_function.crawler_all_actros(header, main_url)
        file_io.write_all_lines(actors_list_path, actors_list)

    for tmp in actors_list:
        try:
            actor_name,actor_url = tmp.split('|')
            print(actor_name,actor_url)
            #ToDo 这里的actor_name名字和html中'演员：XXXXX'不太一样
            main_crawler_one_artor_works.function(header,main_url,actor_url,file_path)
        except Exception as e:
            continue



    # except Exception as e:
    #     main(main_url,file_path)
    # print('文件保存在：'+file_path)


if __name__ == '__main__':
    main_url = 'https://javdb4.com'
    file_path = r'Z:\censored'
    main(main_url,file_path)
