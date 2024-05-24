# Building the Parallel Version of MODFLOW 6

This file provides the instructions for obtaining MODFLOW 6 source code, installing a conda environment with a Fortran compiler and the required compiling dependencies, and building the parallel version of MODFLOW 6.

## Step 1. Clone the modflow6 repository from GitHub
The following command can be used to clone the modflow6 repository.

```
git clone https://github.com/MODFLOW-USGS/modflow6.git
```

This will download the repository and create a new folder called `modflow6` in the working directory.

## Step 2. Create the `mf6xtd` Conda Environment
Next, you will create a conda environment, called `mf6xtd`, that will be used to compile the parallel version of MODFLOW 6.  The `mf6xtd` environment will have all of the software needed to compile serial and parallel versions of MODFLOW 6.

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

This `mf6xtd_environment.yml` will be used to create the `mf6xtd` environment by running the following command:

```
conda env create -f mf6xtd_environment.yml
```

## Step 3. Build MODFLOW

To build the parallel version of MODFLOW, simply run the following commands from a terminal with the `mf6xtd` environment activated.

```
conda activate mf6xtd
cd modflow6
meson setup builddir -Ddebug=false -Dparallel=true --prefix=$(pwd) --libdir=bin
meson install -C builddir
meson test --verbose --no-rebuild -C builddir
```

If everything is working properly, then the last command should show that the tests completed ok and without errors.

## Step 4. Make Symbolic Link
For convenience you may wish to create a sybmolic link to the MODFLOW 6 executable, which will be located in the `bin` folder of the modflow6 repository if Step 3 was successful.

To make this new MODFLOW 6 executable available for future simulations, add a symbolic link to the newly compiled binary executable (`./bin/mf6`).  If you created the `mfandmore2024` environment for the workshop, then the `bin` folder for that environment will likely be located here: `~/miniconda3/envs/mfandmore2024/bin`.  The following command will put a symbolic link to the parallel version of MODFLOW in that conda environment folder.  This will make the parallel version of MODFLOW 6 available whenever that environment is active.

```
ln ./bin/mf6 ~/miniconda3/envs/mfandmore2024/bin/mf6
```
