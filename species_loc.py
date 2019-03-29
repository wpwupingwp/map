#!/usr/bin/pythonk

import argparse
import json
from collections import defaultdict


def parse_args():
    arg = argparse.ArgumentParser(description=main.__doc__)
    arg.add_argument('-json', help='Geocoding result file (json)')
    arg.add_argument('-csv', help='Species-Address csv file')
    arg.add_argument('-out', help='output directory')
    arg.print_help()
    return arg.parse_args()


def get_addr_loc(arg):
    with open(arg.json, 'r') as _:
        raw = _.readlines()
    addr_loc = dict()
    # good = open(arg.json+'.good.json', 'w')
    # bad = open(arg.json+'.bad.json', 'w')
    bad_n = 0
    for i in raw:
        record = json.loads(i)
        raw_addr, addr, js = record
        if js['status'] == 'OK':
            # [latitude, longitude]
            loc = list(js['results'][0]['geometry']['location'].values())
            addr_loc[addr] = loc
            # good.write(i)
        else:
            bad_n += 1
            # bad.write(i)
    return addr_loc, bad_n


def main():
    arg = parse_args()
    if arg.out is None:
        arg.out = arg.csv + '.result'

    species_loc = defaultdict(list)
    addr_loc, bad_loc = get_addr_loc(arg)
    with open(arg.csv, 'r') as _:
        raw = _.readlines()
    for rawline in raw:
        line = rawline.strip().split(',')
        species = line[0]
        place = ','.join(line[1:])
        if place not in addr_loc:
            # skip bad address
            continue
        species_loc[species].append(addr_loc[place])
    with open(arg.out, 'w') as out:
        json.dump(species_loc, out)
    with open(arg.out+'.csv', 'w') as out:
        for i in species_loc:
            for j in species_loc[i]:
                out.write('{},{},{}\n'.format(i, j[0], j[1]))
    print('{} records.'.format(len(raw)))
    print('{} species.'.format(len(species_loc)))
    print('Good geocoding results:\t{}'.format(len(addr_loc)))
    print('Bad geocoding results:\t{}'.format(bad_loc))


if __name__ == '__main__':
    main()
