import codecs
import os
import re
import subprocess
import chardet
import sys


def encodepath(path):
    path = path.replace(' ', '\ ')
    path = path.replace('[', '\[')
    path = path.replace(']', '\]')
    path = path.replace('(', '\(')
    path = path.replace(')', '\)')
    path = path.replace('&', '\&')
    return path
    # return re.sub(r'([\[\] ])', r'\\\1', path)


def convert_to_utf8(file_path):
    # 检测文件编码

    newcue = file_path + '.utf8.cue'
    if os.path.exists(newcue):
        return newcue
    # print("...", file_path)

    with open(file_path, 'rb') as f:
        content = f.read()
        result = chardet.detect(content)
        encoding = result['encoding']

    # 如果文件编码不是UTF-8，则另存为UTF-8格式
    if encoding != 'utf-8':
        with codecs.open(file_path, 'r', encoding) as f:
            content = f.read()

        with codecs.open(newcue, 'w', 'utf-8') as f:
            f.write(content)


def detect_and_convert_cue_encoding(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            basename, extension = os.path.splitext(file)
            if extension == '.cue':
                cuepath = os.path.join(root, file)
                convert_to_utf8(cuepath)


def main():
    if len(sys.argv) < 2:
        print('Usage: python auto_split_cue.py <folder>')
        return

    folder = sys.argv[1]
    detect_and_convert_cue_encoding(folder)


if __name__ == '__main__':
    main()
