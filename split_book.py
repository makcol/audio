# -*- coding: utf-8 -*-
# __author__:'Administrator'
# @Time    : 2018/8/31 14:19
import os

dst = "./"  # 生成文件目录

template = '''
    <speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts"
       xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
    <mstts:backgroundaudio src="https://bgm5.b-cdn.net/kongbubgm.mp3" volume="0.3"/>
    <voice name="zh-CN-YunyeNeural">
        <prosody rate="-12%" pitch="0%">{}</prosody>
    </voice>
</speak>
    '''


# 将一个txt文件的内容，按照第几章进行分割
def SplitFile(file_path1, dst):
    with open(file_path1, 'rb') as f1:
        # 获取文件每一行
        lines1 = f1.readlines()
        # 获取file的名称
        file_dir1 = file_path1.replace("\\", '/').split("/")[-1].split(".")[0]
        path1 = os.path.join(dst, file_dir1)
        if not os.path.exists(path1):
            os.makedirs(path1)
        i = 0
        for line in lines1:
            try:
                if ('第' in line.decode(encoding='utf-8') and "章" in line.decode(encoding='utf-8')) or (
                        "第" in line.decode(encoding='utf-8') and "章..." in line.decode(encoding='utf-8')) or (
                        "第" in line.decode(encoding='utf-8') and "章\r\n" in line.decode(encoding='utf-8')):
                    name = line.strip().decode('utf8')
                    i += 1
                file_name1 = os.path.join(path1, "%s_%s.txt" % (i - 1, name))
                fp = open(file_name1, 'ab+')
                fp.write(line)
                fp.close()
            except Exception as e:
                print(e)


def split(name):
    SplitFile("{}.txt".format(name), dst)


if __name__ == '__main__':
    split('盗墓笔记2：秦岭神树 作者：南派三叔')
