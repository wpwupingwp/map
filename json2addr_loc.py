#!/usr/bin/python3

import json
from sys import argv

with open(argv[1], 'r') as raw:
    a = raw.readlines()
good = open(argv[1]+'.good.json', 'w')
bad = open(argv[1]+'.bad.json', 'w')
addr_loc = dict()
for i in a:
    record = json.loads(i)
    raw_addr, addr, js = record
    if js['status'] == 'OK':
        loc = list(js['results'][0]['geometry']['location'].values())
        addr_loc[raw_addr] = loc
        good.write(i)
    else:
        bad.write(i)
with open(argv[1]+'.addr_loc.json', 'w') as out:
    json.dump(addr_loc, out)
print('Total:\t{} records.'.format(len(a)))
print('Good geocoding results:\t{}'.format(len(addr_loc)))
print('Bad geocoding results:\t{}'.format(len(a)-len(addr_loc)))
