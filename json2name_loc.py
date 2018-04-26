#!/usr/bin/python3

import json
from sys import argv

with open(argv[1], 'r') as raw:
    a = raw.readlines()
locs = list()
for i in a:
    record = json.loads(i)
    raw_addr, addr, js = record
    loc = list(js['results'][0]['geometry']['location'].values())
    locs.append(loc)
result = {argv[1]: locs}
json.dump(result, open(argv[1]+'.converted.json', 'w'))
