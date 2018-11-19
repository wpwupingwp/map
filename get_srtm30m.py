#!/usr/bin/python3

import requests

for i in range(50, 64):
    for j in range(1, 11):
        url = ('http://srtm.csi.cgiar.org/SRT-ZIP/SRTM_V41/SRTM_Data_GeoTiff/'
               'srtm_{}_{:02d}.zip'.format(i, j))
        print(url)
        r = requests.get(url, proxies={'http': 'http://127.0.0.1:1080'})
        print(r.status_code)
        if r.status_code == 200:
            with open(url.split('/')[-1], 'wb') as out:
                out.write(r.content)
