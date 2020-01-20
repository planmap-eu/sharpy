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
from sharpy import *
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = [15, 10]

# %%
m = SharadRadagramsManager()


# %%
m.loadDatabase()

# %%
m.db.plot(linewidth=0.01)

# %%
m.db

# %%
r =m.getRadargram("00555102")
img = r.getProduct("JPG")
imshow(img)

# %%
g = r.getProduct("GEOM").to_crs(north_pole_crs).geometry
pts = np.array([np.concatenate(a.coords.xy) for a in g])

# %%
scatter(*pts.T, s=0.1)

start = pts[0]
end = pts[-1]

scatter(*start)
scatter(*end)

length = np.linalg.norm(end-start)
print(length)

# %%
nrows = 3600
ncols = img.shape[1]
print(ncols)

# %%
scale = length / ncols
vlength = nrows * scale
print(vlength)


# %%
import vtk
s = vtk.vtkPlaneSource()




# %%

# %%
origin = np.concatenate([start, [-vlength]])
p1 = np.concatenate([end, [-vlength]])
p2 = origin + np.array([0,0,vlength])

# %%
s.SetOrigin(origin)
s.SetPoint1(p1)
s.SetPoint2(p2)
s.Update()

pd = s.GetOutput()

w = vtk.vtkXMLPolyDataWriter()
w.SetFileName("file.vtp")
w.SetInputData(pd)
w.Update()

# %%
