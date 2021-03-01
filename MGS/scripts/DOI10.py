"""
Compute the DOI with resistivity value 100
"""

#  Copyright (c) 2021. Robin Thibaut, Ghent University

# %% Imports
import os
from os.path import join as jp

from tomopal.crtomopy.crtomo import crc

# %% Directories

cwd = os.getcwd()  # Current working directory
sub_folder_name = "paper"
data_dir = jp(cwd, "data", sub_folder_name)  # Data files directory
mesh_dir = jp(cwd, "mesh", sub_folder_name)  # Mesh files directory
iso_dir = jp(cwd, "iso", sub_folder_name)  # ISO file dir
ref_dir = jp(cwd, "ref", sub_folder_name)  # Reference model files dir
start_dir = jp(cwd, "start", sub_folder_name)  # Start model files dir

results_dir = jp(cwd, "results", sub_folder_name, "field_data",
                 "DOI10")  # Results files directory

# %% Exe names

mesh_exe_name = jp(cwd, "mesh", "mesh.exe")
crtomo_exe_name = jp(cwd, "crtomo.exe")

# %%  Create crtomo object

myinv = crc.Crtomo(
    working_dir=cwd,
    data_dir=data_dir,
    mesh_dir=mesh_dir,
    iso_dir=iso_dir,
    ref_dir=ref_dir,
    start_dir=start_dir,
    crtomo_exe=crtomo_exe_name,
    mesh_exe=mesh_exe_name,
)

# %%  Generating the mesh
# Data file name A B M N R
df = jp(data_dir, "elecs.dat")
dat = crc.datread(df)

# Electrode spacing
es = 5

#  Electrodes elevation
ef = jp(data_dir, "field_data_elevation.dat")  # Data elevation file name X Z
elev = crc.datread(ef)

# %% Make the mesh
mshf = jp(mesh_dir, "Mesh.dat")

if not os.path.exists(mshf):
    myinv.meshmaker(abmn=dat[:, [0, 1, 2, 3]],
                    electrode_spacing=es,
                    elevation_data=elev)

# %% Read the mesh data (number of cells, blocks coordinates, x-y coordinates of the center of the blocks) from Mesh.dat
ncol, nlin, nelem, blocks, centerxy, nodes = crc.mesh_geometry(mshf)

# %% Buid configuration file
myinv = crc.Crtomo(
    working_dir=cwd,
    data_dir=data_dir,
    mesh_dir=mesh_dir,
    iso_dir=iso_dir,
    ref_dir=ref_dir,
    start_dir=start_dir,
    crtomo_exe=crtomo_exe_name,
    mesh_exe=mesh_exe_name,
)

# 0 Mesh.dat file
mesh_file = mshf  # Should keep this default name

# 1 elec.dat file
elec_file = jp(mesh_dir, "elec.dat")  # Should keep this default name

# 2 Data file
data_file = jp(data_dir, "field_data.dat")

# 3 Results folder file
# frname = uuid.uuid4().hex  # If you want to save the results in a sub-folder in the main results folder
# result_folder = jp(results_dir, 'WFA_', frname)

frname = ""

result_folder = jp(results_dir, frname)

# 8 Flag for reference model constraint (0/1)
reference_model = 3
#
# reference_model_file = jp(cwd,
#                           'ref',
#                           'paper',
#                           'field_data_interpreted.dat')
reference_model_file = jp(cwd, "ref", "paper", "doi10.dat")
val = 3
with open(reference_model_file, "w") as smf:
    smf.write(str(nelem) + "\n")
    [
        smf.write(
            str(10**val) + "\t" + "0" + "\t" + str(val) + "\t" + "0" + "\n")
        for i in range(nelem)
    ]
    smf.close()

# %% 12 File for reference model (model weights)

reference_weights_file = jp(cwd, "ref", "paper", "ref_005.dat")

# dm = crc.datread(reference_model_file, start=1)
# rfwm = ModelMaker(model_name=reference_weights_file, blocks=blocks, values=dm[:, 0], values_log=1, bck=0.05)
#
# with open(reference_weights_file, 'w') as rw:
#     rw.write(str(nelem) + '\n')
#     [rw.write('0.05' + '\n') for i in range(nelem)]
#     rw.close()

# %% 22 Maximum numbers of iterations
iterations = 30

# 23 Min data RMS
rms = 1.0

# 24 Flag for DC inversion (0/1)
dc = 1

# 25 Flag for robust inversion (0/1)
robust = 1

# 26 Flag for checking polarity (0/1)
check_polarity = 1

# 27 Flag for final phase improvement (0/1)
final_phase_improvement = 1

# 29 Relative magnitude error level (%)
error_level = 1
# error_level = 0.5 + 2 * np.random.rand()

# 30 Minimum absolute magnitude error (ohm)
min_abs_error = 0.00015

# 31 Error in phase (mrad)
phase_error = 0.2
# phase_error = 0.1 + 2 * np.random.rand()

# 36 Flag for MGS inversion (0/1)
mgs = 0

# 37 Beta value
# beta = 0.0016090885664409743
beta = 12e-4
# beta = 10e-4 + np.random.rand()*10e-4

# 38 Flag for starting model (0/1)
starting_model = 0


# 39 Starting model file
def my_func(data):
    return 1.05 * data


# smooth_file = \
#     jp(cwd, 'results', 'paper', 'scenario', 'WFB', 'STEPIII', 'config', 'forwardscenariostartmodelwithIP.dat')
# smooth_wfa = crc.res2mod(smooth_file, processing_function=my_func)

smooth_file = jp(cwd, "results", "paper", "field_data", "WFB", "STEPI",
                 "rho27.txt")
smooth_wfa = crc.res2mod(smooth_file, processing_function=my_func)

starting_model_file = smooth_wfa

# %% 19 ISO file 1
iso_file1 = jp(iso_dir, "iso.dat")  # Should keep this default name

# dm = datread(starting_model_file, header=1)[:, 0]
# isom = ModelMaker(blocks=blocks, values=dm, values_log=1, bck=1)
# #
# with open(iso_file1, 'w') as rw:
#     rw.write(str(nelem)+'\n')
#     [rw.write('{} 1'.format(str(i))+'\n') for i in isom.final_results]
#     rw.close()
with open(iso_file1, "w") as rw:
    rw.write(str(nelem) + "\n")
    rr = 1
    # rr = np.round(1 + np.random.rand(), 2)
    [rw.write("1 {}".format(str(rr)) + "\n") for i in range(nelem)]
    rw.close()

# %% Generate configuration file

myinv.write_config(
    erase=1,
    resolution_mtx=0,
    mesh_file=mesh_file,
    elec_file=elec_file,
    data_file=data_file,
    result_folder=result_folder,
    reference_model=reference_model,
    reference_model_file=reference_model_file,
    reference_weights_file=reference_weights_file,
    iso_file1=iso_file1,
    iterations=iterations,
    rms=rms,
    dc=dc,
    robust=robust,
    check_polarity=check_polarity,
    final_phase_improvement=final_phase_improvement,
    error_level=error_level,
    min_abs_error=min_abs_error,
    phase_error=phase_error,
    mgs=mgs,
    beta=beta,
    starting_model=starting_model,
    starting_model_file=starting_model_file,
)

myinv.run()
