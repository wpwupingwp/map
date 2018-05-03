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
    fig, ax = plt.subplots(figsize=(20,20))
    map.readshapefile('./province', 'province', drawbounds=True)
    loc = data[species]
    lat_list = [i[0] for i in loc]
    lon_list = [i[1] for i in loc]
    x, y = map(lon_list, lat_list)
    ax.scatter(x, y, marker='D', color='r', s=10)
    plt.savefig(species+'.svg')
    plt.show()
