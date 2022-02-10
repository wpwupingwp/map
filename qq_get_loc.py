#!/usr/bin/python3

import requests
import json
from functools import lru_cache
from hashlib import md5
from pathlib import Path
from sys import argv
from time import sleep

from read_key import read_key

qq_key = read_key()['qq']
baidu_key = read_key()['baidu']
decode_url = 'https://apis.map.qq.com/ws/geocoder/v1/'
search_url = 'https://apis.map.qq.com/ws/place/v1/search'
proxy = {'http': 'http://127.0.0.1:1080'}
address = list()


def get_address_list(list_file: Path) -> list:
    # each line for one address, must be utf-8
    address_list = list()
    with open(list_file, 'r', encoding='utf-8') as raw:
        for line in raw:
            address_list.append(line.strip())
    return address_list


@lru_cache(maxsize=None)
def translate(query: str, key: str) -> str:
    url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    app_id = '20220210001079060'
    salt = 'baidu'
    sign_str = ''.join([app_id, query, salt, key])
    sign = md5(sign_str.encode('utf-8')).hexdigest()
    r = requests.get(url, params={'q': query, 'from': 'auto', 'to': 'zh',
                                  'appid': app_id, 'salt': salt, 'sign': sign})
    # print(r.url)
    result = r.json()
    dst = result['trans_result'][0]['dst']
    print('\t', dst)
    return dst


@lru_cache(maxsize=None)
def get_loc(query: str):
    zh = translate(query, baidu_key)
    r = requests.get(decode_url, params={'address': zh, 'output': 'json',
                                         'key': qq_key}, timeout=1)
    # print(r.url)
    if r.status_code == 200:
        result = r.json()
        lng = result['result']['location']['lng']
        lat = result['result']['location']['lat']
        print(query, lng, lat)
        return query, lng, lat
    else:
        return [query, '', '']


def main():
    input_file = Path(argv[1])
    out_file = input_file.with_suffix('.json')
    all_result = list()
    address_list = get_address_list(input_file)
    for index, address in enumerate(address_list):
        print(index, address)
        result = get_loc(address)
        all_result.append(result)
        sleep(0.2)
    with open(out_file, 'w', encoding='utf-8') as out:
        json.dump(all_result, out)
    return


if __name__ == '__main__':
    main()
