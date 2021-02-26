"""
Plots different results
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
sub_folder_name = 'paper'
mesh_dir = jp(cwd, 'mesh', sub_folder_name)  # Mesh files directory

labelsize = 12
bpos = .38

mshf = '/Users/robin/PycharmProjects/MGS/mesh/paper/Mesh.dat'
ncol, nlin, nelem, blocks, centerxy, nodes = crc.mesh_geometry(mshf)

# %% MODEL MISFIT
true_model = jp('/Users/robin/PycharmProjects/MGS', 'data/paper/models/forwardscenario.dat')

# Load true model
resmod = crc.datread(true_model, start=1)[:, 2]
ipmod = crc.datread(true_model, start=1)[:, 3]
m2p = -1.234598

res_levels = 10 ** np.linspace(min(resmod), max(resmod), 10)
ip_levels = np.linspace(min(ipmod / m2p), 150, 10)

true_data = crc.datread('data/paper/field_data.dat', start=1)
a = true_data[:, 0] * 5
b = true_data[:, 1] * 5
m = true_data[:, 2] * 5
n = true_data[:, 3] * 5

xy = np.column_stack([(m + n) / 2, -np.min(((m + n) / 2 - a, b - (m + n) / 2), axis=0) / 3])

results_dir = jp('/Users/robin/PycharmProjects/MGS', 'results/paper/field_data/WFB')

# %% STEPI Smooth
# Load solution

results_dir = jp('/Users/robin/PycharmProjects/MGS', 'results/paper/field_data/WFB')
subs = 'STEPI'
result_folder = jp(results_dir, subs)
sol, files = crc.import_res(result_folder=result_folder, return_file=1)

# Res plot
res = sol[0]

# res_levels = 10**np.array(sorted(set(resmod)))
rtp = 10 ** np.copy(res)

model_map(polygons=blocks, vals=rtp, log=1, cbpos=bpos, levels=res_levels, folder=result_folder,
          figname='res_smooth', fontsize=10, labelsize=labelsize, extension='pdf')
plt.show()

# IP plot
ip = sol[1]
ipt = np.copy(np.abs(ip / m2p))
# cut = 260
# ipt[ipt > cut] = cut
ipmodt = ipmod / m2p

model_map(polygons=blocks, vals=ipt, log=0, cbpos=bpos, levels=ip_levels,
          folder=result_folder, fontsize=10, labelsize=labelsize,
          figname=None, extension='pdf')
plt.show()

# Sensitivity plot
sens = np.array([s[2] for s in sol[2]])
sens_levels = [-8, -7, -6, -5, -4, -3, -2, -1, 0]
model_map(polygons=blocks, vals=sens, log=0, cbpos=bpos, levels=sens_levels,
          folder=result_folder, fontsize=10, labelsize=labelsize,
          figname=None, extension='pdf')
plt.show()

# Data relative error
volt = np.array([v for v in sol[2] if len(v) > 1])

plt.scatter(xy[:, 0], xy[:, 1], s=7, c=volt[:, 4], vmin=0, vmax=0.4, cmap='coolwarm')
plt.show()

plt.scatter(xy[:, 0], xy[:, 1], s=7, c=true_data[:, 4], vmin=0, vmax=0.4, cmap='coolwarm')
plt.show()

plt.scatter(xy[:, 0], xy[:, 1], s=7, c=volt[:, 5], vmin=-25, vmax=0, cmap='coolwarm')
plt.show()

plt.scatter(xy[:, 0], xy[:, 1], s=7, c=true_data[:, 5], vmin=-25, vmax=0, cmap='coolwarm')
plt.show()

# %% STEPII Interpreted model
results_dir = jp('/Users/robin/PycharmProjects/MGS', 'results/paper/field_data/WFB')
subs = 'STEPII'
result_folder = jp(results_dir, subs)

int_mod_file = jp('/Users/robin/PycharmProjects/MGS',
                  'results/paper/field_data/WFB/STEPII/field_data_interpreted.dat')

int_mod = crc.datread(int_mod_file, start=1)[:, 2]

model_map(polygons=blocks, vals=10 ** int_mod, log=1, cbpos=bpos,
          levels=res_levels,
          folder=result_folder, fontsize=10, labelsize=labelsize,
          figname=None, extension='pdf')
plt.show()

# %% STEPIII Ref model smooth
subs = 'STEPIII_ref'
result_folder = jp(results_dir, subs)

sol, files = crc.import_res(result_folder=result_folder, return_file=1)

# Res plot
res = sol[0]

model_map(polygons=blocks, vals=10 ** res, log=1, cbpos=bpos,
          levels=res_levels,
          folder=result_folder, fontsize=10, labelsize=labelsize,
          figname=None, extension='pdf')
plt.show()

# %% STEPIV Ref model smooth
results_dir = jp('/Users/robin/PycharmProjects/MGS', 'results/paper/field_data/WFB')
subs = 'STEPIV_ref'
result_folder = jp(results_dir, subs)

sol, files = crc.import_res(result_folder=result_folder, return_file=1)

# Res plot
res = sol[0]

model_map(polygons=blocks, vals=10 ** res, log=0, cbpos=bpos,
          levels=res_levels,
          folder=result_folder, fontsize=10, labelsize=labelsize,
          figname=None, extension='pdf')
plt.show()

# IP plot
ip = sol[1]
ipt = np.copy(np.abs(ip / m2p))
# cut = 150
# ipt[ipt > cut] = cut
ipmodt = ipmod / m2p
# ip_levels = np.linspace(min(ipt), cut, 7)
# ip_levels = sorted(set(ipmod/m2p))
model_map(polygons=blocks, vals=ipt, log=0, cbpos=bpos, levels=ip_levels,
          folder=result_folder, fontsize=10, labelsize=labelsize,
          figname=None, extension='pdf')
plt.show()

# %% WFA
results_dir = jp('/Users/robin/PycharmProjects/MGS', 'results/paper/field_data/WFA_12')
subs = ''
result_folder = jp(results_dir, subs)

sol, files = crc.import_res(result_folder=result_folder, return_file=1)

# Res plot
res = sol[0]

# lev = 10**np.linspace(min(resmod), max(resmod), 12)

model_map(polygons=blocks, vals=10 ** res, log=0, cbpos=bpos,
          levels=res_levels,
          folder=result_folder, fontsize=10, labelsize=labelsize,
          figname=None, extension='pdf')
plt.show()

# IP plot
ip = sol[1]
ipt = np.copy(np.abs(ip / m2p))
# cut = 150
# ipt[ipt > cut] = cut
ipmodt = ipmod / m2p
# ip_levels = np.linspace(min(ipt), cut, 7)
# ip_levels = sorted(set(ipmod/m2p))
model_map(polygons=blocks, vals=ipt, log=0, cbpos=bpos, levels=ip_levels,
          folder=result_folder, fontsize=10, labelsize=labelsize,
          figname=None, extension='pdf')
plt.show()

# %% DOI

# Load solution

results_dir = jp('/Users/robin/PycharmProjects/MGS', 'results/paper/field_data/DOI')
subs = 'DOI10'
result_folder = jp(results_dir, subs)
sol, files = crc.import_res(result_folder=result_folder, return_file=1)
res10 = sol[0]

results_dir = jp('/Users/robin/PycharmProjects/MGS', 'results/paper/field_data/DOI')
subs = 'DOI1000'
result_folder = jp(results_dir, subs)
sol, files = crc.import_res(result_folder=result_folder, return_file=1)
res1000 = sol[0]

doi = np.abs((res1000 - res10) / 2)
doi_levels = np.linspace(doi.min(), doi.max(), 8)

model_map(polygons=blocks,
          vals=doi, log=0,
          stepy=12,
          contour=None,
          ndec=2,
          cmap_name='PuBu',
          cbpos=bpos, levels=doi_levels,
          folder=results_dir,
          figname='DOI', fontsize=10, labelsize=labelsize, extension='pdf')
plt.show()
