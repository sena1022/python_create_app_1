import urllib.request
import urllib.parse
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

API = "https://tvetamovie.pstatic.net/libs/1222/1222741/33ed1d7d9c75df6628c8_20190425163559580.mp4-pBASE-v0-f79898-20190425163825053_1.mp4"

savePath3 ="C:/Users/lilia/Desktop/inflearn/web crawling/section2/test1.mp4"

f3 = urllib.request.urlopen(API).read()

with open(savePath3,'wb') as saveFile3: #with를 씀으로써 close를 안 해도 됨
    saveFile3.write(f3)
