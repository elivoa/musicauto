'''
这个脚本用来将CUE文件和WAV文件分离

usage:
    python auto_split_cue.py <folder>

example:
    python auto_split_cue.py /Users/bogao/Downloads/2020 ABC德国制 《克雷莫纳的荣耀·绝世十二把大提琴》 6N纯银镀膜 [WAV+CUE]

'''
import sys
import os
import codecs
import subprocess
import chardet


# folder = '/opt/dangers/music_gogogo____[KEEP_EMPTY]/科冈的传奇(Arlecchino_现有17CD)'
FOLDER = '/Users/bogao/Downloads/2020 ABC德国制 《克雷莫纳的荣耀·绝世十二把大提琴》 6N纯银镀膜 [WAV+CUE]'


def encodepath(path):
    ''' 将路径中的特殊字符转换为转义字符 '''

    path = path.replace(' ', r'\ ')
    path = path.replace('[', r'\[')
    path = path.replace(']', r'\]')
    path = path.replace('(', r'\(')
    path = path.replace(')', r'\)')
    path = path.replace('&', r'\&')
    return path
    # return re.sub(r'([\[\] ])', r'\\\1', path)


def convert_to_utf8(file_path):
    ''' 将CUE文件转换为UTF-8格式; return processed, newcue'''

    # 检测文件编码
    newcue = file_path + '.utf8.cue'
    if os.path.exists(newcue):
        return True, newcue
    # print("...", file_path)

    with open(file_path, 'rb') as f:
        content = f.read()
        result = chardet.detect(content)
        encoding = result['encoding']

    # 如果文件编码不是UTF-8，则另存为UTF-8格式
    if encoding != 'utf-8':
        if encoding.lower() == 'gb2312':
            encoding = 'gb18030'
        print('open with : ', encoding)
        with codecs.open(file_path, 'r', encoding) as f:
            content = f.read()

        with codecs.open(newcue, 'w', 'utf-8') as f:
            f.write(content)
        return False, newcue
    else:
        return False, file_path


def auto_split_cue(folder):
    ''' 自动分割CUE文件 '''

    for root, dirs, files in os.walk(folder):
        cuefile = None
        targetfile = None
        for file in files:
            basename, extension = os.path.splitext(file)
            extension = extension.lower()

            if extension == '.cue':
                cuefile = file
            elif extension == '.flac':
                targetfile = file
            elif extension == '.wav':
                targetfile = file

        if cuefile and targetfile:
            # print(f"\n>> {root}\n\t{cuefile}\n\t{targetfile}")

            # transfer cue
            already_processed, newcue = convert_to_utf8(f'{root}/{cuefile}')
            if already_processed:
                print(f"❯ Skip Folder (Already Converted): {root}")
                continue

            if not newcue:
                print(f"❯ Skip Folder (Bad CUE files): {root}")
                continue

            # print info
            print(f"\n❯ Found Music Folder: {root}")
            print(f"  - CUE   File: {cuefile}")
            print(f"  - Track File: {targetfile}")

            cuepath = encodepath(newcue)
            targetpath = encodepath(root+'/'+targetfile)
            rrr = encodepath(root)

            cmd = f'shntool split -t "%n %t" -o flac -f {cuepath} -d {rrr} {targetpath}'

            print("  Converting...")

            with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
                while True:
                    output = process.stdout.readline()
                    if output == b'' and process.poll() is not None:
                        break
                    if output:
                        print(f"  Identify CUE :{output.strip().decode()}")

            print("  Command:", cmd)
            print("  Convert Success!")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python auto_split_cue.py <folder>')
        exit(0)

    FOLDER = sys.argv[1]
    auto_split_cue(FOLDER)
