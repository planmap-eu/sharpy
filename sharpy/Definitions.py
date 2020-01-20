import fiona.crs
north_pole_crs = fiona.crs.from_string("+proj=stere +lat_0=90 +lon_0=0 +k=1 +x_0=0 +y_0=0 +a=3396190 +b=3376200 +units=m +no_defs ")
mars_2000_crs = fiona.crs.from_string("+proj=longlat +a=3396190 +b=3376200 +no_defs ")