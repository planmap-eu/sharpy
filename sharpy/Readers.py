# in an io module
import pandas as pd
import cv2 as cv
from osgeo import gdal
from datetime import datetime
from .Definitions import *
from shapely.geometry import Point
from geopandas import GeoDataFrame

# readers and file formats definitions for sharad data loading

geom_names = ["RADARGRAM COLUMN", "TIME", "LATITUDE", "LONGITUDE", "MARS RADIUS", "SPACECRAFT RADIUS",
                 "RADIAL VELOCITY", "TANGENTIAL VELOCITY", "SZA", "PHASE/1.0E16"]

geom_types = [int, datetime, float, float, float, float, float, float, float, float]
geom_names = [n.replace(" ", "_").replace("/", "_").lower() for n in geom_names]

def pandas_to_geopandas_points(df, xname="longitude", yname="latitude", crs=mars_2000_crs):
    geometry = [Point(xy) for xy in zip(df[xname], df[yname])]
    geo_df = GeoDataFrame(df, crs=crs, geometry=geometry)
    return geo_df

def read_geom(file):
    table = pd.read_csv(file, skiprows=0, names=geom_names)

    return pandas_to_geopandas_points(table)




def read_image(file):
    return cv.imread(file)[:,:,0]


def read_img(file):
    lbl = file[:-3] + "lbl"
    raster = gdal.Open(lbl)
    return raster.GetRasterBand(1).ReadAsArray()