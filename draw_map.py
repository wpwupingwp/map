#!/usr/bin/python3

import requests
import json
from sys import argv


def google(query, key):
    """
    Input: query, key
    Output: png map
    """
    species, loc = query
    loc_str = ['{:.6f},{:.6f}'.format(*i) for i in loc]
    markers = '|'.join(loc_str)
    print(markers)
    draw_url = 'https://maps.google.cn/maps/api/staticmap'
    r = requests.get(draw_url,
                     params={'input': query,
                             'markers': markers,
                             'size': '640x640',
                             'scale': 2,
                             'format': 'png',
                             'maptype': 'terrain',
                             'center': 'China',
                             'language': 'zh-CN',
                             'region': 'cn',
                             'key': key})
    if r.status_code == 200:
        png = r.content
        with open(species+'.png', 'wb') as out:
            out.write(png)
    return r.status_code


# get key
with open('key', 'r') as raw:
    a = raw.readlines()
    key = a[2].strip().split(' ')[1]
# get query list
with open(argv[1], 'r') as raw:
    data = json.load(raw)
failed = dict()
for i in data.items():
    result = google(i, key)
    if result != 200:
        failed[i[0]] = i[1]
with open('failed.json', 'w') as out:
    json.dump(failed, out)
