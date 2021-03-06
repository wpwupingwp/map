#!/usr/bin/python3

import requests
import json
from time import sleep
from sys import argv

address = list()
with open(argv[1], 'r') as raw:
    for line in raw:
        address.append(line.strip().split(','))
address_dict = {i[1]: False for i in address}
result = dict()
for index, i in enumerate(address):
    print(index, i)
    r = requests.get('https://apis.map.qq.com/ws/geocoder/v1/',
#                     proxies={'http': '127.0.0.1:1080'},
                     params={'address': i[1],
                             'output': 'json',
                             'key': '2KHBZ-BTQAK-ADUJH-AXMTA-5H5L3-CPFI6'})

    if r.status_code == 200:
        print(r.content)
        result[i[0]] = r.json()
        address_dict[i[1]] = True
    else:
        print(r.status_code, i, r.text.decode('utf-8'))
    sleep(0.22)
with open(argv[1]+'_address_dict.json', 'w') as out:
    json.dump(address_dict, out)
with open(argv[1]+'.json', 'w') as out:
    json.dump(result, out)
