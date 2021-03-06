#!/usr/bin/python3  
# -*- coding: utf-8 -*- 
import file_io,my_selenium,html_to_json
import os

def crawler_all_actros(header, main_url):
    xpath_ = '//*[@id="actors"]/div'
    actors_list = []
    for page_num in range(1, 50):  # 只有30页？
        actors_page_url = main_url + '/actors?page=' + str(page_num)
        html, html_text, html_xpath = my_selenium.get_html_by_requests(header,actors_page_url, xpath_)
        num = len(html_xpath.xpath('//*[@id="actors"]/div'))
        print(actors_page_url)
        print('第' + str(page_num) + '页，共' + str(num) + '名演员')
        for x in range(1, num+1):
            next_url = main_url + \
                html_xpath.xpath(
                    '//*[@id="actors"]/div[' + str(x) + ']/a/@href')[0]
            actor = html_xpath.xpath(
                '//*[@id="actors"]/div[' + str(x) + ']/a/@title')[0]
            actors_list.append(actor+'|'+next_url)
        if '下一頁' not in html_text :
            break
    print('共找到' + str(len(actors_list)) + '名演员')
    print('-' * 20)
    return actors_list

def crawler_actro_works(header, main_url, actor_url):
    xpath_ = '//*[@id="videos"]/div/div/a'
    num = 1
    work_list = []
    for page_num in range(1,100):
        tmp_work_list = []
        actor_works_url = actor_url + '?page=' + str(page_num)
        html, html_text, html_xpath = my_selenium.get_html_by_requests(header,actor_works_url, xpath_)
        # print(html)
        try:
        # /html/head/title/text()  竹內乃愛(竹内乃愛) | JavDB - 成人影片資料庫 - 磁力鏈接分享
            actor_name = html_xpath.xpath('/html/head/title/text()')[0].split('|')[0].replace(' ','')
        except Exception as e:
            print('actor_name有误')
            work_list = crawler_actro_works(header, main_url, actor_url)
            return work_list
        print(actor_name)
        print(actor_works_url)
        works_num = len(html_xpath.xpath(xpath_))
        print('第' + str(page_num) + '页，共' + str(works_num) + '作品')
        for y in range(1,works_num+1):
            fanhao_url = main_url + \
                html_xpath.xpath('//*[@id="videos"]/div/div[' + str(y) + ']/a/@href')[0]
            fanhao = html_xpath.xpath('//*[@id="videos"]/div/div[' + str(y) + ']/a/div[2]/text()')[0]
            # //*[@id="videos"]/div/div[3]/a/div[4]/span
            text_tmp = ''
            for x in html_xpath.xpath('//*[@id="videos"]/div/div[' + str(y) + ']//text()'):
                text_tmp += x
            if '可下' in text_tmp:
                work_list.append(actor_name+'|'+fanhao+'|'+fanhao_url)
                tmp_work_list.append(actor_name+'|'+fanhao+'|'+fanhao_url)
                # print(fanhao,fanhao_url,'可下，已保存url')
            else:
                pass
                # print(fanhao,fanhao_url,'找不到可下载，已跳过')
                # print(text_tmp)
        print('共找到' + str(len(tmp_work_list)) + '个可下载作品')
        print('-' * 20)
        num +=1
        if '下一頁' not in html_text :
            break
    print('共找到' + str(len(work_list)) + '个可下载作品')
    print('-' * 20)
    return work_list

def crawler_work(header, main_url,work_list,file_path):
    xpath_ = '//*[@id="magnets-content"]'
    num = 1
    nums = len(work_list)
    for x in work_list:
        actor_name,fanhao,fanhao_url = x.split('|')
        print('共：' + str(nums)+'部，第：' + str(num)+'部')
        num +=1
        print(actor_name,fanhao)
        print(fanhao_url)
        #判断文件夹是否存在
        actor_path = file_path + '\\' + actor_name + '\\' + fanhao
        file_io.create_dir_if_not_exist(actor_path)
        # 3保存每个作品的html
        work_html_path = actor_path + '\\' + fanhao + '.html'
        if os.path.exists(work_html_path):
            html_text = file_io.read_all_text(work_html_path)
            print('html已存在，读取成功')
        else:
            html, html_text, html_xpath = my_selenium.get_html_by_requests(header,fanhao_url, xpath_)
            print('html爬取成功')
            if '暫無磁鏈下載' in html_text:
                print('暫無磁鏈下載，跳过该番号。')
                print('-' * 20)
                continue
            elif len(html_xpath.xpath('//*[@id="magnets-content"]/table//tr'))==0:
                print('找不到磁鏈下載，跳过该番号。')
                print('-' * 20)
                continue
            file_io.write_all_text(work_html_path, html_text)
            print('html保存成功')
        html_to_json.info_to_json(html_text, fanhao, actor_path)
        print('-' * 20)

