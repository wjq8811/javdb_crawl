#!/usr/bin/python3  
# -*- coding: utf-8 -*- 
import urllib.request
import gevent
from gevent import monkey

import json
import os,shutil

monkey.patch_all()

def downloader(file_path, url):
    print(url)
    print(file_path)
    req = urllib.request.urlopen(url)
    file_content = req.read()
    with open(file_path, "wb") as f:
        f.write(file_content)


def main(path):
    for file_path in os.listdir(path):
        file_path = os.path.join(path,file_path)
        if os.path.isdir(file_path):
            print(file_path)
            gevent_list = []
            for json_path in os.listdir(file_path):
                json_path = os.path.join(file_path,json_path)
                if '.json' in json_path:
                    print(json_path)
                    html_path = json_path.replace('json','html')
                    print(html_path)
                    new_file_path = json_path.replace('.json','')
                    print(new_file_path)
                    fanhao = new_file_path.split('\\')[-1]
                    print(fanhao)
                    print('-'*20)
                    if os.path.exists(new_file_path):
                        pass
                    else:
                        os.mkdir(new_file_path)
                    shutil.move(html_path, new_file_path)
                    shutil.move(json_path, new_file_path)
                    new_json_path = os.path.join(new_file_path,fanhao+'.json')
                    print(new_json_path)

            for root,dirs,files in os.walk(file_path):
                for name in files:
                    json_path = os.path.join(root,name)
                    if '.json' in json_path:
                        print(json_path)
                        with open(json_path,'r', encoding='utf-8') as load_f:
                            load_dict = json.load(load_f)

                        #海报
                        poster_url = ''.join(load_dict['poster'])
                        poster_path = os.path.join(root,name.replace('.json','')+'_poster.' + poster_url.split('.')[-1])
                        # print(poster_path)
                        if os.path.exists(poster_path):
                            print('海报已存在')
                        else:
                            gevent_list.append(gevent.spawn(downloader,poster_path,poster_url))

                        #截图列表 fanart
                        images_list = load_dict['images_list']
                        num = 0
                        for fanart_urL in images_list:
                            # print(fanart_urL)
                            fanart_path = os.path.join(root,name.replace('.json','')+'_fanart-'+str(num)+'.' + fanart_urL.split('.')[-1])
                            if os.path.exists(fanart_path):
                                print('截图已存在')
                            else:
                                gevent_list.append(gevent.spawn(downloader,fanart_urL,fanart_path))
                            num+=1

                        #trailer load_dict['trailer'] #预告片
                        trailer_url = ''.join(load_dict['trailer'])
                        trailer_path = os.path.join(root,name.replace('.json','')+'_trailer.' + trailer_url.split('.')[-1])
                        if os.path.exists(trailer_path):
                            print('预告片已存在')
                        else:
                            gevent_list.append(gevent.spawn(downloader,trailer_url,trailer_path))

                        gevent.joinall(gevent_list)
                        print('-'*20)
        print('-'*40)


if __name__ == '__main__':
    path = r'C:\javdb\all'
    main(path)

