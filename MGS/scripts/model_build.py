"""
Interactively construct an interpreted resistivity/ip model
"""

#  Copyright (c) 2021. Robin Thibaut, Ghent University

import os
from os.path import join as jp
from tomopal.crtomopy.crtomo import crc
from tomopal.geoview.diavatly import model_map
from tomopal.model.mohinh import ModelMaker

cwd = os.getcwd()  # Current working directory
sub_folder_name = 'paper'
mesh_dir = jp(cwd, 'mesh', sub_folder_name)  # Mesh files directory
mshf = jp(mesh_dir, 'Mesh.dat')
iso_dir = jp(cwd, 'iso', sub_folder_name)  # ISO file dir

ncol, nlin, nelem, blocks, centerxy = crc.mesh_geometry(mshf)

iso_file1 = jp(iso_dir, 'iso_iso.dat')
start_dir = jp(cwd, 'start', sub_folder_name)
starting_model_file = jp(start_dir, 'rho07.dat')

dm = crc.datread(starting_model_file, start=1)[:, 0]
isom = ModelMaker(blocks=blocks, values=dm, values_log=1, bck=1)
#
with open(iso_file1, 'w') as rw:
    rw.write(str(nelem)+'\n')
    for val in isom.final_results:
        if val > 1:
            rw.write('{} {}'.format(str(val), str(1)) + '\n')
        if val < 1:
            rw.write('{} {}'.format(str(1), str(1/val)) + '\n')
        if val == 1.0:
            rw.write('{} {}'.format(str(1), str(1)) + '\n')
    rw.close()
