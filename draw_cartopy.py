#!/usr/bin/python3

from sys import argv
import matplotlib.pyplot as plt
from cartopy.io.shapereader import Reader
import cartopy.crs as ccrs
import io
import json
import pickle

south_china_sea = 3415
crs = ccrs.Mercator()
crs2 = ccrs.epsg(3415)
crs = ccrs.Mercator()
fig = plt.figure(figsize=(20,20))
ax = fig.add_subplot(1, 1, 1, projection=crs)
#ax = plt.axes(projection=crs)
#ax.set_extent([140, 80, -2, 55], crs=crs)
ax.set_extent([136, 72, 3, 55], crs=crs)
nation = Reader('/home/ping/work/map/Basemap/nation')
province = Reader('/home/ping/work/map/Basemap/province')
river = Reader('/home/ping/work/map/Basemap/river')
lake = Reader('/home/ping/work/map/Basemap/lake')
ax.add_geometries(nation.geometries(), crs=crs, edgecolor='#000000',
                  facecolor='none', linewidth=2)
ax.add_geometries(province.geometries(), crs=crs, edgecolor='#222222',
                  facecolor='none', linewidth=1)
ax.add_geometries(river.geometries(), crs=crs, edgecolor='#189EEC',
                  facecolor='none', linewidth=1)
ax.add_geometries(lake.geometries(), crs=crs, edgecolor='#189EEC',
                  facecolor='none', linewidth=1)
# ax.gridlines(color='#888888', alpha=0.5)
tmpfile = io.BytesIO()
pickle.dump(ax, tmpfile)

data = json.load(open(argv[1], 'r'))
for species in data:
    tmpfile.seek(0)
    ax = pickle.load(tmpfile)
    loc = data[species]
    lat = [i[0] for i in loc]
    lon = [i[1] for i in loc]
    label = '$\it{{{}}}$'.format(species.replace(' ', '\ '))
    ax.scatter(lon, lat, marker='o', color='r', s=15, label=label,
               transform=crs)
    legend = plt.legend(bbox_to_anchor=(0.01, 0.15, 0, 0), loc='lower left',
                        fontsize=30, markerscale=5)
    # legend.get_frame().set_linewidth(0)
    # plt.show()
    plt.savefig(species+'.svg')

    print('{}, {} distribution(s)'.format(species, len(loc)))
