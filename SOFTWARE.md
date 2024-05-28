# Software Installation
To get the most out of this workshop, you will need to come prepared with a laptop computer that has Python installed.  **If you are familiar with conda environments and know how to create a new conda environment using an environment.yml file, then skip ahead to Part 2**.  For all others, we recommend using the Miniforge software to download and install Python and required dependencies needed for the workshop.  

The following instructions will guide you through the installation process and setup of a mfandmore2024 environment.

## Part 1 -- Install Miniforge
1. Go to the miniforge website and download the installer (https://github.com/conda-forge/miniforge) for your platform.

2. Run the installer program that you downloaded.  On Windows the installer is called `Miniforge3-Windows-x86_64.exe`.

3. Click through the installer options, and select "Just Me (recommended)" if asked.  Default installation options should be fine, with the exception that you should select an installation location that does not have any special characters or spaces in it.

4. After installation, you should see "Miniforge Prompt" as a program under the Windows Start menu.

## Part 2 -- Create an Environment File
We will use an environment file to create a containerized version of Python and the Python packages needed for the class.  An environment file is simply a list of packages that we want to install in our environment.

1. Using a text editor, such as Notepad or Notepad++, create a file called `environment.yml`.  It should contain the information in [this environment file](./environment.yml).  Save this file to your hard drive, preferably in your user home folder so that it can be easily accessed in the next step. (Caution!  Notepad will automatically append a .txt suffix to your file name; you don't want this to happen.)

2. **For Mac and Linux users only!** You will need to add six additional dependencies to the `environment.yml` file from step 1.  The following dependencies are also required: 

```
  # parallel modflow build dependencies
  - pkg-config
  - openmpi
  - gfortran
  - petsc
  - meson>=1.1.0
  - ninja
```  

## Part 3.  Create the `mfandmore2024` Environment

1. Start the miniforge prompt from the Windows start menu (or equivalent on Mac or Linux) to bring up a terminal.

2. At the terminal prompt enter the following command, where `<path to file>` is the location of the `environment.yml` file that you created in Part 2.  You will need to be connected to the internet for this to work properly.  The installation process may take a couple of minutes.
```
mamba env create --file <path to file>/environment.yml
```

3.  After the environment has been installed, you may activate this new class environment with the following command
```
mamba activate mfandmore2024
```

4.  The windows terminal prompt should reflect the current environment:
```
(mfandmore2024) C:\Users\JaneDoe>
```

5.  We will be using jupyter notebooks in the workshop.  To test if jupyter is installed and working properly use the following command.  After entering this command, the default web browswer should open to a Jupyter Lab page.
```
jupyter lab
```

For most users, the setup is complete at this point.  For those working on a Mac or Linux laptop, please proceed to Part 4.


## Part 4.  Obtaining MODFLOW 6

We will be using the parallel version of MODFLOW 6 in this workshop.  If you are working on Windows, then you can download the parallel version of MODFLOW 6 from [here](https://github.com/MODFLOW-USGS/modflow6/releases/tag/6.5.0).  Note that we will also walk through this step during the workshop.  The distribution file for windows that includes the parallel version is called `mf6.5.0_win64par.zip`.

If you are using a Mac or Linux laptop for the workshop, then you will need to build the parallel version of MODFLOW.  We have simplified the build process, which can be completed in just a few minutes.  Instructions for building the parallel version of MODFLOW 6 are located [here](./build_parallel_mf6.md).


# Preparation for the Workshop
If you have never used Python before, there are many online resources for getting started.  A recommendation is to start with the tutorial at https://cscircles.cemc.uwaterloo.ca/.

# If Software Installation Fails

Notebooks can be run from mybinder.org by clicking the button below.

[![badge](https://img.shields.io/badge/launch-binder-579ACA.svg?logo=data:image/png;base64,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)](https://mybinder.org/v2/gh/langevin-usgs/modflow-training-princeton2024/HEAD)

We have had some problems running the notebooks through mybinder.org when internet connections are intermittent.  A local software installation on a laptop is preferred.