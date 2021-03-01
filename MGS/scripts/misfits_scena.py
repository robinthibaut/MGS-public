"""
Compute the model and data misfit of the synthetic scenario
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

labelsize = 12
bpos = 0.38

# %% MODEL MISFIT
true_model = jp("/Users/robin/PycharmProjects/MGS",
                "data/paper/models/forwardscenario.dat")

# Load true model
resmod = crc.datread(true_model, start=1)[:, 2]
ipmod = crc.datread(true_model, start=1)[:, 3]
m2p = -1.234598

mshf = "/Users/robin/PycharmProjects/MGS/mesh/paper/Mesh.dat"
ncol, nlin, nelem, blocks, centerxy, nodes = crc.mesh_geometry(mshf)

res_levels = 10**np.linspace(min(resmod), max(resmod), 10)
ip_levels = np.linspace(min(ipmod / m2p), 150, 7)

result_folder = "/Users/robin/PycharmProjects/MGS/results/paper/scenario"

model_map(
    polygons=blocks,
    vals=10**resmod,
    log=1,
    cbpos=bpos,
    aspect=1,
    levels=res_levels,
    binned=False,
    folder=result_folder,
    fontsize=10,
    labelsize=labelsize,
    figname=None,
    extension="pdf",
)
plt.show()

model_map(
    polygons=blocks,
    vals=ipmod / m2p,
    log=0,
    cbpos=bpos,
    levels=ip_levels,
    binned=False,
    folder=result_folder,
    fontsize=10,
    labelsize=labelsize,
    figname=None,
    extension="pdf",
)
plt.show()

results_dir = jp("/Users/robin/PycharmProjects/MGS",
                 "results/paper/scenario/WFB")

# %% STEPI Smooth
# Load solution

results_dir = jp("/Users/robin/PycharmProjects/MGS",
                 "results/paper/scenario/WFB")
subs = "STEPI"
result_folder = jp(results_dir, subs)
sol, files = crc.import_res(result_folder=result_folder, return_file=1)

# Res plot
res = sol[0]

# res_levels = 10**np.array(sorted(set(resmod)))
rtp = 10**np.copy(res)

model_map(
    polygons=blocks,
    vals=rtp,
    log=1,
    cbpos=bpos,
    levels=res_levels,
    folder=result_folder,
    figname=None,
    fontsize=10,
    labelsize=labelsize,
    extension="pdf",
)
plt.show()

# IP plot
ip = sol[1]
ipt = np.copy(np.abs(ip / m2p))
# cut = 260
# ipt[ipt > cut] = cut
ipmodt = ipmod / m2p

model_map(
    polygons=blocks,
    vals=ipt,
    log=0,
    cbpos=bpos,
    levels=ip_levels,
    folder=result_folder,
    fontsize=10,
    labelsize=labelsize,
    figname=None,
    extension="pdf",
)
plt.show()

# Compute res misfit
model_misfit_s = resmod - res
# Get norm
ms = np.linalg.norm(model_misfit_s, ord=1) / nelem
# Chi2
chi = np.sum(model_misfit_s**2)

# Compute ip misfit
model_misfit_s_ip = ipmod - ip
# Get norm
msip = np.linalg.norm(model_misfit_s_ip, ord=1) / nelem

# %% STEPII Interpreted model
results_dir = jp("/Users/robin/PycharmProjects/MGS",
                 "results/paper/scenario/WFB")
subs = "STEPII"
result_folder = jp(results_dir, subs)

int_mod_file = jp(
    "/Users/robin/PycharmProjects/MGS",
    "results/paper/scenario/WFB/STEPII/interpreted_model/config/forwardscenariostartmodel.dat",
)

int_mod = crc.datread(int_mod_file, start=1)[:, 2]

model_map(
    polygons=blocks,
    vals=10**int_mod,
    log=1,
    cbpos=bpos,
    levels=res_levels,
    folder=result_folder,
    fontsize=10,
    labelsize=labelsize,
    figname=None,
    extension="pdf",
)
plt.show()

# Compute misfit
model_misfit_int = resmod - int_mod
# Get norm
mmint = np.linalg.norm(model_misfit_int, ord=1) / nelem

# %% STEPIII Ref model smooth
subs = "STEPIII"
result_folder = jp(results_dir, subs)

sol, files = crc.import_res(result_folder=result_folder, return_file=1)

# Res plot
res = sol[0]

model_map(
    polygons=blocks,
    vals=10**res,
    log=1,
    cbpos=bpos,
    levels=res_levels,
    folder=result_folder,
    fontsize=10,
    labelsize=labelsize,
    figname=None,
    extension="pdf",
)
plt.show()

# Compute misfit
model_misfit_int = resmod - res
# Get norm
mmint2 = np.linalg.norm(model_misfit_int, ord=1) / nelem

# %% STEPIV Ref model smooth
results_dir = jp("/Users/robin/PycharmProjects/MGS",
                 "results/paper/scenario/WFB")
subs = "STEPIV"
result_folder = jp(results_dir, subs)

sol, files = crc.import_res(result_folder=result_folder, return_file=1)

# Res plot
res = sol[0]

model_map(
    polygons=blocks,
    vals=10**res,
    log=0,
    cbpos=bpos,
    levels=res_levels,
    folder=result_folder,
    fontsize=10,
    labelsize=labelsize,
    figname=None,
    extension="pdf",
)
plt.show()

# IP plot
ip = sol[1]
ipt = np.copy(np.abs(ip / m2p))
# cut = 150
# ipt[ipt > cut] = cut
ipmodt = ipmod / m2p
# ip_levels = np.linspace(min(ipt), cut, 7)
# ip_levels = sorted(set(ipmod/m2p))
model_map(
    polygons=blocks,
    vals=ipt,
    log=0,
    cbpos=bpos,
    levels=ip_levels,
    folder=result_folder,
    fontsize=10,
    labelsize=labelsize,
    figname=None,
    extension="pdf",
)
plt.show()

# Compute misfit
model_misfit_int = resmod - res
# Get norm
mmint3 = np.linalg.norm(model_misfit_int, ord=1) / nelem

# Compute ip misfit
model_misfit_s_ip2 = ipmod - ip
# Get norm
msip2 = np.linalg.norm(model_misfit_s_ip2, ord=1) / nelem

# %% WFA
results_dir = jp("/Users/robin/PycharmProjects/MGS",
                 "results/paper/scenario/WFA")
subs = ""
result_folder = jp(results_dir, subs)

sol, files = crc.import_res(result_folder=result_folder, return_file=1)

# Res plot
res = sol[0]

# lev = 10**np.linspace(min(resmod), max(resmod), 12)

model_map(
    polygons=blocks,
    vals=10**res,
    log=0,
    cbpos=bpos,
    levels=res_levels,
    folder=result_folder,
    fontsize=10,
    labelsize=labelsize,
    figname=None,
    extension="pdf",
)
plt.show()

# IP plot
ip = sol[1]
ipt = np.copy(np.abs(ip / m2p))
# cut = 150
# ipt[ipt > cut] = cut
ipmodt = ipmod / m2p
# ip_levels = np.linspace(min(ipt), cut, 7)
# ip_levels = sorted(set(ipmod/m2p))
model_map(
    polygons=blocks,
    vals=ipt,
    log=0,
    cbpos=bpos,
    levels=ip_levels,
    folder=result_folder,
    fontsize=10,
    labelsize=labelsize,
    figname=None,
    extension="pdf",
)
plt.show()

# Compute misfit
model_misfit_int = resmod - res
# Get norm
mmint4 = np.linalg.norm(model_misfit_int, ord=1) / nelem

# Compute ip misfit
model_misfit_s_ip3 = ipmod - ip
# Get norm
msip3 = np.linalg.norm(model_misfit_s_ip3, ord=1) / nelem

# %% DATA MISFIT

# True data
true_data = "data/paper/scenario.dat"

td = crc.datread(true_data, start=1)

# Interpreted
# Data of smooth solution
int_data = "results/paper/scenario/WFB/STEPII/interpreted_model/volt.dat"
did = crc.datread(int_data, start=1)

# Compute misfit for int data
data_misfit_s = ((td[:, 4] - did[:, 4]) / (td[:, 4] * 0.03))**2
# Get norm
nds = np.sqrt(np.sum(data_misfit_s) / nelem)

# MGS
# Data of sharp solution
mgs_data = "results/paper/scenario/WFB/STEPIV/volt08.dat"
mgsd = crc.datread(mgs_data, start=1)
mgsdt = np.array([mgsd[i] for i in range(0, len(mgsd), 2)])

# Compute misfit for sharp data
data_misfit_mgs = ((td[:, 4] - mgsdt[:, 4]) / (td[:, 4] * 0.03))**2

# Get norm
ndmgs = np.sqrt(np.sum(data_misfit_mgs) / nelem)
