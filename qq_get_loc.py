#!/usr/bin/python3

import requests
import json
from time import sleep
from sys import argv
from functools import lru_cache
from pathlib import Path

from read_key import read_key

key = read_key()['qq']
decode_url = 'https://apis.map.qq.com/ws/geocoder/v1/'
search_url = 'https://apis.map.qq.com/ws/place/v1/search'
address = list()

def get_address_list(list_file: Path) ->list:
    # each line for one address, must be utf-8
    address_list = list()
    with open(list_file, 'r', encoding='utf-8') as raw:
        for line in raw:
            address_list.append(line.strip())
    return address_list


@lrucache(maxsize=None)
def get_loc(query: str, key: str):
    r = requests.get(decode_url, params={'address': i, 'output': 'json',
                                         'key': key})
                     # proxies={'http': '127.0.0.1:1080'},
    if r.status_code == 200:
        print(r.content)
    else:
        print(r.status_code, i, r.text.decode('utf8'))
    return r.json()
    # five times per second


def main():
    input_file = Path(argv[1])
    out_file = input_file.with_suffix('.json')
    all_result = list()
    address_list = get_address_list(input_file)
    for index, address in enumerate(address_list):
        print(index, address)
        result = get_loc(address, key)
        all_result.append(result)
        sleep(0.22)
    with open(out_file, 'w', encoding='utf-8') as out:
        json.dump(all_result, out)
    return


if __name__ == '__main__':
    main()
