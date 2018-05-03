#!/usr/bin/python3

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from json import load

wgs84 = 4326
south_china_sea = 3415
xi_an = (108.886, 34.265)
map = Basemap(epsg=south_china_sea, lat_0=xi_an[1], lon_0=xi_an[0],
#              resolution='h',
              llcrnrlon=80, llcrnrlat=-2, urcrnrlon=140,
              urcrnrlat=55)

data = load(open('./species_loc.json', 'r'))
for species in data:
#     ax.axis('off')
    plt.figure(figsize=(20,20))
    map.readshapefile('./province', 'province', drawbounds=True)
    map.drawmeridians(range(80,140,10), labels=(0,0,1,1), fontsize=15)
    map.drawparallels(range(0,80, 10), labels=(1,1,0,0), fontsize=15)
    loc = data[species]
    lat_list = [i[0] for i in loc]
    lon_list = [i[1] for i in loc]
    x, y = map(lon_list, lat_list)
    label = '$\it{{{}}}$'.format(species.replace(' ', '\ '))
    plt.scatter(x, y, marker='o', color='r', s=15, label=label)
    legend = plt.legend(bbox_to_anchor=(0.01, 0.15,0,0),loc='lower left',
                       fontsize=30, markerscale=5)
    # legend.get_frame().set_linewidth(0)
    plt.savefig(species+'.svg')
