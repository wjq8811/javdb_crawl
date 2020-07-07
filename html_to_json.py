#!/usr/bin/python3  
# -*- coding: utf-8 -*- 
import os,re
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
        #/html/body/section/div/div[3]/div/div[2]/nav
        # /html/body/section/div/div[3]/div/div[2]/nav/div[1]
        strong_text = html.xpath('/html/body/section/div/div[3]/div[2]/nav/div[' + str(x) + ']/strong/text()')
        print(strong_text)
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


# 功能：去除xml文档和windows路径不允许的特殊字符 &<>  \/:*?"<>|
# 参数：（文件名、简介、标题）str
# 返回：str
# 辅助：无
def replace_xml_win(name):
    # 替换windows路径不允许的特殊字符 \/:*?"<>|
    return name.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')\
                .replace('\n', '').replace('\t', '').replace('\r', '')\
                .replace("\\", "#").replace("/", "#").replace(":", "：").replace("*", "#")\
                .replace("?", "？").replace("\"", "#").replace("|", "#").rstrip()

def html_to_info_by_copy_javsdt(html_web_):
    # 有大部分信息的html_web
    html_web = re.search(r'h2 class([\s\S]*?)想看', html_web_, re.DOTALL).group(1)
    # print(html_web)
    # 标题
    title = re.search(r'strong>(.+?)</', html_web).group(1).replace(' 中文字幕 ', '')
    # 去除xml文档和windows路径不允许的特殊字符 &<>  \/:*?"<>|
    title = replace_xml_win(title)
    print('影片标题：', title)
    # title的开头是车牌号，想要后面的纯标题
    car_titleg = re.search(r'(.+?) (.+)', title)

    # 车牌号
    fanhao = [car_titleg.group(1)]
    # print(fanhao)

    # 给用户重命名用的标题是“短标题”，nfo中是“完整标题”，但用户在ini中只用写“标题”
    title = [car_titleg.group(2)]
    # print(title)

    # DVD封面cover
    coverg = re.search(r'img src="(.+?)"', html_web)  # 封面图片的正则对象
    if str(coverg) != 'None':
        poster = [coverg.group(1)]
    else:
        poster = []
    # print(poster)

    # 发行日期
    premieredg = re.search(r'(\d\d\d\d-\d\d-\d\d)', html_web)
    if str(premieredg) != 'None':
        time = [premieredg.group(1)]
    else:
        time = []
    # print(time)

    # 片长 <td><span class="text">150</span> 分钟</td>
    runtimeg = re.search(r'value">(\d+) 分鍾<', html_web)
    if str(runtimeg) != 'None':
        runtimeg = [runtimeg.group(1)+'min']
    else:
        runtimeg = ['0min']
    # print(runtimeg)

    # 片商 制作商
    studiog = re.search(r'makers/.+?">(.+?)<', html_web)
    if str(studiog) != 'None':
        studio = [replace_xml_win(studiog.group(1))]
    else:
        studio = []
    # print(studio)

    #评分
    scoring = re.findall(r'</span>(.+?分.+?)</span>', html_web)
    if len(scoring)>0:
        scoring = [scoring[0].replace('&nbsp','').replace(';','').replace(' ','')]
    else:
        scoring = []
    # print(scoring)

    # 特点
    genres = re.findall(r'tags.+?">(.+?)</a>', html_web)
    type_ = [i for i in genres if i != '其他' and i != '成人' and i != '素人' and i != '高清' and i != '字幕']    # 这些特征没有参考意义，为用户删去
    # print(type_)

    #演员
    performer = re.findall(r'"/actors/.+?">(.+?)<', html_web)
    # print(performer)

    #截图
    images_list = re.findall(r'tile-item.+?(https://.+?.jpg)"', html_web_)
    # print(images_list)
    
    #预告片
    preview_video = re.findall(r'source src="(.+?)"', html_web_)
    if len(preview_video)>0:
        trailer = ['https:' + preview_video[0]]
    else:
        trailer = [preview_video]
    # print(trailer)

    #磁力链接
    magnet_list = re.findall(r'(magnet:\?xt=.+?)"', html_web_)
    # print(magnet_list)
    return title,fanhao,time,scoring,type_,performer,poster,trailer,magnet_list,images_list,runtimeg



def info_to_json(one_page_html, fanhao: str,actors_path: str):
    path_file_json = actors_path + '\\' + fanhao + '.json'
    if os.path.exists(path_file_json):
        print('json已存在')
        return
    title,fanhao,time,scoring,type_,performer,poster,trailer,magnet_list,images_list,runtimeg = html_to_info(one_page_html)
    d = {'title': title, 'fanhao': fanhao,
            'time': time, 'scoring': scoring,'runtimeg':runtimeg,
            'type_': type_, 'performer': performer,
            'poster': poster, 'trailer': trailer,
            'magnet_list': magnet_list,'images_list':images_list}
    file_io.write_all_text(path_file_json, json.dumps(d, ensure_ascii=False))
    # print('json保存成功')



def main():
    work_html_path = r'C:\javdb\all\高崎聖子(高橋しょう子)\MIDE-777.html'
    work_html = file_io.read_all_text(work_html_path)
    # print(work_html.encode('gbk', 'ignore').decode('gbk'))
    # title,fanhao,time,scoring,type_,performer,poster,trailer,magnet_list = html_to_info(work_html)
    # for x in [title,fanhao,time,scoring,type_,performer,poster,trailer,magnet_list]:
    #     print(x)
    title,fanhao,time,scoring,type_,performer,poster,trailer,magnet_list,images_list,runtimeg = html_to_info_by_copy_javsdt(work_html)
    print(title,fanhao,time,scoring,type_,performer,poster,trailer,magnet_list,images_list,runtimeg)

if __name__ == '__main__':
    main()