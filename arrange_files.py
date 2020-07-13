#!/usr/bin/python3  
# -*- coding: utf-8 -*- 
import os,shutil
import pymysql

def sql_query():
    connect = pymysql.Connect(host='192.168.2.10',port=33077,user='root',passwd='Wjq1988!@#',db='javdb',charset='utf8')
    # 使用cursor()方法获取操作游标 
    cursor = connect.cursor()
    # SQL 查询语句
    sql = "SELECT fanhao,actors,video_cover,preview_video,preview_pictures FROM censored_info WHERE 1"
    # try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    tmp_list = []
    for row in results:
        tmp_list.append(row)
    # 关闭数据库连接
    connect.close()
    return tmp_list

def find_censored_images(censored_images_path):
    for file_name in os.listdir(censored_images_path):
        file_path = os.path.join(censored_images_path,file_name)
        if '.jpg' in file_path:
            print(file_name)
            print(file_path)
            # for images_path in os.listdir(file_path):
            #     images_path = os.path.join(file_path,images_path)
            #     
            #         print(json_path)
            #         html_path = json_path.replace('json','html')
            #         print(html_path)
            #         new_file_path = json_path.replace('.json','')
            #         print(new_file_path)
            #         fanhao = new_file_path.split('\\')[-1]
            #         print(fanhao)
            #         print('-'*20)
            #         if os.path.exists(new_file_path):
            #             pass
            #         else:
            #             os.mkdir(new_file_path)
            #         shutil.move(html_path, new_file_path)
            #         shutil.move(json_path, new_file_path)
            #         new_json_path = os.path.join(new_file_path,fanhao+'.json')


if __name__ == '__main__':
    censored_images_path = r'Z:\censored_images'
    find_censored_images(censored_images_path)
    # tmp_list = sql_query()
    # for x in tmp_list:
    #     print(x[0])
    