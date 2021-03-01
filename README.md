# MGS-public
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4763a876682f4f36af7240b4c92882a6)](https://app.codacy.com/gh/robinthibaut/MGS-public?utm_source=github.com&utm_medium=referral&utm_content=robinthibaut/MGS-public&utm_campaign=Badge_Grade_Settings)

### [A new workflow to incorporate prior information in minimum gradient support (MGS) inversion of electrical resistivity and induced polarization data](https://www.sciencedirect.com/science/article/abs/pii/S0926985121000331)

#### Authors
**Robin Thibaut**, Thomas Kremer, Annie Royen, Bun Kim Ngun, Frédéric Nguyen, Thomas Hermans

For any enquiries, please contact the corresponding author.

#### DOI
https://doi.org/10.1016/j.jappgeo.2021.104286

#### Description 
This repository contains excerpts from the code used to realize the research paper mentioned above, published in [Journal of Applied Geophysics](https://www.sciencedirect.com/journal/journal-of-applied-geophysics).

The code itself relies on the [Tomopal package](https://pypi.org/project/tomopal/) also available in this [repository](https://github.com/robinthibaut/TomoPal).

To perform inversions and forward modelling, it is necessary to obtain a copy of the CRTOMO software ([Kemna, 2000](https://www.geo.uni-bonn.de/mitarbeiter/Andreas-Kemna/dissertation)) (not included in the repository).

#### Abstract

The current paradigm for geophysical inversions is to select the simplest solution according to Occam's principle. The implicit assumption usually made is that the parameters of interest have a smooth spatial distribution, which is rarely geologically plausible. An alternative is the Minimum Gradient Support (MGS), a functional that allows to compute a regularized inversion favoring sharp contrasts. However, solutions are highly sensitive to the selection of a variable called the focusing parameter β and the method is not very performant when many structures are present in the subsurface. Thus, we propose a new workflow to apply this functional to real case studies where heterogeneous structures are expected: a smooth solution is first computed and used as a starting model for sharp MGS inversions. Sequentially incorporating additional prior information on resistivity (e.g., from drillings, previous geophysical surveys) is possible and further improves imaging for resistivity and chargeability structures. The new methodology is first tested on a synthetic case and then applied to ERT/IP data collected on a gold deposit. The methodology enables to compute plausible electrical resistivity spatial distributions in accordance with the vast prior geological knowledge, and reveals new insights about the mineralization key characteristics. The choice of β remains challenging and should be automated in future developments.

#### Repository structure

##### config

Contains a CRTOMO configuration file crtritime.cfg.

##### data

Contains data files (electrode configuration, tomography results, elevation data...). 
Note that the original field dataset is not included in the repository for confidentiality reasons. Instead, fake data has been generated in the field_data.dat file.

##### ip

Contains IP configuration files to convert complex IP data to time-domain.

##### iso 

Contains structural constraint files for the inversions (horizontal and vertical weights ).

##### mesh

Contains the computational mesh data.

##### ref

Contains reference models files used in the paper.

##### results

Contains the results of the different steps described in the paper.

##### scripts 

Contains all the script used to compute the results.