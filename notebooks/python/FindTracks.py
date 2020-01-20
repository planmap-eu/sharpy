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
from sharpy import *
regions = "/data/SciBigData/radargrams/regions.gpkg"
layer = "regions"

alltracks = "alltracks"
tracks=GeoDataFrame.from_file(alltracks)


regs = GeoDataFrame.from_file(regions, layer=layer, crs=fiona.crs.from_string("+proj=stere +lat_0=90 +lat_ts=90 +lon_0=0 +k=1 +x_0=0 +y_0=0 +a=3376200 +b=3376200 +units=m +no_defs"))
regs = regs.to_crs(tracks.crs)


# %%

# %%
inttrack = tracks[tracks.intersects(regs.geometry[0])]

inttracks = inttrack.intersection(regs.geometry[0])

iid = inttrack.track_id

inttracks.to_file("intersecting")

# %%
iid.to_csv("ids_to_download.csv")

# %%

# %%
