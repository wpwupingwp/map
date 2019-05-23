#!/usr/bin/python3

import re
from sys import argv

print('usage: python3 degree2decimal.py csv_file')
print('csv format: name,lat,long')

with open(argv[1], 'r') as _:
    raw = _.readlines()
raw = [i.strip().split(',') for i in raw]
pattern = re.compile(r'\d+\.?\d*')
clean = [raw[0], ]
decimal = [raw[0], ]
for idx, record in enumerate(raw[1:]):
    print(idx, end=',')
    name = record[0]
    a = re.findall(pattern, record[1])
    a = [float(i) for i in a]
    if len(a) == 1:
        a = [a[0], 0, 0]
    elif len(a) == 2:
        a = [a[0], a[1], 0]
    print(a, end=',')
    a_d = a[0] + a[1]/60 + a[2]/60/60
    b = re.findall(pattern, record[2])
    b = [float(i) for i in b]
    if len(b) == 1:
        b = [b[0], 0, 0]
    elif len(b) == 2:
        b = [b[0], b[1], 0]
    print(b)
    b_d = b[0] + b[1]/60 + b[2]/60/60
    clean.append([name, a, b])
    decimal.append([name, a_d, b_d])
with open(argv[1]+'.clean', 'w') as out:
    out.write(','.join(clean[0])+'\n')
    for i in clean[1:]:
        out.write("""{},{}°{}'{}",{}°{}'{}"\n""".format(i[0], *i[1], *i[2]))
with open(argv[1]+'.decimal', 'w') as out:
    out.write(','.join(clean[0])+'\n')
    for i in decimal[1:]:
        out.write('{},{},{}\n'.format(*i))


