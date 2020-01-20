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
import logging as log
log.getLogger().setLevel(log.INFO)
import pandas as pd
from ipypb import track
import pandas as pd
from geopandas import GeoDataFrame
from pandas import DataFramed
from shapely.geometry import Point
import fiona
import regex
from datetime import datetime
from sharpy import *

import glob

names = ["RADARGRAM COLUMN", "TIME", "LATITUDE", "LONGITUDE", "MARS RADIUS", "SPACECRAFT RADIUS", 
                 "RADIAL VELOCITY", "TANGENTIAL VELOCITY", "SZA", "PHASE/1.0E16"]

types = [int, datetime, float, float, float, float, float, float, float, float]
names = [n.replace(" ", "_").replace("/", "_").lower() for n in names]


dtype = [t for t in zip(names, types)]

geom_f = "/data/SciBigData/radargrams/geom/"
pattern = geom_f + "/**/*_geom.lbl"
log.info(pattern)

allgeoms = glob.glob(pattern)

log.info(f"found {len(allgeoms)} radargrams geom-files")

# %%

# %%
# this is the actual loop injesting the geom files and simplyfying them
out = []
ids = []
for f in track(allgeoms):
    tab = lbl_to_geom(f)
    df = read_geom_lbl(tab)
    geometry = LineString([Point(xy) for xy in zip(df.longitude, df.latitude)])
    geometry= geometry.simplify(0.001)
    i = ids.append( match_sharad_id(f) )
    out.append(geometry)
    

# %%
m

# %%
df = DataFrame()
df["track_id"] = ids

# %%
crs = fiona.crs.from_string("+proj=longlat +a=3396190 +b=3376200 +no_defs") # MARS 2000
gf = GeoDataFrame(df, crs=crs, geometry=out)

# %%
gf.to_file("alltracks")

# %%
