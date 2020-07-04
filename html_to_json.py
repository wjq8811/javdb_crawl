#!/usr/bin/python3  
# -*- coding: utf-8 -*- 
import os
import json
import file_io
from lxml import etree

def html_to_info(html_):
    html = etree.HTML(html_)
    title = html.xpath('/html/body/section/div/h2/strong/text()')
    # print(title.encode('gbk', 'ignore').decode('gbk'))
    fanhao = ''
    time = ''
    scoring = ''
    type_ = ''
    performer = ''
    for x in range(1,10):
        strong_text = html.xpath('/html/body/section/div/div[3]/div[2]/nav/div[' + str(x) + ']/strong/text()')
        # print(strong_text)
        if '番號:' in strong_text:
            fanhao = html.xpath('/html/body/section/div/div[3]/div[2]/nav/div[' + str(x) + ']/a/@data-clipboard-text')
            continue
            
        if '時間:' in strong_text:
            time = html.xpath('/html/body/section/div/div[3]/div[2]/nav/div[' + str(x) + ']/span/text()')
            continue

        if '評分:' in strong_text:
            scoring = html.xpath('/html/body/section/div/div[3]/div[2]/nav/div[' + str(x) + ']/span/text()')
            continue

        if '類別:' in strong_text:
            type_ = html.xpath('/html/body/section/div/div[3]/div[2]/nav/div[' + str(x) + ']/span/a/text()')
            continue

        if '演員:' in strong_text:
            performer = html.xpath('/html/body/section/div/div[3]/div[2]/nav/div[' + str(x) + ']/span/a/text()')
            continue

    if '暫無磁鏈下載' in html_:
        magnet_list = []
        print('暫無磁鏈下載')
    else:
        magnet_list = []
        for x in range(1,10):
            #//*[@id="magnets-content"]/table/tbody/tr[4]/td[1]/a/@href
            magnet_link = html.xpath('//*[@id="magnets-content"]/table//tr[' + str(x) + ']/td[1]/a/@href')
            magnet_info_list = html.xpath('//*[@id="magnets-content"]/table//tr[' + str(x) + ']/td[1]/a/span/text()')
            magnet_time = html.xpath('//*[@id="magnets-content"]/table//tr[' + str(x) + ']/td[2]/span/text()')
            # print(magnet_link)
            if len(magnet_link):
                magnet_info = ''
                for x in magnet_info_list:
                    magnet_info += '|'+x.replace(' ','').replace('\n','').replace('\xa0','')
                    magnet_info = magnet_info[1:]
                magnet_list.append([magnet_link[0],magnet_time[0],magnet_info])
    # print(magnet_list)
    #海报
    poster = html.xpath('/html/body/section/div/div[3]/div[1]/a/img/@src')
    #预告片
    trailer = html.xpath('//*[@id="preview-video"]/source/@src')
    return title,fanhao,time,scoring,type_,performer,poster,trailer,magnet_list

def info_to_json(one_page_html, fanhao: str,actors_path: str):
    path_file_json = actors_path + '\\' + fanhao + '.json'
    if os.path.exists(path_file_json):
        print('json已存在')
        return
    title,fanhao,time,scoring,type_,performer,poster,trailer,magnet_list = html_to_info(one_page_html)
    d = {'title': title, 'fanhao': fanhao,
            'time': time, 'scoring': scoring,
            'type_': type_, 'performer': performer,
            'poster': poster, 'trailer': trailer,
            'magnet_list': magnet_list}
    file_io.write_all_text(path_file_json, json.dumps(d, ensure_ascii=False))
    print('json保存成功')



def main():
    work_html_path = r'C:\Users\w\Desktop\新建文件夹\file\高崎聖子(高橋しょう子)\MIDE-551.html'
    work_html = file_io.read_all_text(work_html_path)
    print(work_html.encode('gbk', 'ignore').decode('gbk'))
    title,fanhao,time,scoring,type_,performer,poster,trailer,magnet_list = html_to_info(work_html)
    for x in [title,fanhao,time,scoring,type_,performer,poster,trailer,magnet_list]:
        print(x)
    
    


if __name__ == '__main__':
    main()