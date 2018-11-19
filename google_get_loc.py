#!/usr/bin/python3

import requests
import json
import re
from sys import argv


def google(query, place_key, geocode_key):
    """
    Input: query, place_key, geocode_key
    Output: json()
    """
    place_url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json'
    geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    r = requests.get(place_url, params={'input': query, 'language': 'zh-CN',
                                        'key': place_key})
    if r.status_code == 200:
        autocomplete = r.json()
    else:
        return {'status': r.status_code}
    if autocomplete['status'] == 'OK':
        place_id = autocomplete['predictions'][0]['place_id']
        r2 = requests.get(geocode_url, params={'place_id': place_id,
                                               'key': geocode_key})
    else:
        r2 = requests.get(geocode_url, params={'address': query,
                                               'key': geocode_key})
    js = r2.json()
    return js


# get key
with open('key', 'r') as key:
    place_key = key.readline().strip().split(' ')[1]
    geocode_key = key.readline().strip().split(' ')[1]
# get query list
# Format:
# Name,Country,Province,City,Detail
with open(argv[1], 'r') as _:
    raw = _.readlines()
    raw2 = [i.strip().split(',') for i in raw]
    name_address = [[i[0], ','.join(i[1:])] for i in raw2]
address_dict = {i[1]: 0 for i in name_address}
total = len(address_dict)

out = open(argv[1]+'.json', 'w')
for index, address_str in enumerate(list(address_dict.keys())):
    addr_list = address_str.split(',')
    query = ','.join(addr_list)
    print('{} of {}, {}'.format(index, total, query))
    js = google(query, place_key, geocode_key)
    while js['status'] != 'OK' and len(addr_list) != 0:
        addr_list.pop()
        query = ','.join(addr_list)
        print('\t', query)
        js = google(query, place_key, geocode_key)
    if js['status'] == 'OK':
        result = [address_str, query, js]
    else:
        continue
    print('\t', result[2]['status'])
    json.dump(result, out)
    out.write('\n')
    out.flush()
