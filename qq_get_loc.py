#!/usr/bin/python3

import requests
import json
from time import sleep
from sys import argv

from read_key import read_key

key = read_key()['qq']
decode_url = 'https://apis.map.qq.com/ws/geocoder/v1/'
search_url = 'https://apis.map.qq.com/ws/place/v1/search'
address = list()
# each line for one address, must be utf-8
with open(argv[1], 'r', encoding='utf-8') as raw:
    for line in raw:
        address.append(line.strip())
address_dict = {i: False for i in address}
result = dict()
for index, i in enumerate(address):
    print(index, i)
    r = requests.get(decode_url, params={'address': i, 'output': 'json',
                                         'key': key})
                     # proxies={'http': '127.0.0.1:1080'},
    if r.status_code == 200:
        print(r.content)
        result[i] = r.json()
        address_dict[i] = True
    else:
        print(r.status_code, i, r.text.decode('utf8'))
    # five times per second
    sleep(0.22)
with open(argv[1]+'_address_dict.json', 'w') as out:
    json.dump(address_dict, out)
with open(argv[1]+'.json', 'w') as out:
    json.dump(result, out)
