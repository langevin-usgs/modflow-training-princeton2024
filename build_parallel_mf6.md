# Building the Parallel Version of MODFLOW 6

These are the instructions for obtaining the MODFLOW 6 source code and building the parallel version of MODFLOW 6.  Note that requires adding additional dependencies to the `environment.yml` file described on the [software](./SOFTWARE.md) page.

## Step 1. Clone the modflow6 repository from GitHub
The following command can be used to clone the modflow6 repository.

```
git clone https://github.com/MODFLOW-USGS/modflow6.git
```

This will download the repository and create a new folder called `modflow6` in the working directory.

## Step 2. Activate your `mfandmore2024` Conda Environment

Activate the `mfandmore2024` environment:

```
conda activate mfandmore2024
```

## Step 3. Build MODFLOW

To build the parallel version of MODFLOW, simply run the following commands from a terminal.

```
cd modflow6
meson setup builddir -Ddebug=false -Dparallel=true --prefix=$(pwd) --libdir=bin
meson install -C builddir
meson test --verbose --no-rebuild -C builddir
```

If everything is working properly, then the last command should show that the tests completed ok and without errors.  The message should look something like the following:

```
――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
5/5 Parallel simulation test - 2 cores  OK              0.20s
 
 
Ok:                 5
Expected Fail:      0
Fail:               0
Unexpected Pass:    0
Skipped:            0
Timeout:            0
 
Full log written to /home/user/modflow-training-princeton2024/modflow6/builddir/meson-logs/testlog.txt has context menu
```

## Step 4. Make Symbolic Link
For convenience you may wish to create a sybmolic link to the MODFLOW 6 executable, which will be located in the `bin` folder of the modflow6 repository if Step 3 was successful.

To make this new MODFLOW 6 executable available for future simulations, add a symbolic link to the newly compiled binary executable (`./bin/mf6`).  If you created the `mfandmore2024` environment for the workshop, then the `bin` folder for that environment will likely be located here: `~/miniconda3/envs/mfandmore2024/bin`.  The following command will put a symbolic link to the parallel version of MODFLOW in that conda environment folder.  This will make the parallel version of MODFLOW 6 available whenever that environment is active.

```
ln ./bin/mf6 ~/miniconda3/envs/mfandmore2024/bin/mf6
```
