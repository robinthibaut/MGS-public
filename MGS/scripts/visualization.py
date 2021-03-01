"""
Script to visualize results given their folder location.
"""

import os
from os.path import join as jp

import matplotlib.pyplot as plt
import numpy as np
from tomopal.crtomopy.crtomo import crc
from tomopal.geoview.diavatly import model_map

cwd = os.getcwd()  # Current working directory
sub_folder_name = "paper"
mesh_dir = jp(cwd, "mesh", sub_folder_name)  # Mesh files directory
mshf = jp(mesh_dir, "Mesh.dat")
results_dir = jp(cwd, "results", sub_folder_name,
                 "FM1B")  # Results files directory

subs = ""

result_folder = jp(results_dir, subs)

ncol, nlin, nelem, blocks, centerxy, nodes = crc.mesh_geometry(mshf)

# %% Load results
try:
    m2p = crc.mtophase(ncycles=1, pulse_l=3.5, tmin=0.02, tmax=2.83)

    res, ip, s = crc.import_res(result_folder=result_folder)

    rest = np.copy(res)
    ipt = np.copy(ip[:] / m2p)
    ss = [si[-1] for si in s]

    # res, files = import_res(result_folder=result_folder, return_file=1)
    # rest = np.copy(res[0])
    res_levels = 10**np.linspace(min(rest), max(rest), 8)
    rtp = 10**np.copy(rest)

    figname = jp(results_dir, result_folder + "_res.png")
    model_map(
        polygons=blocks,
        vals=rtp,
        log=1,
        cbpos=0.35,
        levels=res_levels,
        folder=result_folder,
        figname="res",
    )
    plt.show()
except ValueError:
    pass

# %%
# np.histogram(np.abs(ipt))
# cut = 200
# ipt = np.where(np.abs(ipt) < 200, ipt, 200)
#
# figname = jp(results_dir, result_folder + '_ip.png')
# ip_levels = np.linspace(0, max(ipt), 10)
# model_map(polygons=blocks, vals=np.abs(ipt), log=0, levels=ip_levels, cbpos=0.35, folder=result_folder, figname='ip')
# plt.show()

# %%  Plot model sensitivity
figname = jp(results_dir, result_folder + "_sens.png")
s_levels = np.linspace(0, np.max(ss), 10)
model_map(
    polygons=blocks,
    vals=ss,
    log=0,
    levels=s_levels,
    stepy=8,
    contour=-3,
    aspect=1.5,
    cbpos=0.2,
    folder=result_folder,
    figname="sens",
)
plt.show()

# %% Plot pseudosections

#  Open data file
os.chdir(cwd)
sub_folder_name = "paper"
data_dir = jp(cwd, "data", sub_folder_name)  # Data files directory
data_file = jp(data_dir, "field_data.dat")

data = crc.datread(data_file, start=1)

a = data[:, 0] * 5
b = data[:, 1] * 5
m = data[:, 2] * 5
n = data[:, 3] * 5

xy = np.column_stack([(m + n) / 2, -np.min(
    ((m + n) / 2 - a, b - (m + n) / 2), axis=0) / 3])

fig, ax = plt.subplots()
ax.plot(xy[:, 0], xy[:, 1], "k+", markersize=4)
ax.set_xlabel("X(m)", fontsize=12)
ax.set_ylabel("Pseudo depth(m)", fontsize=12)
ax.grid(alpha=0.7)
ax.set_aspect(aspect=7)
plt.savefig("pseudosection.png",
            bbox_inches="tight",
            transparent=False,
            dpi=300)
plt.show()
