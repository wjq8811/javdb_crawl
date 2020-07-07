#!/usr/bin/python3  
# -*- coding: utf-8 -*- 
import os
import json
import datetime
from openpyxl import Workbook

def main(path):
    wb = Workbook()
    ws1 = wb.active
    ws1.title = "sheet1"
    sheet1 = wb[wb.sheetnames[0]]
    
    
    list1_1 = ['演员','番号','时间','标题','时间','评分','类型','海报','预告片','截图','链接信息','链接时间','中文字幕','链接地址']
    sheet1.append(list1_1)

    for root,dirs,files in os.walk(path):
        for name in files:
            json_path = os.path.join(root,name)
            if '.json' in json_path:
                print(json_path)
                with open(json_path,'r', encoding='utf-8') as load_f:
                    load_dict = json.load(load_f)

                    title = ''.join(load_dict['title'])
                    fanhao = ''.join(load_dict['fanhao'])
                    time = ''.join(load_dict['time'])
                    scoring = ''.join(load_dict['scoring'])#评分 
                    type_ = '、'.join(load_dict['type_'])
                    performer = '、'.join(load_dict['performer'])#演员
                    poster = ''.join(load_dict['poster'])#海报
                    trailer = ''.join(load_dict['trailer'])#预告片
                    runtimeg = ''.join(load_dict['runtimeg'])#片长
                    #截图列表'images_list':images_list
                    images = '|'.join(load_dict['images_list'])

                    for magnets in load_dict['magnet_list']:
                        magnet_link,magnet_time,magnet_info = magnets

                        #是否中文
                        is_zh = '否'
                        if ('字幕' in magnet_info) or ('中文' in magnet_info):
                            is_zh = '是'

                        tmp_list = [performer,fanhao,time,title,runtimeg,scoring,type_,poster,trailer,images,magnet_info,magnet_time,is_zh,magnet_link]
                        sheet1.append(tmp_list)
                        for x in tmp_list:
                            print(x.encode('gbk', 'ignore').decode('gbk'))
                        print('_'*20)
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    new_name = path + '\\' + str(now) +'.xlsx'
    wb.save(filename=new_name)
    print('文件保存在'+ new_name)



if __name__ == '__main__':
    path = r'C:\javdb\all'
    main(path)