def crawler_top_works(header,top_url,main_url):
    xpath_ = '//*[@id="videos"]/div/div'
    work_list = []
    html, html_text, html_xpath = my_selenium.get_html_by_requests(header,top_url, xpath_)
    works_num = len(html_xpath.xpath(xpath_))
    for y in range(1,works_num+1):
        fanhao_url = main_url + \
            html_xpath.xpath('//*[@id="videos"]/div/div[' + str(y) + ']/a/@href')[0]
        fanhao = html_xpath.xpath(
            '//*[@id="videos"]/div/div[' + str(y) + ']/a/div[2]/text()')[0]
        work_list.append(fanhao+'|'+fanhao_url)
    print('共找到' + str(len(work_list)) + '个番号')
    print('-' * 20)
    return work_list

#上个页面没有名字，得重写
def crawler_top_work(header, main_url,work_list,file_path_):
    xpath_ = '//*[@id="magnets-content"]'
    num = 1
    nums = len(work_list)
    for x in work_list:
        fanhao,fanhao_url = x.split('|')
        print('共：' + str(nums)+'部，第：' + str(num)+'部')
        num +=1
        print(fanhao)
        print(fanhao_url)
        file_path = file_path_ + '\\' + fanhao
        #判断文件夹是否存在
        file_io.create_dir_if_not_exist(file_path)
        # 3保存每个作品的html
        work_html_path = file_path + '\\' + fanhao + '.html'
        if os.path.exists(work_html_path):
            html_text = file_io.read_all_text(work_html_path)
            print('html已存在，读取成功')
        else:
            html, html_text, html_xpath = my_selenium.get_html_by_requests(header,fanhao_url, xpath_)
            print('html爬取成功')
            if '暫無磁鏈下載' in html_text:
                print('暫無磁鏈下載，跳过该番号。')
                print('-' * 20)
                continue
            elif len(html_xpath.xpath('//*[@id="magnets-content"]/table//tr'))==0:
                print('找不到磁鏈下載，跳过该番号。')
                print('-' * 20)
                continue
            file_io.write_all_text(work_html_path, html_text)
            print('html保存成功')
        html_to_json.info_to_json(html_text, fanhao, file_path)
        print('-' * 20)

def crawler_serise_works(header,serise_url,main_url):
    xpath_ = '//*[@id="videos"]/div/div/a'
    num = 1
    work_list = []
    for page_num in range(1,100):
        tmp_work_list = []
        works_url = serise_url + '?page=' + str(page_num)
        html, html_text, html_xpath = my_selenium.get_html_by_requests(header,works_url, xpath_)
        # print(html)
        print(works_url)
        works_num = len(html_xpath.xpath(xpath_))
        print('第' + str(page_num) + '页，共' + str(works_num) + '作品')
        for y in range(1,works_num+1):
            fanhao_url = main_url + \
                html_xpath.xpath('//*[@id="videos"]/div/div[' + str(y) + ']/a/@href')[0]
            fanhao = html_xpath.xpath('//*[@id="videos"]/div/div[' + str(y) + ']/a/div[2]/text()')[0]
            text_tmp = ''
            for x in html_xpath.xpath('//*[@id="videos"]/div/div[' + str(y) + ']//text()'):
                text_tmp += x
            if '可下' in text_tmp:
                work_list.append(fanhao+'|'+fanhao_url)
                tmp_work_list.append(fanhao+'|'+fanhao_url)
                # print(fanhao,fanhao_url,'可下，已保存url')
            else:
                pass
                # print(fanhao,fanhao_url,'找不到可下载，已跳过')
                # print(text_tmp)
        print('共找到' + str(len(tmp_work_list)) + '个可下载作品')
        print('-' * 20)
        num +=1
        if '下一頁' not in html_text :
            break
    print('共找到' + str(len(work_list)) + '个可下载作品')
    print('-' * 20)
    return work_list



def main():
    pass

if __name__ == '__main__':
    main()