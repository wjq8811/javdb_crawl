from selenium import webdriver
import requests
from lxml import etree
import os
import time
import json

def read_all_text(path: str):
    with open(path, 'r', encoding='utf-8')as f:
        lines = f.readlines()
        text = ''.join(lines)
        return text

def write_all_text(path: str, content: str):
    create_dir_if_not_exist(os.path.dirname(path))
    with open(path, 'w', encoding='utf-8')as f:
        f.write(content)

def create_dir_if_not_exist(path: str):
    if path == '':
        return
    if not os.path.exists(path):
        os.makedirs(path)

def crawl_all_actors_page(actors_page_html_source,page_num,main_url):
    actors_page_html_source = etree.HTML(actors_page_html_source)
    num = len(actors_page_html_source.xpath('//*[@id="actors"]/div'))
    print('第'+ str(page_num) +'页，共'+str(num)+'名演员')
    actors_url_list = []
    for x in range(1, num):
        next_url = main_url + actors_page_html_source.xpath('//*[@id="actors"]/div[' + str(x) + ']/a/@href')[0]
        actors = actors_page_html_source.xpath('//*[@id="actors"]/div[' + str(x) + ']/a/@title')[0]
        actors_url_list.append([actors, next_url])
    return actors_url_list

def crawl_actor_works_page(html,main_url):
    html = etree.HTML(html)
    num = len(html.xpath('//*[@id="videos"]/div/div'))
    print('共'+ str(num) + '个番号')
    one_page_list = []
    for x in range(1, num):
        next_url = main_url + html.xpath('//*[@id="videos"]/div/div['+str(x)+']/a/@href')[0]
        fanhao = html.xpath('//*[@id="videos"]/div/div['+str(x)+']/a/div[2]/text()')[0]
        one_page_list.append([fanhao,next_url])
    return one_page_list

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
        print(fanhao + '.json已存在')
        return
    title,fanhao,time,scoring,type_,performer,poster,trailer,magnet_list = html_to_info(one_page_html)
    d = {'title': title, 'fanhao': fanhao,
            'time': time, 'scoring': scoring,
            'type_': type_, 'performer': performer,
            'title': title, 'trailer': trailer,
            'magnet_list': magnet_list}
    write_all_text(path_file_json, json.dumps(d, ensure_ascii=False))


def main():
    main_url = 'https://javdb4.com'
    file_path = r'file'
    #定义浏览器，不加载图片，跳过认证
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2
        }
    }
    options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(main_url)
    browser.find_elements_by_xpath("/html/body/div[1]/div[2]/footer/a[1]")[0].click()
    main_html_source = browser.page_source
    print(main_html_source)


    #1爬取所有演员地址
    for page_num in range(1,31):#最后一页是30页懒得写
        actors_url_list = []
        actors_page_url = main_url + '/actors?page=' + str(page_num)
        browser.get(actors_page_url)
        actors_page_html_source = browser.page_source
        actors_url_list = crawl_all_actors_page(actors_page_html_source,page_num,main_url)
        # print('第'+ str(page_num)+'页-------------------')
        #2爬取演员下的作品地址
        for actor,actor_works_url in actors_url_list:
            print(actor)
            print(actor_works_url)
            #判断是否存在actor文件夹
            actor_path = file_path + '\\' + actor
            create_dir_if_not_exist(actor_path)
            #爬取每个演员所有的作品链接
            one_page_list = []
            for x in range(1,2):
                actor_all_url = actor_works_url + '?page=' + str(x)
                print(actor_all_url)
                browser.get(actor_all_url)
                actor_all_page_html = browser.page_source
                one_page_list = one_page_list+ crawl_actor_works_page(actor_all_page_html,main_url)
                if '下一頁' not in actor_all_page_html:
                    break
                time.sleep(5)
            print('共找到' + str(len(one_page_list)) + '个番号')
            #3保存每个作品的html
            for fanhao,one_page_url in one_page_list:
                print(fanhao,one_page_url)
                path_file_html = actor_path+ '\\' + fanhao + '.html'
                browser.get(one_page_url)
                one_page_html = browser.page_source
                write_all_text(path_file_html,one_page_html)
                #4根据本地html提取info
                #5保存为json
                info_to_json(one_page_html, fanhao,actor_path)
                print('json保存成功----------')
                time.sleep(5)
            time.sleep(5)
        time.sleep(5)
        print("-"*40)






if __name__ == '__main__':
    main()