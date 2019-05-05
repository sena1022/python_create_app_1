import json
import time
from urllib.request import Request, urlopen  #python 3
from urllib.parse import urlencode, quote_plus

from fluent import sender
from fluent import event


def run():
    max_retries = 7
    retries  = 0
    today = datetime.today().strftime("%Y%m%d")

    while True:
        try:
            if retries >= max_retries:
                print(today, '-> Data.go.kr API Call Error!!!')
                return

            hira_url = 'http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList'
            ServiceKey = '2UWvNIvNmrdJQKq4OhO3sipd2S7NO36m1bCqJi61wdShwJIp1Wg5D%2FAEanZ97vZAydIS%2FN9eL418xqyN7J0vzw%3D%3D'
            queryParams = '?' + 'serviceKey=' + ServiceKey + '&_type=json&numOfRows=10'
            # queryParams = '?numOfRows=70000&pageNo=1&ServiceKey=%s&_type=json'%(service_key)

            request = Request(hira_url + queryParams)
            request.get_method = lambda: 'GET'
            response = urlopen(request)

            if response.getcode() == 200: #urllib.request.urlopen().getcode() 의 결과값 status: 200 이면 잘 연결되었다는 뜻
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



            #컬럼 제한 했으니 제한 없게

            
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




def all_hira_data():

    print(hira_url + queryParams)
    # r = requests.get(hira_url + queryParams)
    resp = dict(json.loads(r.text))
    with io.open('./csv/hira.json', 'w', encoding='utf8') as outfile:
        str_ = json.dumps(resp,
                          indent=4, sort_keys=True,
                          separators=(',', ': '), ensure_ascii=False)
        outfile.write(to_unicode(str_))
    with open('./csv/hira.json') as data_file:
        data_loaded = json.load(data_file)

    print(resp == data_loaded)

    return resp
