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
    
    
    list1_1 = ['演员','番号','时间','标题','评分','类型','海报','预告片','链接信息','链接时间','中文字幕','链接地址']
    sheet1.append(list1_1)

    for root,dirs,files in os.walk(path):
        for name in files:
            json_path = os.path.join(root,name)
            if '.json' in json_path:
                print(json_path)
                with open(json_path,'r', encoding='utf-8') as load_f:
                    load_dict = json.load(load_f)
                    title = ''
                    if len(load_dict['title']):
                        title =  load_dict['title'][0]

                    fanhao = ''
                    if len(load_dict['fanhao']):
                        fanhao = load_dict['fanhao'][0]

                    time = ''
                    if len(load_dict['time']):
                        time =  load_dict['time'][0]

                    scoring = ''
                    if len(load_dict['scoring']):
                        scoring = load_dict['scoring'][0].replace(' ','')#评分

                    type_ = ''
                    for x in load_dict['type_']:#类型
                        type_ += '、' + x
                    if type_ != '':
                        type_ = type_[1:]

                    performer = ''
                    for x in load_dict['performer']:#演员
                        performer += '、' + x
                    if performer != '':
                        performer = performer[1:]

                    poster = ''
                    if len(load_dict['scoring']):
                        poster = load_dict['poster'][0]#海报

                    trailer = ''
                    if len(load_dict['trailer']):
                        trailer = 'https://' + load_dict['trailer'][0]#预告片

                    for magnets in load_dict['magnet_list']:
                        magnet_link,magnet_time,magnet_info = magnets

                        #是否中文
                        is_zh = '否'
                        if ('字幕' in magnet_info) or ('中文' in magnet_info):
                            is_zh = '是'


                        tmp_list = [performer,fanhao,time,title,scoring,type_,poster,trailer,magnet_info,magnet_time,is_zh,magnet_link]
                        sheet1.append(tmp_list)
                        for x in tmp_list:
                            print(x.encode('gbk', 'ignore').decode('gbk'))
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    new_name = './'+ str(now) +'.xlsx'
    wb.save(filename=new_name)
    print('保存成功_'+now+'.xlsx')



if __name__ == '__main__':
    path = r'C:\Users\w\Desktop\javdb_crawl\file\all'
    main(path)