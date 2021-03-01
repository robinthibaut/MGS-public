"""
Compute the model and data misfit of the forward model #1
"""

#  Copyright (c) 2021. Robin Thibaut, Ghent University

import os
from os.path import join as jp

import matplotlib.pyplot as plt
import numpy as np
from tomopal.crtomopy.crtomo import crc
from tomopal.geoview.diavatly import model_map

# Directories
cwd = os.getcwd()  # Current working directory
sub_folder_name = "paper"
mesh_dir = jp(cwd, "mesh", sub_folder_name)  # Mesh files directory
mshf = "mesh/paper/Mesh.dat"

# Mesh
ncol, nlin, nelem, blocks, centerxy, nodes = crc.mesh_geometry(mshf)

# IP conversion factor
m2p = -1.234598  # crc.mtophase(ncycles=1, pulse_l=3.5, tmin=0.02, tmax=2.83)

# %% MODEL MISFIT
result_folder = "results/paper/FM1B/config"
true_model = jp(result_folder, "fm1b_model.dat")
# Load true model
resmod = crc.datread(true_model, start=1)[:, 2]
# res_levels = 10 ** np.linspace(min(resmod), max(resmod), 7)
# res_levels = 10**np.array([0]+sorted(set(resmod)))
res_levels = 10**np.linspace(min(resmod), max(resmod), 8)

model_map(
    polygons=blocks,
    vals=10**resmod,
    log=1,
    cbpos=0.35,
    levels=res_levels,
    binned=False,
    folder=result_folder,
    fontsize=10,
    labelsize=12,
    figname="res_mod",
    extension="pdf",
)
plt.show()

# Smooth
# Load solution
results_dir = "results/paper/FM1B/"
subs = ""
result_folder = jp(results_dir, subs)
sol, files = crc.import_res(result_folder=result_folder, return_file=1)

res = sol[0]
# Res plot
rtp = 10**np.copy(res)

# res_levels = 10**np.array([0]+sorted(set(resmod)))
# res_levels = 10 ** np.linspace(min(resmod), max(resmod), 10)
model_map(
    polygons=blocks,
    vals=rtp,
    log=1,
    cbpos=0.35,
    levels=res_levels,
    folder=result_folder,
    figname="res",
    fontsize=10,
    labelsize=12,
    extension="pdf",
)
plt.show()

# Compute misfit
model_misfit_s = resmod - res
# Get norm
ms = np.linalg.norm(model_misfit_s, ord=1)

# MGS
results_dir = "results/paper/FM1B_MGS/"
subs = ""
result_folder = jp(results_dir, subs)
sol, files = crc.import_res(result_folder=result_folder, return_file=1)
res_mgs = sol[0]
# Res plot
rtp = 10**np.copy(res_mgs)
model_map(
    polygons=blocks,
    vals=rtp,
    log=1,
    cbpos=0.35,
    levels=res_levels,
    folder=result_folder,
    figname="res_mgs",
    fontsize=10,
    labelsize=12,
    extension="pdf",
)
plt.show()

# Compute misfit
model_misfit_mgs = resmod - res_mgs
# Get norm
mmgs = np.linalg.norm(model_misfit_mgs, ord=1)

# %% DATA MISFIT

# True data
true_data = "results/paper/FM1B/config/fm1b_data.dat"

td = crc.datread(true_data, start=1)

# Smooth
# Data of smooth solution
smooth_data = "results/paper/FM1B/volt08.dat"
sd = crc.datread(smooth_data, start=1)

# Compute misfit for smooth data
data_misfit_s = td[:, 4] - sd[:, 4]
# Get norm
nds = np.linalg.norm(data_misfit_s, ord=1)

# MGS
# Data of sharp solution
mgs_data = "results/paper/FM1B_MGS/volt10.dat"
mgsd = crc.datread(mgs_data, start=1)

# Compute misfit for sharp data
data_misfit_mgs = td[:, 4] - mgsd[:, 4]
# Get norm
ndmgs = np.linalg.norm(data_misfit_mgs, ord=1)
