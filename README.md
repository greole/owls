# Owls

![](https://badge.fury.io/py/owls.svg)
![](https://badge.fury.io/gh/greole%2Fowls.svg)
![](https://pypip.in/py_versions/owls/badge.svg)
![](https://travis-ci.org/greole/owls.svg?branch=master)

The Owls package is a collection of python tools for data analysis and
plotting of OpenFOAM cases. It provides the following basic functionality:

- A reader for OpenFOAM scalar and vector fields, set files and log files
- Converting OpenFOAM data to FoamFrames which are derived DataFrames from the pandas library


# Installation
Owls can be installed via pip

~~~~.bash
pip install Owls # non development version probably out of date
~~~~

For a more recent version install the development version

~~~~.bash
python setup.py install --user
~~~~


If you have docker installed you can use the automaticly build docker container
~~~~.bash
docker pull greole/owls
~~~~

# Dependencies
It is recommended to have matplotlib installed, which itself depends on libpng and freetype.
The simplest way is to just use your distros package manager to install matplotlib.

# Introduction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {.python .numberLines}
import Owls as ow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## Reading Foam Data
Owls provides convenient methods to import OpenFOAM data and experimental data i.e.

~~~~.python
s1 = read_sets(
    folder='/some/path/',
    name='foo', # name of the case
    )
~~~~
where folder is the root folder of your OpenFOAM case. Additionally available `read_eul`, `read_lag`, and `read_exp`, `read_log`

## Accessing Data
Owls is build on Pandas and you can use the standard features of Pandas like bracket notation to access the data

~~~~.python
s1['T'] # access full Temperature row
s1.latest['T'] # access latest temperature row
# access latest temperature data
# at 'y0.1' location
# corresponds to sets/TIME/y0.1_T.xy
s1.latest.location('y0.1')
~~~~

## Filtering Data
Data can be filtered using user defined function
~~~~.python
s1.filter_locations(ow.isIn('axis')) # filter all location with axis in the name
s1.filter_fields("T", 1000, 2000) # return all fields where temperature is between 1000 and 2000
s1.latest.filter(name="Pos", func=lambda x: 0.1<x<0.2)
~~~~


## Grouping Data
Data can be grouped to generate multiple plots at once

~~~~.python
s1.by_index('Loc') # group into locations
s1.by_location() # group into locations
s1.by_time() # group by times
~~~~

## Data Visualisation
Data can be passed to any standard python plotting library i.e. matplotlib, ggplot, seaborn.
Currently bokeh is choosen to generate on the fly data visualisations.

If .show is called the natural representation of the FoamFrame will be choosen, i.e. line plots for sets and scatter experimental data. To make standard calls concise the default value of x='Pos'.
~~~~.python
s1.by_location().show(y=['v','u'], overlay="Field") # plot u and v for each location
s1.by_location().show(y=['v','u'], overlay="Group") # plot u and v for each location
~~~~

you can pass bokeh arguments through the plot function for styling
~~~~.python
s1.by_index('Loc').show(y='v', y_label='foo')
s1.by_index('Loc').scatter(x='u',y='v',legend='bar')
~~~~
