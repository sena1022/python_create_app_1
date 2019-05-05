import urllib.request
from urllib.parse import urlparse
import sys
import io


sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

url = "http://www.encar.com/"

mem = urllib.request.urlopen(url)

print(type(mem))
print("geturl :",mem.geturl())  #결과 : http://www.encar.com/index.do
print("status :",mem.status)  #응답코드 200 (정상), 404(요청페이지 없음), 403 (Reject), 500 (서버 에러)
print("headers :",mem.getheaders())
print("info :",mem.info(),"\n")   #== headers
print("getcode :",mem.getcode())  #== status
print("read :",mem.read(10).decode('utf-8')) #해당 숫자만큼 불러옴
print(urlparse('http://www.encar.co.kr?test=test').query)
