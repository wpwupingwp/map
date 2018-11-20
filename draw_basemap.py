#!/usr/bin/python3

from sys import argv
from os.path import join as path_join
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import io
import json
import pickle
import matplotlib.pyplot as plt

wgs84 = 4326
south_china_sea = 3415
xi_an = (108.886, 34.265)
plt.figure(figsize=(20, 20))
ax = plt.gca()
m = Basemap(epsg=south_china_sea, lat_0=xi_an[1], lon_0=xi_an[0],
            llcrnrlon=80, llcrnrlat=-2, urcrnrlon=140, urcrnrlat=55,
            ax=ax)

#m.readshapefile(path_join('Basemap', 'world'), 'world', drawbounds=True,
#                linewidth=1.5, color='#666666', zorder=1)
m.readshapefile(path_join('Basemap', 'nation-polygon'), 'nation',
                drawbounds=True, linewidth=2, color='#000000')
# use nation to cover world for south tibet
p = [Polygon(i) for i in m.nation]
ax.add_collection(PatchCollection(p, facecolor='#FFFFFF',
                                  edgecolor='#000000', linewidths=2,
                                  zorder=2))

m.readshapefile(path_join('Basemap', 'province'), 'province', drawbounds=True,
                linewidth=1, color='#222222')
m.readshapefile(path_join('Basemap', 'river'), 'river', drawbounds=True,
                linewidth=1, color='#189EEC')
m.readshapefile(path_join('Basemap', 'lake'), 'lake', drawbounds=True,
                linewidth=1, color='#189EEC')
m.drawmeridians(range(80, 140, 10),  labels=(0, 0, 1, 1),  fontsize=15)
m.drawparallels(range(0, 80, 10),  labels=(1, 1, 0, 0),  fontsize=15)
tmpfile = io.BytesIO()
pickle.dump(m, tmpfile)

data = json.load(open(argv[1], 'r'))
for species in data:
    tmpfile.seek(0)
    basemap = pickle.load(tmpfile)
    loc = data[species]
    lat_list = [i[0] for i in loc]
    lon_list = [i[1] for i in loc]
    x, y = basemap(lon_list, lat_list)
    label = '$\it{{{}}}$'.format(species.replace(' ', '\ '))
    plt.scatter(x, y, marker='o', color='r', s=15, label=label, zorder=3)
    legend = plt.legend(bbox_to_anchor=(0.01, 0.15, 0, 0), loc='lower left',
                        fontsize=30, markerscale=5)
    # legend.get_frame().set_linewidth(0)
    plt.savefig(species+'.svg')
    print('{}, {} distribution(s)'.format(species, len(loc)))
    plt.close()
