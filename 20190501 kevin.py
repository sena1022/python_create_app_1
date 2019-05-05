import json
import time
from fluent import sender
from fluent import event
from datetime import datetime
import requests
try:
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request
try:
    from urllib import urlencode, quote_plus
except ImportError:
    from urllib.parse import urlencode, quote_plus

def run():
    max_retries = 7
    retries  = 0
    today = datetime.today().strftime("%Y%m%d")

    while True:
        try:
            if retries >= max_retries:
                print(today, '-> Data.go.kr API Call Error!!!')
                return

            url = 'http://apis.data.go.kr/B551182/pharmacyInfoService/getParmacyBasisList'
            queryParams = '?' + 'serviceKey=' + '0iL736RveVYyQp%2F99eV2vwEyvArFlIW4cPcPfSZd7sRb0tDE3wbwQTZrmZt3mxB55AOU9HQC3uiA6e%2F8oqt%2FCQ%3D%3D&_type=json&numOfRows=100000'

            request = Request(url + queryParams)
            request.get_method = lambda: 'GET'
            response = urlopen(request)
            if response.getcode() == 200:
                response_body = response.read()
                pharm_json_rt = response_body.decode('utf-8')
                pharm_items = json.loads(pharm_json_rt)
                print(today, '-> 약국 API호출통해 받은 건수 : ', pharm_items['response']['body']['totalCount'])
            else:
                print(today, '-> 약국 API호출 result : ',  response.getcode())
                retries += 1
                wait = 2 ** (retries - 1)
                time.sleep(wait)
                continue

            url = 'http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList'
            queryParams = '?' + 'serviceKey=' + '0iL736RveVYyQp%2F99eV2vwEyvArFlIW4cPcPfSZd7sRb0tDE3wbwQTZrmZt3mxB55AOU9HQC3uiA6e%2F8oqt%2FCQ%3D%3D&_type=json&numOfRows=100000'

            request = Request(url + queryParams)
            request.get_method = lambda: 'GET'
            response = urlopen(request)
            if response.getcode() == 200:
                response_body = urlopen(request).read()
                hosp_json_rt = response_body.decode('utf-8')
                hosp_items = json.loads(hosp_json_rt)
                print(today, '-> 병원 API호출통해 받은 건수 : ', hosp_items['response']['body']['totalCount'])
            else:
                print(today, '-> 병원 API호출 result : ',  response.getcode())
                retries += 1
                wait = 2 ** (retries - 1)
                time.sleep(wait)
                continue

            sender.setup('td.hira', host='localhost', port=24224)
            print(today, '-> sender.setup ok ')
            tot = 0
            for item in pharm_items['response']['body']['items']['item']:
                tot = tot + 1
                item['inputDate'] = today
                item['inputType'] = '약국'
                event.Event('getParmacyBasisList_getHospBasisList', item)
                if tot % 5000 == 0:
                    print(today, '-> TD 전송 약국진행건수 : ', tot)
            print(today, '-> TD 전송 약국완료건수 : ', tot)

            tot = 0
            for item in hosp_items['response']['body']['items']['item']:
                tot = tot + 1
                item['inputDate'] = today
                item['inputType'] = '병원'
                event.Event('getParmacyBasisList_getHospBasisList', item)
                if tot % 5000 == 0:
                    print(today, '-> TD 전송 병원진행건수 : ', tot)
            print(today, '-> TD 전송 병원완료건수 : ', tot)
            sender.close()
            break
        except:
            retries += 1
            wait = 2**(retries - 1)
            time.sleep(wait)
def isEnableStatus(url):
    max_retries = 5
    retries  = 0
    today = datetime.today().strftime("%Y%m%d")
    while True:
        try:
            print(today, '-> Retrieving {0}...'.format('Data.go.kr API Test Call~~'))
            response = requests.get(url)
            print(today, '-> Status {0}'.format(response.status_code))
            if response.status_code == 200:
                return response # 일시적인 오류가 아니라면 response를 반환합니다.
        except requests.exceptions.RequestException as ex:
            # 네트워크 레벨 오류의 경우 재시도합니다.
            print(today, '-> Exception occured: {0}'.format(ex))
            retries += 1
            if retries >= max_retries:
                #raise Exception('Too many retries.')
                response.status_code = 404
                return response
            wait = 2**(retries - 1)
            print(today, '-> Waiting {0} seconds...'.format(wait))
            time.sleep(wait)

def main():
    today = datetime.today().strftime("%Y%m%d")
    url = 'http://apis.data.go.kr/B551182/pharmacyInfoService/getParmacyBasisList'
    queryParams = '?' + 'serviceKey=' + '0iL736RveVYyQp%2F99eV2vwEyvArFlIW4cPcPfSZd7sRb0tDE3wbwQTZrmZt3mxB55AOU9HQC3uiA6e%2F8oqt%2FCQ%3D%3D&_type=json&numOfRows=1'
    response = isEnableStatus(url + queryParams)
    if response.status_code == 200:
        print(today, '-> Data.go.kr API Call Test OK!!!')
        run()
    else:
        print(today, '-> Data.go.kr API Call Error!!!')

if __name__ == '__main__':
    main()

# 한번에 호출해서 끝낼수 있는 데이타인듯해서 한번에 처리. (페이지별, 병원/약국별로 나눠처리하게 로직처리 필요함
# 서버자체나 네트웍문제시 재시도를 통해 가능상태인것을 체크후 처리
