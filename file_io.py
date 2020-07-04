# version 2020.0411.1341
# author 117503445
# email t117503445@gmail.com

import os


def read_all_text(path: str):
    with open(path, 'r', encoding='utf-8')as f:
        lines = f.readlines()
        text = ''.join(lines)
        return text


def read_all_lines(path: str):
    with open(path, 'r', encoding='utf-8')as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].replace('\n', '')
            lines[i] = lines[i].replace('\r', '')
        return lines


def write_all_text(path: str, content: str):
    create_dir_if_not_exist(os.path.dirname(path))
    with open(path, 'w', encoding='utf-8')as f:
        f.write(content)


def write_all_lines(path: str, content: list):
    create_dir_if_not_exist(os.path.dirname(path))
    with open(path, 'w', encoding='utf-8')as f:
        text = '\n'.join(content)
        f.write(text)


def append_all_text(path: str, content: str):
    with open(path, 'a', encoding='utf-8')as f:
        f.write(content)


def append_all_texts(path: str, content: list):
    with open(path, 'a', encoding='utf-8')as f:
        text = '\n'.join(content)
        f.write(text)


def create_dir_if_not_exist(path: str):
    if path == '':
        return
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == "__main__":
    write_all_text('1.txt', '123')
