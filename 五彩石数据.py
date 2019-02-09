import urllib.request
import urllib.parse
import json
import time
import sys


def get_data(url, headers):
    request = urllib.request.Request(url, headers = headers)
    while True:
        try:
            response = urllib.request.urlopen(request, timeout = 5)
        except:
            print('ERR')
            continue
        else:
            break
    return response.read().decode()

def parse_get(data):
    return '?' + urllib.parse.urlencode(data)

def refresh_headers(zhiye):
    return {'Referer':rf'https://www.j3pz.com/dps/{zhiye}/',
           'User-Agent':r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

api = r'https://www.j3pz.com/api/stone'
headers = {'Referer':rf'https://www.j3pz.com/dps/tianluo/',
           'User-Agent':r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

with open(r'data.csv',mode='w') as f:
    f.write('name,id,attr1,value1,attr2,value2,attr3,value3\n')
    #for i in range(3,2702,3):
    for iters in (range(3,1594,3),
                  (1595,1597,1598,1600,1602,1604,1607,1610,1612),
                  range(1615,2702,3)):
        for i in iters:
            temp = get_data(api+r'/'+str(i), headers)
            attr = json.loads(temp)['data']
            f.write('%s,%s,%s,%s,%s,%s,%s,%s\n'%(attr['name'],
                                                        attr['id'],
                                                        attr['attr'][0]['attribute'],
                                                        attr['attr'][0]['number'],
                                                        attr['attr'][1]['attribute'],
                                                        attr['attr'][1]['number'],
                                                        attr['attr'][2]['attribute'],
                                                        attr['attr'][2]['number'],))
            print(attr['name'],attr['id'])
