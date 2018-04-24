#!/usr/bin/python3

import requests
import json

address = list()
with open('./failed.csv', 'r') as raw:
#with open('./test.csv', 'r') as raw:
    for line in raw:
        address.append(line.strip())
result = dict()
for i, j in enumerate(address):
    print(j)
    if i in (2000, 4000):
        pause = input('pause')
    post = ('{{"keyWord":{},"level":"11","mapBound":"-180,-90,180,90",'
            '"queryType":"1","count":"1"}}'.format(j))

    r = requests.get('http://www.tianditu.com/query.shtml',
                     params={'postStr': post, 'type': 'query'})
    if r.status_code == 200:
        result[j] = r.json()
    print(r.status_code, j, r.text)
with open('tianditu.result.json', 'w') as out:
    json.dump(result, out)
