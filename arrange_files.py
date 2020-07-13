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

def arrange_censored_images(censored_path,censored_images_path):
    tmp_list = sql_query()
    print('sql_query_ok')
    #先找html路径
    num = 1 
    for root,dirs,files in os.walk(censored_path):
        for html_name in files:
            html_path = os.path.join(root,html_name)
            if '.html' in html_path:
                print(num,'_'*20)
                print(html_name.encode('gbk', 'ignore').decode('gbk'))
                print(html_path.encode('gbk', 'ignore').decode('gbk'))
                html_fanhao = html_name.replace('.html','')
                html_fanart_path = root + '\\' + html_fanhao + '-fanart.jpg'
                if os.path.exists(html_fanart_path):
                    print('fanart已存在')
                    continue
                else: 
                    for tmp in tmp_list:
                        sql_fanhao,actors,video_cover,preview_video,preview_pictures = tmp
                        sql_img_name = ''
                        if sql_fanhao == html_fanhao:
                            sql_img_name = video_cover.split('/')[-1]
                            break
                    if sql_img_name == '':
                        print('数据库中找不到html_fanhao')
                        continue
                    else:
                        for img_name in os.listdir(censored_images_path):
                            img_path = os.path.join(censored_images_path,img_name)
                            if sql_img_name == img_name:
                                old_img_path = img_path
                                print(old_img_path)
                                #移动
                                shutil.copy(old_img_path,root)
                                print('移动成功')
                                #重命名
                                old_name = root + '\\' + img_name
                                new_name = root + '\\' + sql_fanhao + '-fanart.jpg'
                                os.rename(old_name,new_name)
                                print('重命名成功')
                                num +=1
                                break

if __name__ == '__main__':
    censored_images_path = r'E:\javdb\censored\censored_poster'
    censored_path = r'Z:\censored'
    arrange_censored_images(censored_path,censored_images_path)
    # tmp_list = sql_query()
    # for x in tmp_list:
    #     print(x[0])
    