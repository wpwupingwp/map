#!/usr/bin/python3

import re

with open('./uniq.csv', 'r') as _:
    a = _.readlines()

a = [i.strip() for i in a]
pattern = r'(<td>|\,{1,3}|")'
b = {}
for i in a:
    b[i] = re.sub(pattern, ' ', i)
with open('table.csv', 'w') as out:
    for i in b:
        out.write(i+'\t\t\t'+b[i]+'\n')
