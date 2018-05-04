#!/usr/bin/python3

from glob import glob

with open('./qlr.xml', 'r') as _:
    qlr_template = _.read()
with open('./layer.xml', 'r') as _:
    layer_template = _.read()
with open('./maplayer.xml', 'r') as _:
    maplayer_template = _.read()
files = list(glob('/home/ping/work/map/1-100wan/*.zip'))
layers = 'HYDA HYDL HYDP RESA RESP LRRL LRDL BOUA BOUL BOUP AGNP AANP'.split(' ')
n = 0
for layer_name in layers:
    layer_str = ''
    maplayer_str = ''
    for path in files:
        layer_str += layer_template.format(layer_id=n, path=path,
                                           layer_name=layer_name,
                                           name=str(n)+'-'+layer_name)
        maplayer_str += maplayer_template.format(layer_id=n, path=path,
                                                 layer_name=layer_name)
        n += 1
    with open('{}.qlr'.format(layer_name), 'w') as out:
        out.write(qlr_template.format(layer_str=layer_str,
                                      maplayer_str=maplayer_str))
