# Building the Parallel Version of MODFLOW 6

This file provides the instructions for obtaining MODFLOW 6 source code, installing a conda environment with a Fortran compiler and the required compiling dependencies, and building the parallel version of MODFLOW 6.

## Cloning MODFLOW Resources from GitHub
A first step is to clone the GitHub repositories for MODFLOW 6 and the MODFLOW 6 parallel class.

```
git clone https://github.com/MODFLOW-USGS/modflow6.git
```

## Installing the `mf6xtd` Conda Environment
Next, you will create a conda environment, called `mf6xtd`, that will be used for thie class.  The `mf6xtd` environment will have all of the software needed to compile serial and parallel versions of MODFLOW 6, and the Python packages needed to pre- and post-process MODFLOW models.

The steps for creating the `mf6xtd` conda environment are as follows

Create a an environment file that has the following contents.  Call this file `mf6xtd_environment.yml`

```
name: mf6xtd

channels:
  - conda-forge

dependencies:
  - pkg-config
  - openmpi
  - gcc
  - gfortran
  - petsc
  - meson>=1.1.0
  - ninja
```

From this environment file, the `mf6xtd` environment will be created by initiating the following command:

```
conda env create -f mf6xtd_environment.yml
```

## Building MODFLOW

To build the parallel version of MODFLOW, simply run the following commands from a terminal with the `mf6xtd` environment activated.

```
cd modflow6
meson setup builddir -Ddebug=false -Dparallel=true --prefix=$(pwd) --libdir=bin
meson install -C builddir
meson test --verbose --no-rebuild -C builddir
```

If everything is working properly, then the last command should show that the tests completed ok and without errors.

## Make a Symbolic Link

xxx -- Provide instructions for symbolically linking to the newly compiled binary executable.