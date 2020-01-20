import logging as log
from .Readers import *
import attr, sys
import fiona
import geopandas as gpd
from shapely.geometry import Point
import os
import numpy as np

@attr.s
class RemoteProductDescriptor(object):
    name = attr.ib(default="IDENTIFIER_NAME")
    subpath = attr.ib(default="./")
    file_postfix = attr.ib(default=".txt")
    python_loader_f = attr.ib(default=None)
    dependencies = attr.ib(factory=list)

    def getFileName(self, filename):
        return self.processFilename(filename) + self.file_postfix

    def getPath(self, filename):
        return self.subpath + self.getFileName(filename)

    def processFilename(self, filename):
        return "s_" + filename[0:4] + "xx/s_" + filename

    def hasLoader(self):
        return self.python_loader_f is not None


def getSharadDefaultRemoteProducts():
    R = RemoteProductDescriptor
    return [R("IMG", "/data/rgram/", "_rgram.img", python_loader_f=read_img, dependencies=["IMG_LBL"]),
            # we always need the lbl to read a pds file.
            R("IMG_LBL", "data/rgram/", "_rgram.lbl"),
            R("TIFF", "/browse/tiff/", "_tiff.tif", read_image),
            R("TIFF_LBL", "/browse/tiff/", "_tiff.lbl"),
            R("JPG", "/browse/thm/", "_thm.jpg", read_image),
            R("JPG_LBL", "/browse/thm/", "_thm.lbl"),
            R("GEOM", "/data/geom/", "_geom.tab", python_loader_f=read_geom),
            R("GEOM_LBL", "/data/geom/", "_geom.lbl")]


mars_2000_crs = fiona.crs.from_string("+proj=longlat +a=3396190 +b=3376200 +no_defs ")
n_pole_stereo_crs = fiona.crs.from_string(
    "+proj=stere +lat_0=90 +lat_ts=90 +lon_0=0 +x_0=0 +y_0=0 +a=3396190 +rf=169.894447223612 +units=m +no_defs")


@attr.s
class Radargram(object):
    uid = attr.ib(default=None, validator=attr.validators.instance_of(str))
    filename = attr.ib(default="", validator=attr.validators.instance_of(str))
    manager = attr.ib(default=None)

    def __attrs_post_init__(self):
        if len(self.uid) != 8:
            log.critical("uid must be a string of 8 chars")
            return

    def getProduct(self, prod_type="JPG"):
        return self.manager.getProduct(self.uid, prod_type)

    def getTrack(self):
        r = self.getProduct("GEOM")
        track = [Point(xy) for xy in zip(r.longitude, r.latitude)]
        tt = gpd.GeoDataFrame()
        tt.geometry = track
        tt.crs = mars_2000_crs
        return tt

    def getTrackNumpy(self):
        return np.array(self.getTrack().coords.xy).T


import requests
import geopandas as gp


@attr.s
class SharadRadagramsManager(object):
    data_folder = attr.ib(default=os.path.join(os.getcwd(), "sharad_data/"))
    remote_basepath = attr.ib(default="http://pds-geosciences.wustl.edu/mro/mro-m-sharad-5-radargram-v1/mrosh_2001/")
    products = attr.ib(default=getSharadDefaultRemoteProducts())
    db_file = attr.ib(default="/home/luca/Code/sharpy.git/data/alltracks")
    db = attr.ib(default=None)

    def loadDatabase(self):
        self.db = gp.GeoDataFrame.from_file(self.db_file)

    def __attrs_post_init(self):
        self.update_remote_pats_subfolders()

    def getAvailableProducts(self):
        return [a.name for a in self.products]

    def getProductDescriptor(self, prod_type="JPG"):
        for p in self.products:
            if p.name == prod_type:
                return p
        log.critical(f"Product type {prod_type} not know. wrong name ? or please add the descriptor to products list")
        return None

    def downloadProduct(self, filename, prod_type="JPG", force=False):
        des = self.getProductDescriptor(prod_type)
        for d in des.dependencies:
            log.info(f"downloading dependencies of type {d}")
            self.downloadProduct(filename, d)

        url = self.getRemotePathForProduct(filename, prod_type)
        self._download_http_url(url, force=force)

    def downloadProducts(self, filenames, prod_types=[["JPG"]], force=False):
        for fname in filenames:
            for prod_type in prod_types:
                self.downloadProduct(fname, prod_type, force=force)

    def getProduct(self, filename, prod_type="GEOM"):
        local = self.getLocalPathForProduct(filename, prod_type)
        if not os.path.exists(local):
            self.downloadProduct(filename, prod_type)

        des = self.getProductDescriptor(prod_type)

        if not des.hasLoader():
            log.critical(f"cannot load product of type {prod_type}. missing loader")
            return

        else:
            return des.python_loader_f(local)

    def getRemotePathForProduct(self, filename, prod_type="JPG"):
        des = self.getProductDescriptor(prod_type)
        subpath = des.getPath(filename)
        remote_fullpath = self.remote_basepath + subpath
        return remote_fullpath

    def getLocalPathForProduct(self, filename, prod_type="JPG"):
        url = self.getRemotePathForProduct(filename, prod_type)
        fname = os.path.split(url)[-1]
        local_filepath = os.path.join(self.data_folder, fname)
        return local_filepath

    def _download_http_url(self, url, force=False):
        log.info(f"downloading {url}")
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder, exist_ok=False)

        fname = os.path.split(url)[-1]
        fullfilepath = os.path.join(self.data_folder, fname)

        if os.path.exists(fullfilepath) and not force:
            log.warning(f"file {fullfilepath} yet exists not downloading again")
            return

        r = requests.get(url, allow_redirects=True)
        open(fullfilepath, 'wb').write(r.content)

        return True

    def getRadargram(self, radname):
        return Radargram(radname, manager=self)






