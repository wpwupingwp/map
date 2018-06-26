#!/usr/bin/python3

from sys import argv
import json

with open(argv[1], 'r') as _:
    data = json.load(_)

with open(argv[1]+'.csv', 'w') as out:
    for i in data:
        for j in data[i]:
            out.write('{},{},{}\n'.format(i, j[0], j[1]))
