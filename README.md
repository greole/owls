# Owls
The Owls package is a collection of python tools for data analysis and 
plotting of OpenFOAM cases. It provides the following basic functunality: 

- A reader for OpenFOAM scalar and vector fields, set files and log files
- Converting OpenFOAM data to FoamFrames which are derived DataFrames from the pandas library

This tutorial aims to illustrate the basic workflow of the Owls package.
After installing, make sure that the module following imports are availible

# Installation
~~~~.bash
python setup.py install # or
pip install Owls # for non development version
~~~~

# Introduction

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {.python .numberLines}
import Owls # or
import Owls as ow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Basic documentation is provided through Pythons docstrings and can be called by:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {.python .numberLines}
help(Owls)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## Reading Foam Data

~~~~.python
s1 = read_sets(
    folder='/some/path/', 
    name='foo', # name of the case 
    plot_properties=PlotProperties() # an object to store plotting info
    )
~~~~

also availible read_eul, read_lag, and read_exp, read_log

## Accessing Data
~~~~.python
s1['T'] # access full Temperature row
s1.latest['T'] # access latest temperature row
# access latest temperature data
# at 'y0.1' location
# corresponds to sets/1000/y0.1_T.xy
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
