# FoamAna
The FoamAnaL package is a collection of python tools for data analysis and 
plotting of OpenFOAM cases. It provides the following basic functunality: 

- A reader for OpenFOAM scalar and vector fields, set files and log files
- Converting OpenFOAM data to pandas DataFrame
- A matplotlib wrapper for plotting with consistent axis labels

This tutorial aims to illustrate the basic workflow of the FoamAnaL package.
After installing, make sure that the module following imports are availible

# Installation
~~~~.bash
python setup.py install
python setup.py install -f
~~~~

# Introduction

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {.python .numberLines}
from FoamAna.case import *
from FoamAna.analysis import *
from FoamAna.plot import *
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Basic documentation is provided through Pythons docstrings and can be called by:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {.python .numberLines}
help(FoamAna.case)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## Reading Foam Data

The simplest way to read data is to use the provided read methods. To read data
OpenFOAM case root folder needs to be specified, and a plot_properties dict should 
be passed. A plot_properties dictionary holds the field name as key and a tuple of
the label for the plot axis and the data range for plotting as values. The field names
can be specified with regular expressions to match similar fields, which is usefull
for sets data. Examples:

- 'centerLine*' will match centerLine but not centerLine_u
- 'P[0-9]*_u$' will match P023_u but not P023_uMean


~~~~.python
sets_props = {
       'fileRegExp': ["label for axis", "plotting range"],
       '*$': ["axis label", [0,1]],
}

set = read_sets(folder, sets_props, name) # read_exp, read_eul, read_lag, read_log
~~~~

## Accessing Data
Once the data has been read it can be accessed using the *.data* attribute.  The
data is structured by *[data_type][time][field_name]*. Additionally the .field_tpye
attribute is a shortcut to latest timestep of a given field

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {.python .numberLines}
U = LAG.data['lag']['0']['U'] # returns the lagrangian U at 0s 
U = LAG.lag['U'] # returns the lagrangian U at latest time 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Case object also provides a generator function ```sets()``` to iterate over
all sets entries which is useful for plotting convergence checks


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {.python .numberLines}
for time, set_ in cases[case_name].sets():
    print set_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

### Automatic renaming of sets and exp data
FoamAnaL tries to give meaningfull names to set and exp data. 
OpenFoam sets files are assumed to following the naming convetion
yw*setname_field1_field2.xy* this referes to a file containing 3 fields
position, field1 and field2 these fields will be accessible by the name 
defined by the file name. Vector fields like U will be replace by u, v, w etc.
If the field names cannot be determined by the file name the fields will have
the following naming convetion *setname_field1_field2.xy_0 ,.. *setname_field1_field2.xy_2


## Data Visualisation
For data visualistion a matplotlib wrapper is provided. Plots are created by 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {.python .numberLines}
p = Plot([geom=[2,2], style='matrix') # creates a 2x2 plot matrix
p.add (x=LAG.lag['pos'], y=LAG.lag['T'], subplot=0) # inserts a plot at position 0
p.show()    # draws the plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

example for multiple radial plots for jet cases

~~~~.python
pos = ['-10', '+0','+25', '+50', '+85'] # 
symb = ['-', '-.' ,'--',':','-','-.','--'] # symbol examples
p=Plot(geom=[1, len(pos)], style='wide', leg=[0]) # create a wide multiplot with  5 sub plots
for n, x in enumerate(reversed(pos)):
    i=0
    # EXPERIMENTAL DATA
    POS = EXP.exp['TX{}'.format(x)] # access positons series
    T = EXP.exp['TX{}_T'.format(x)] # access temperature series
    p.add(x=POS, y=T, subplot=n, symbol='o' ) # add data to plot at subplot n, give it an 'o' symbol 
    # CFD DATA
    for name, case in cases.iteritems(): # go through all cases in cases dictionary
        POS = case.set['X{}'.format(x)]
        T = case.set['X{}_TMean'.format(x)]
        p.add(x=POS, y=T, plot_type='Plot', subplot=n, symbol=symb[i])
        i+=1
p.show()
~~~~

The following plot style templates are availible:
- 'jet'
- 'matrix'
- 'dcol'
- 'classic' (default)

Consitent plot range are generally useful, but sometimes the ranges of a certain 
plot has to be modified. The plot object provides a zoom method to change thje data
ranges of a subplot

~~~~.python$
p.zoom(subplot=1, y=[0,10])
~~~~ 
