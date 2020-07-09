#!/usr/bin/python3  
# -*- coding: utf-8 -*- 
import os,shutil

def function(path):
    for file_path in os.listdir(path):
        file_path = os.path.join(path,file_path)
        if os.path.isdir(file_path):
            print(file_path)
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


if __name__ == '__main__':
    path = r'Y:\javdb\all'
    function(path)