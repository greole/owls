# Owls

![](https://badge.fury.io/py/owls.svg)
![](https://badge.fury.io/gh/greole%2Fowls.svg)
![](https://travis-ci.org/greole/owls.svg?branch=master)

The Owls package is a collection of python tools for data analysis and 
plotting of OpenFOAM cases. It provides the following basic functionality: 

- A reader for OpenFOAM scalar and vector fields, set files and log files
- Converting OpenFOAM data to FoamFrames which are derived DataFrames from the pandas library

This tutorial aims to illustrate the basic workflow of the Owls package.
After installing, make sure that the module following imports are available

# Installation

~~~~.bash
python setup.py install --user
pip install Owls # or for non development version
                 # but probably out of date   
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
where folder is the root folder of your OpenFOAM case. Additionally available read_eul, read_lag, and read_exp, read_log

## Accessing Data
Since Owls is build on Pandas you can use the standard features of Pandas like bracket notation to access the data

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
s1.latest.filter(name="T", field=lambda x: 291<x<291.5)
s1.latest.filter(name="Pos", field=lambda x: 0.1<x<0.2)
~~~~


## Grouping Data
Data can be grouped/facetted to generated plot matrizes or overlayed plots

~~~~.python
s1.by_index('Loc')
s1.by(name='Loc', index=lambda x: x))
~~~~

### Automatic renaming of sets and exp data
Owls tries to give meaningfull names to set and exp data. 
OpenFoam sets files are assumed to following the naming convetion
yw*setname_field1_field2.xy* this referes to a file containing 3 fields
position, field1 and field2 these fields will be accessible by the name 
defined by the file name. Vector fields like U will be replace by u, v, w etc.
If the field names cannot be determined by the file name the fields will have
the following naming convetion *setname_field1_field2.xy_0 ,.. *setname_field1_field2.xy_2

## Data Visualisation
Data can be passed to any standard python plotting library i.e. matplotlib, ggplot, seaborn.
Currently bokeh is choosen to generate on the fly data visualisations.

If .show is called the natural representation of the FoamFrame will be choosen, i.e. line plots for sets and scatter experimental data. To make standard calls concise the default value of x='Pos'.
~~~~.python
s1.by_index('Loc').show(y='v') 
s1.by_index('Loc').scatter(x='u',y='v') 
~~~~

you can pass bokeh arguments through the plot function for styling
~~~~.python
s1.by_index('Loc').show(y='v', y_label='foo') 
s1.by_index('Loc').scatter(x='u',y='v',legend='bar') 
~~~~

## Further Information
you will find an example Owls demo notebook for ipython in the examples folder.


##Contribution

Yes please!
