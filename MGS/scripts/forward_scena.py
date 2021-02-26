"""
Forward modelling for the synthetic scenario model.
"""

#  Copyright (c) 2021. Robin Thibaut, Ghent University

# %% Imports
import os
from os.path import join as jp

import numpy as np
from tomopal.crtomopy.crtomo import crc

# %% Directories

cwd = os.getcwd()  # Current working directory
sub_folder_name = 'paper'
data_dir = jp(cwd, 'data', sub_folder_name)  # Data files directory
mesh_dir = jp(cwd, 'mesh', sub_folder_name)  # Mesh files directory
iso_dir = jp(cwd, 'iso', sub_folder_name)  # ISO file dir
ref_dir = jp(cwd, 'ref', sub_folder_name)  # Reference model files dir
start_dir = jp(cwd, 'start', sub_folder_name)  # Start model files dir
results_dir = jp(cwd, 'results', sub_folder_name)  # Results files directory

# %% Exe names

mesh_exe_name = jp(cwd, 'mesh', 'mesh.exe')
crtomo_exe_name = jp(cwd, 'crtomo.exe')

# %%  Generating the mesh
# Data file name A B M N R
df = jp(data_dir, 'elecs.dat')
dat = crc.datread(df)

# Electrode spacing
es = 5

#  Electrodes elevation
ef = jp(data_dir, 'field_data_elevation.dat')  # Data elevation file name X Z
elev = crc.datread(ef)

# %% Make the mesh
mshf = jp(mesh_dir, 'Mesh.dat')

# %% Read the mesh data (number of cells, blocks coordinates, x-y coordinates of the center of the blocks) from Mesh.dat
ncol, nlin, nelem, blocks, centerxy, nodes = crc.mesh_geometry(mshf)

# Define modelling parameters

# 0 Mesh.dat file
mesh_file = mshf  # Should keep this default name

# 1 elec.dat file
elec_file = jp(mesh_dir, 'elec.dat')  # Should keep this default name

# 2 Data file
data_file = jp(data_dir, 'scenario.dat')

# 3 Results folder file
# frname = uuid.uuid4().hex  # If you want to save the results in a sub-folder in the main results folder
# result_folder = jp(results_dir, 'WFA_', frname)

frname = 'forward_scenario'

result_folder = jp(results_dir, frname)

# Forward modeling

# Results folder file
fwname = 'forward_scena'  # If you want to save the results in a sub-folder in the main results folder

result_folder_fwd = jp(results_dir, fwname)

# Initiate forward modelling object
myfwd = crc.Crtomo(working_dir=cwd,
                   data_dir=data_dir,
                   mesh_dir=mesh_dir,
                   iso_dir=iso_dir,
                   ref_dir=ref_dir,
                   start_dir=start_dir,
                   crtomo_exe=crtomo_exe_name,
                   mesh_exe=mesh_exe_name)

# Write configuration file
myfwd.write_config(mesh_file=mesh_file,
                   elec_file=elec_file,
                   iso_file1=jp(iso_dir, 'iso.dat'),
                   data_file=jp(data_dir, 'field_data.dat'),
                   fwd_only=1,
                   starting_model=1,
                   result_folder=result_folder_fwd,
                   starting_model_file=jp(cwd, 'data', 'paper', 'models', 'forwardscenario.dat'))

# Run forward modelling
myfwd.run()

# Read results
volt_file = 'results/paper/forward_scena/volt.dat'
volt = crc.datread(volt_file, start=1)

# Add noise
std = 1
volt_rg = volt[:, 4] + std * np.random.rand(len(volt))