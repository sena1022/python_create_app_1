# https://github.com/nficano/pytube
#pip install pytube
# https://docs.python.org/3.6/library/subprocess.html
#
# 윈도우 : http://www.filehorse.com/download-ffmpeg-64/


import os
import subprocess

import pytube

yt = pytube.YouTube("https://www.youtube.com/watch?v=WH7xsW5Os10") #�ٿ����� ������ URL ����

videos= yt.streams.all()

#���� ���� ����Ʈ Ȯ��
for i in range(len(videos)):
    print(i,'. ',videos[i])

# vnum = int(input("�ٿ� ���� ȭ����? "))

down_dir = "C:/Users/lilia/Desktop/inflearn/web crawling/section2/download"
videos[0].download(down_dir)
# vids[vnum].download(down_dir) #�ٿ��ε� ����
#
# new_filename = input("��ȯ �� mp3 ���ϸ���?")
#
# default_filename = vids[vnum].default_filename
# subprocess.call(['ffmpeg', '-i',                 #cmd ���ɾ� ����
#     os.path.join(parent_dir, default_filename),
#     os.path.join(parent_dir, new_filename)
# ])
#
# print('������ �ٿ��ε� �� mp3 ��ȯ �Ϸ�!')
