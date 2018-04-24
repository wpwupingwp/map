#!/usr/bin/python3

import re

with open('./city.csv', 'r') as raw:
    a = raw.readlines()
a = [i.strip() for i in a]
b = set(a)
pattern = r'\W'
result = list()
for i in b:
    match = re.search(pattern, i)
    if match is not None:
        result.append(re.sub(r'\W|td', '', i))
s = set(result)
print(len(a), len(b), len(result), len(s))
with open('clean.csv', 'w') as out:
    for i in s:
        out.write(i+'\n')
