# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
# %pylab inline

from sharpy.sharad import *
log.getLogger().setLevel(log.INFO)

# %%

# %%

# filepath = r"/home/luca/Code/sharpy.git/notebooks/sharad_data/s_00525702_rgram.lbl"

# # Open the file:
# raster = gdal.Open(filepath)
# raster

# %%

    

# %%

    

img = getSharadDefaultRemoteProducts()[0]
img.hasLoader()

# %%

# %%

# import geopandas as gpd

# # Read points from shapefile
# pts = gpd.read_file('your_point_shapefile.shp')
# pts = pts[['UTM_E', 'UTM_N', 'Value', 'geometry']]
# pts.index = range(len(pts))
# coords = [(x,y) for x, y in zip(pts.UTM_E, pts.UTM_N)]

# # Open the raster and store metadata
# src = rasterio.open('your_raster.tif')

# # Sample the raster at every point location and store values in DataFrame
# pts['Raster Value'] = [x for x in src.sample(coords)]
# pts['Raster Value'] = probes.apply(lambda x: x['Raster Value'][0], axis=1)

# %%
m = SharadRadagramsManager()
m.loadDatabase()
r1 = m.getRadargram('00525702')
# m.downloadProduct('00525702', "JPG", 0)
# m.downloadProducts(['00525702', '00203001'], ["JPG", "JPG_LBL", "GEOM", "GEOM_LBL", "TIFF", "TIFF_LBL"])


# %%
pts = np.array([(a.coords.xy[0][0], a.coords.xy[1][0]) for a in r1.getTrack().to_crs(n_pole_stereo_crs).geometry])

# %%
gpd.GeoDataFrame([r1.getTrack()]).crs

# %%

pts = r1.getTrackNumpy()

# %%
d.crs

# %%
import rasterio
raster = "/run/media/luca/data/SciBigData/radargrams/mola_polar_megt_512pd/megt_n_512_1/"
d = rasterio.open(raster)
ll = np.array(list(d.sample(pts.tolist())))

# %%
from rasterio.plot import show
figure(figsize=(10,10))
plot(*pts.T)
show(d)


# %%
figure(figsize=(10,10))
imshow(r1.getProduct("JPG")[2000:3000,:])

# %%
plot(ll)

# %%
from shapely.geometry import Point, LineString, MultiLineString
r = r1.getProduct("GEOM")

track = LineString([Point(xy) for xy in zip(r.longitude, r.latitude)])

# %%
r

# %%
download_data_for_sharad_id??

# %%
from sharpy.sharad

# %%
