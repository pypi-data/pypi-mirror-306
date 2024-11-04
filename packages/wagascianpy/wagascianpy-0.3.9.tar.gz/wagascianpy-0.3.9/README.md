# WAGASCI ANPAN for Python v0.3.9

This package contains all the Python modules used by the ANPAN
 framework of the WAGASCI/T2K experiment.

## What is ANPAN?

ANPAN (Acquisition Networked Program for Accelerated Neutrinos) is a collective
 name to identify all the software used to acquire data and analyze it for
  the WAGASCI experiment. It is composed of many packages:
  - [Pyrame](http://llr.in2p3.fr/sites/pyrame/) (C/Python2)
  - [ANPAN DAQ](https://llrgit.in2p3.fr/online/wagasci) (C/Python2)
  - [WagasciCalibration](https://git.t2k.org/wagasci_babymind/WagasciCalibration) (C++11)
  - [WagasciMidas](https://git.t2k.org/wagasci_babymind/WagasciMidas) (C++11/JS)
  - [WagasciRunControl](https://git.t2k.org/wagasci_babymind/WagasciRunControl) (Python2)
  - [WagasciAnpy (this package)](https://git.t2k.org/wagasci_babymind/WagasciAnpy) (Python2/3)

## Python compatibility

 - **Python2.7 or Python3.4+**

 This package is fully compatible with both Python2.7 and Python3.4+. It is
 tested usually with Python 3.8 and sporadically with other Python versions.
 
 However, I strongly suggest you to use Python 3 whenever possible because
 Python 2 has now reached end of life and many packages are starting to drop 
 support for it. I am still trying to ensure Python 2 compatibility but I might 
 drop it in the future for non DAQ related modules.

## Dependencies

Many functions of this package depend on ROOT

 - [ROOT](https://ph-root-2.cern.ch/)

To use the analysis programs, you need the WagasciCalibration package:

  - [WagasciCalibration](https://git.t2k.org/wagasci_babymind/WagasciCalibration)

To download and update the WAGASCI run database you may need the BorgBackup
 program:

  - [BorgBackup](https://borgbackup.readthedocs.io/en/stable/installation.html)

The ``pyrmod`` module depends on Pyrame. This module is used only by the DAQ
so no need to install Pyrame on a non DAQ machine. 

### ROOT

Be sure that the version of ROOT that you installed is compatible with
your Python version. The precompiled binaries for ROOT until version 6.22.0
are usually only compatible with Python 2. From ROOT version 6.22.0 on,
ROOT should be compatible with both Python 2 and Python 3, so my suggestion
is to just update your ROOT version.

### WAGASCI calibration software (optional)

To analyze the raw data you need the WAGASCI calibration software.
For the installation instructions refer to 
 [this page](https://git.t2k.org/wagasci_babymind/WagasciCalibration).

## Installation (Linux)

Open a terminal and issue
```shell script
python3 -m pip install --upgrade --user wagascianpy
or (recomended)
python3 -m pip install --upgrade --user .
```

## Installation (MacOS)

Currently the support for MacOS is only partial. The SSH connection is broken
because of some issues internal to the [Python paramiko
module](http://www.paramiko.org/), so the program can be used in local mode
only. I tried to fix the issue but the problem is beyond my skills.  Probably in
the following months the paramiko developers will come up with a solution. At
the time of writing, the current (broken) version of paramiko is 2.7.1. When a
new version of paramiko is released, try again to run the software and see what
happens.

I have tested the program only in MacOS Mojave and MacOS Catalina. Both showed
more or less the same problems. You can try older versions of MacOS and might
have better luck.

#### MacOS Mojave/Catalina

Because MacOS Mojave does not bundle Python3 we need to install it manually. The
easiest way is by using the package manager brew. The following commands are
taken from this [webpage](https://installpython3.com/mac/).

The first step is to install the Apple's Xcode suite. Most probably you already
have it already installed, in that case you can skip this step. In your Terminal
app, run the following command to install XCode and its command-line tools:

```shell script
$ xcode-select --install
```

Next install Homebrew by copy/pasting the following command into Terminal and
then type Enter:

```shell script
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
$ brew update
```

To confirm Homebrew installed correctly, run this command:
```shell script
$ brew doctor
Your system is ready to brew.
```

Now we can install the latest version of Python 3. Type the following command
into Terminal and press Enter:

```shell script
$ brew install python3
```

To confirm which version of Python was installed, run the following command in
Terminal:

```shell script
$ /usr/local/bin/python3 --version
Python 3.7.7
```

Many functions of the WAGASCI database viewer use borgbackup. We can easily
install it using brew.

```shell script
$ brew cask install borgbackup
```

For other ways of installing borg refer to the
[borg website](https://borgbackup.readthedocs.io/en/stable/installation.html).

Then we can finally install the wagascianpy package

```shell script
$ python3 -m pip install --user --upgrade wagascianpy
```

If you use MacOS Catalina continue reading the next section.

#### MacOS Catalina - troubleshooting

**MacOS Catalina comes with its own version of Python3. However
[as stated in the Python website](https://www.python.org/download/mac/tcltk/)
the Apple-supplied Tcl/Tk 8.5 has serious bugs that can cause application 
crashes.

So follow the same instructions as MacOS Mojave but also install tkinter:
```shell script
$ brew install tcl-tk
```

## Configuration

### Environment parameters

You can easily configure all the parameters from the GUI itself (or from the
command line if you run the programs from the shell). However, because
inserting the same values over and over again can be tedius, you can modify the
configuration file called `wagasci.ini`. This file is created in the
`${HOME}/.wagasci` folder on the first execution of the program and filled with
the default values. You can just open and edit it with any text editor. The
options names and values are in one to one correlation with the GUI fields
and CLI arguments.

Upon start, the program tries to load the configuration file from the following
 directories in this order:
- Environment : `${WAGASCI_CONFIGDIR}`
- User : `${HOME}/.wagasci`
- System : `/usr/local/wagasci`

The configuration file must be called `wagasci.ini`. Both the WAGASCI database
viewer and the spill history plotter can use the same configuration file.

### Good runs 

The list of good runs and bad runs is hardcoded at the beginning of the 
`wagascianpy/database/wagascidb.py` file. If a run is completely bad, add it 
to the `_BAD_RUNS` list. If a run is bad only for a single detector, add it 
to the `_BAD_RUNS_X` where X is the name of the detector. After modifying 
the bad run list, to apply it again, please rerun `wagasciviewer.py 
--rebuild-wagasci-database --batch-mode`, and then `wagasciviewer.py 
--apply-detector-flags --batch-mode`.

### Markers

When drawing the history plots, the trouble markers and maintenance day 
markers can be drawn along with the data. The start time and stop time of 
these markers is hardcoded at the beginning of the 
`wagascianpy/plotting/marker.py` file.

## WAGASCI database viewer

![](../WagasciAnpy/docs/images/wagasciviewer.gif)

The following subsections explain the usage of the WAGASCI database viewer GUI
 program.

### Run the program

To open the GUI program, just type in a terminal:

```shell script
wagasciviewer.py
````

If you wish to run the program without a GUI in batch mode, just type in a
 terminal
 
 ```shell script
wagasciviewer.py --batch-mode <other arguments>
```

### WAGASCI run repository

The word repository refers to the place where the runs are backed up. It might
be a simple repository where the runs are stored without encription (plain file
and folders), or a borg repository where all the files are encripted. The
repository can be either local (same machine) or remote (remote machine
reachable by SSH). In case of a borg repository it is necessary for borgbackup
to be installed on both the local machine and the remote machine.

* **Simple repository** : Unencripted repository
* **Borg repository** : Borg repository
* **Repository location** : For a remote repository the syntax is
  `<hostname>:<path of repository>`. The SSH configuration is taken from the
  user `~/.ssh/config` file by looking for `<hostname>`, so make sure that you
  can connect to the remote machine by just opening the terminal and `ssh
  <hostname>`. In case of local repository just insert the repository path. For
  more info about how to connect to KEKCC by SSH refer to the [WAGASCI expert
  shifter manual](https://ja.overleaf.com/7887288445tmqmnjknrynm)
  (Troubleshooting - KEKCC (8.6)).

### WAGASCI run database

Location of the WAGASCI run database. The database is a file (usually named
`wagascidb.db`) that contains some info about each run. If the update database
checkbox is checked, the software checks if the database is synchronized with
the repository (if the database describes the current state of the repository).

* **Database location**: location of the database file. Usually it is the same
  as the repository. In case you specify a different location, enter the
  filename too. Leave as it is if in doubt.
* **Update database**: If left unchecked the database is read as is. If checked,
  the runs that are present in both the repository and database the database are
  not updated and only the runs that are present in the repository but not in
  the database are added. Leave disabled if in doubt.
* **Rebuild database**: If checked each run in the repository is
  inserted/overwritten into the database even if already present. Leave disabled
  if in doubt.
* **WAGASCI library**: path to the directory containing the WAGASCI
  calibration software libraries. It is only used to update the database and
  analyze the raw data. Not needed if you only wish to visualize the database.
  
### Beam Summary Data repository

The word repository refers to the place where the Beam Summary Data files are
stored.  The local repository can be an empty folder or a folder containing
the BSD files.  If the remote repository field is left empty the program assumes
that the BSD files are already present in the local folder. If the remote
repository field is filled, the remote repository and the local repository are
synchronized using rsync.


* **Local repository** : Location of BSD files in the local machine.
* **Remote repository** : Location of the BSD files in the remote machine (the
  syntax is the same as the WAGASCI run repository). If left empty only the
  local repository is used.

### Beam Summary Data database

Location of the BSD database. The database is a file (usually named `bsddb.db`)
that contains some info about each BSD file. If the update or rebuild database
checkbox is checked, the software checks if the database is synchronized with
the repository (if the database describes the current state of the repository).

* **Database location**: location of the database file. Usually it is the same
  as the repository. In case you specify a different location, enter the
  filename too. Leave as it is if in doubt.
* **Update database**: If left unchecked the database is read as is. If checked,
  the runs that are present in both the repository and database the database are
  not updated and only the runs that are present in the repository but not in
  the database are added. Leave disabled if in doubt.
* **Rebuild database**: If checked each run in the repository is
  inserted/overwritten into the database even if already present. Leave disabled
  if in doubt.

### Query

#### Getters
* **Get time interval**: Select an interval and the push the Get interval
 button. In the Run list frame will appear all the runs in that period.
* **Get run interval**: Select all runs whose number is within the interval.
* **Get all**: Get all runs regardless of the interval.

#### Conditions:
* **Include overlapping runs**: If unchecked only the runs that start AND stop
  inside the time interval are shown. If checked all the runs that start OR stop
  inside the interval are shown.
* **Only good runs**: select only the runs marked as good (good_run_flag == 1)

#### Analyzers:
* **Download**: download the selected runs from the WAGASCI run repository into
 a local directory selected by the user (both borg and simple repositories
  are supported)
* **Decoder**: decode the downloaded runs using the wgDecoder program
* **ADC histogram**: plot the ADC distribution channel by channel
* **BCID histogram**: plot the BCID distribution for the whole DIF
* **Spill Number Fixer**: fix the spill number for the decoded runs using the
 wgFixSpillNumber program
* **Beam Summary Data**: integrate the BSD info into the decoded runs using the
 wgBeamSummaryData program
* **Temperature**: integrate the temperature info into the decoded runs using
 the wgTemperature program
* **ADC calibration**: insert PEU information in the decoded data TTree using
 the wgAdcCalib program
* **Start analysis**: apply all the selected analyzers above to the downloaded
 runs

#### Topology
* **Topology**: select which sub-detectors to download (not used for analysis)

### Run list

List of runs that meet the conditions in the query. You can click on the run
name to show more info about that particular run.

### Run info

Show all the info about one particular run.

### GUI customization
The GUI can be partially customized using the
[PyGubu](https://github.com/alejandroautalan/pygubu) program. PyGubu is
 automatically installed by pip as a dependence of this package.

 To customize the GUI, locate the package installation folder and the gui.ui
  file inside it, open a terminal and
 ```shell script
mkdir -p $HOME/.wagasci
cp gui.ui $HOME/.wagasci/
pygubu-designer $HOME/.wagasci/gui.ui
```

The program tries to load the GUI file `gui.ui` in the same way as the
 configuration file as explained above.

## WAGASCI spill history plotter

The ``history_plotter.py`` script is provided by this package. It creates various
history plots for the WAGASCI experiment. It is a CLI only script and all its
features can be controlled by command line arguments. However it also tries to
read the configuration file ``wagasci.ini`` for required arguments that are not
specified in the command line.

For further information, please consult the help message of the script:

```shell script
history_plotter.py --help
```

## MIDAS history to SQLite converter

To convert midas history files into SQLite format, please use the
 ``mhistory_sqlite_converter.py``, script. You need to have MIDAS installed
  to run the script.
  
  For further information, please consult the help message of the script:

```shell script
mhistory_sqlite_converter.py --help
```

## Calibration scripts

Many calibration scripts are provided by this package. They all take the raw
data as input and perform some calibration analysis on it. They depend
strongly on the [WAGASCI calibration software](https://git.t2k.org/wagasci_babymind/WagasciCalibration).

The documentation about how to use them is included in the [WAGASCI expert
 shifter manual](https://ja.overleaf.com/7887288445tmqmnjknrynm).

## Other Python modules

List of all the Python modules provided by this package:

- `wagascianpy.analysis`

  Contains modules for analysing the WAGASCI raw data, decoded data and slow
   data.
  - `wagascianpy.analysis.analysis` : Ctypes wrappers around
   WagasciCalibration libraries.
  - `wagascianpy.analysis.analyzer` : Takes the Ctypes wrappers and organize
   them in a abstract factory design patter.
  - `wagascianpy.analysis.beam_summary_data` : module to integrate the BSD
   information inside the decoded WAGASCI data. It can be used as a
    standalone program or as a analyzer of `wagascianpy.analysis.analyzer`.
  - `wagascianpy.analysis.mhistory2sqlite` : module to convert many mhistory
   files containing slow devices data into a SQLite database.
  - `wagascianpy.analysis.spill` : factory design patter to generate
   various spill objects. A spill object contains information about the spill
   number. It is useful when fixing the spill number bugs or when
   integrating the BSD information.

- `wagascianpy.database`

    Modules to manage the WAGASCI run database and the BSD database.

  - `wagascianpy.database.bsddb` : BSD database creation and access.
  - `wagascianpy.database.db_record` : Virtual database record that is
   inherited by the WAGASCI run record and BSD record.
  - `wagascianpy.database.my_tinydb` : Virtual database build upon the
   `tinydb` external module. It is inherited by the WAGASCI run database and
    BSD database.
  - `wagascianpy.database.wagascidb` : WAGASCI run database creation and access.

- `wagascianpy.plotting`

    Modules to generate history plots (plots where the X axis is time).

  - `wagascianpy.plotting.colors` : manage plot colors
  - `wagascianpy.plotting.detector` : class to store the read TTrees for each
   subdetector and to iterate over them.
  - `wagascianpy.plotting.graph` : class to build a generic graph
  - `wagascianpy.plotting.harvest` : class to harvest the needed data from the
   TTrees. It returns the X points and Y points. It is implemented using the
    strategy design pattern.
  - `wagascianpy.plotting.marker` : class to plot time markers as the
   maintenance days, WAGASCI runs start and stop time, electronics troubles
   , etc...
  - `wagascianpy.plotting.plotter` : class to plot the actual TMultiGraph
  - `wagascianpy.plotting.topology` : class to specify which subdetectors to
   plot and which not

- `wagascianpy.program`

    Modules to generate a runnable program using the analyzers of
    `wagascianpy.analysis.analyzer`. Implemented using the builder design
     pattern.

  - `wagascianpy.program.director` : director of the builder design pattern.
  - `wagascianpy.program.program` : final program that is builded.
  - `wagascianpy.program.program_builder` : builder that builds the program.

- `wagascianpy.pyrmod`

    Interface for the Pyrame modules. Used only for DAQ.
    
  - `wagascianpy.pyrmod.CCC` : control the CCC board
  - `wagascianpy.pyrmod.pyrmod` : wrapper around generic Pyrame module

- `wagascianpy.utils`

    Miscellaneous utilities.

  - `wagascianpy.utils.change_bitstream` : module to change the configuration of
   the SPIROC chip for all the chips in one go.
  - `wagascianpy.utils.classproperty` : implement Python property for classes
   and not only for instances
  - `wagascianpy.utils.configuration` : parse the configuration file and
   create a global configuration class
  - `wagascianpy.utils.environment` : module to read the WAGASCI
   environmental variables from a file or from the shell environment.
  - `wagascianpy.utils.utils` : all other utilities are gathered here.

- `wagascianpy.viewer`

    Module used by the WAGASCI database viewer GUI program. They are not
     supposed to be used anywhere else.

   - `wagascianpy.viewer.configuration` : fill the global configuration
   - `wagascianpy.viewer.downloader` : download runs from remote repository
   - `wagascianpy.viewer.parse_args` : parse the CLI arguments
   - `wagascianpy.viewer.show_run_info` : build the 'run info' tab in the GUI
   - `wagascianpy.viewer.topology` : little class to select which sub
   -detectors are enabled and which not
   - `wagascianpy.viewer.utils` - GUI utilities

## Troubleshooting

 - If you get an error about SSH trying to set a different locale in the KEKCC
repository try the solution explained in this
[stackoverflow post](https://stackoverflow.com/questions/29609371/how-do-not-pass-locale-through-ssh).
