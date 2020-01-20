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

# %%
folder = "/data/SciBigData/radargrams/Tesi triennale/"    
files = find_sharad_radargrams_in_folder(folder)
ids = match_sharad_ids(files)
print(ids)

# %%
ids = np.loadtxt("ids_to_download.csv", delimiter=",", dtype=str)[:,1]

# %%

# %%


rids = np.random.choice(ids, 10).astype(str)

# %%
import logging as log
log.getLogger().setLevel(log.WARNING)

download_data_fot_sharad_id(rids, "newdataset", exclude=['RGRAM_IMG', 'RGRAM_LBL', 'JPG_LBL' ])


# %%
ftp://pds-geosciences.wustl.edu/mro/mro-m-sharad-5-radargram-v1/mrosh_2001/data/geom/s_0083xx/

# %%

# %%
