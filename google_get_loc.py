#!/usr/bin/python3

import json
from sys import argv
from functools import lru_cache
from pathlib import Path

import requests

from read_key import read_key


key = read_key()['google']
proxy = {'http': '127.0.0.1:1080'}


def get_address_list(list_file: Path) -> list:
    # get query list
    # Format:
    # Country,Province,City,Detail
    address_list = []
    with open(argv[1], 'r', encoding='utf8') as _:
        for line in _:
            address_list.append(line.strip())
    return address_list


@lru_cache(maxsize=0)
def google(query: str, key: str) -> 'json':
    """
    Input: query, key
    Output: json()
    """
    place_url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json'
    geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    r = requests.get(place_url,
                     params={'input': query, 'language': 'zh-CN', 'key': key},
                     proxies=proxy)
    if r.status_code == 200:
        autocomplete = r.json()
    else:
        return {'status': r.status_code}
    if autocomplete['status'] == 'OK':
        place_id = autocomplete['predictions'][0]['place_id']
        r2 = requests.get(geocode_url, params={'place_id': place_id,
                                               'key': key})
    else:
        r2 = requests.get(geocode_url, params={'address': query,
                                               'key': key})
    js = r2.json()
    return js


def main():
    input_file = Path(argv[1])
    out_file = input_file.with_suffix('.json')
    all_result = list()
    address_list = get_address_list(Path(argv[1]))
    for index, address in enumerate(address_list):
        print(index, address)
        addr_list = address.split(',')
        query = ','.join(addr_list)
        js = google(query, key)
        while js['status'] != 'OK' and len(addr_list) != 0:
            addr_list.pop()
            query = ','.join(addr_list)
            print('\t', query)
            js = google(query, key)
            if js['status'] == 'OK':
                result = [address, query, js]
                break
            else:
                result = [address, '', '']
        all_result.append(result)
    with open(out_file, 'w', encoding='utf-8') as out:
        json.dump(result, out)
    return


if __name__ == '__main__':
    main()
