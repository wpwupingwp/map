#!/usr/bin/python3

import requests
import json
from time import sleep

address = list()
with open('./test.csv', 'r') as raw:
#with open('./test.csv', 'r') as raw:
    for line in raw:
        address.append(line.strip())
address_dict = {i: False for i in address}
result = dict()
for index, i in enumerate(address):
    print(index, i)
    r = requests.get('http://apis.map.qq.com/ws/geocoder/v1/',
                     params={'address': i,
                             'output': 'json',
                             'key': '2KHBZ-BTQAK-ADUJH-AXMTA-5H5L3-CPFI6'})

    if r.status_code == 200:
        result[i] = r.json()
        address_dict[i] = True
    else:
        print(r.status_code, i, r.text)
    sleep(0.22)
with open('address_dict.json', 'w') as out:
    json.dump(address_dict, out)
with open('result.0424.json', 'w') as out:
    json.dump(result, out)
