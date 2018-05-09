#!/usr/bin/python3

from json import load
from mpl_toolkits.basemap import Basemap
from sys import argv
import matplotlib.pyplot as plt

wgs84 = 4326
south_china_sea = 3415
xi_an = (108.886, 34.265)
map = Basemap(epsg=south_china_sea, lat_0=xi_an[1], lon_0=xi_an[0],
              llcrnrlon=80, llcrnrlat=-2, urcrnrlon=140,
              urcrnrlat=55)

data = load(open(argv[1], 'r'))
for species in data:
    # ax.axis('off')
    plt.figure(figsize=(20, 20))
    map.readshapefile('/home/ping/work/map/Basemap/nation', 'nation',
                      drawbounds=True, linewidth=2, color='#000000')
    map.readshapefile('/home/ping/work/map/Basemap/province', 'province',
                      drawbounds=True, linewidth=1, color='#222222')
    map.readshapefile('/home/ping/work/map/Basemap/river', 'river',
                      drawbounds=True, linewidth=1, color='#189EEC')
    map.readshapefile('/home/ping/work/map/Basemap/lake', 'lake',
                      drawbounds=True, linewidth=1, color='#189EEC')
    map.drawmeridians(range(80, 140, 10),  labels=(0, 0, 1, 1),  fontsize=15)
    map.drawparallels(range(0, 80, 10),  labels=(1, 1, 0, 0),  fontsize=15)
    loc = data[species]
    lat_list = [i[0] for i in loc]
    lon_list = [i[1] for i in loc]
    x, y = map(lon_list, lat_list)
    label = '$\it{{{}}}$'.format(species.replace(' ', '\ '))
    plt.scatter(x, y, marker='o', color='r', s=15, label=label)
    legend = plt.legend(bbox_to_anchor=(0.01, 0.15, 0, 0), loc='lower left',
                        fontsize=30, markerscale=5)
    # legend.get_frame().set_linewidth(0)
    plt.show()
    plt.savefig(species+'.svg')
