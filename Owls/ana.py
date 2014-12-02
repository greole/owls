#!/usr/bin/python
"""
    Usage: 
        ana.py case2case [--avg] [--div] --times=<times> --vectors=<fields> --scalars=<fields> --tensors=<field> --case=<dir>
"""

from io import *
import os
from docopt import docopt
from pandas import *

def file_names(arguments):
    """ construct file names for read in from cli args """
    for ftype in ['vector', 'scalar', 'tensor']:
        fargs = '--' + ftype + 's'
        if not arguments[fargs]:
            continue
        cwd, fields, times = os.getcwd(), arguments[fargs], arguments['--times']
        fields = fields.split(',')
        for fname in fields:
            this = "{}/{}/{}".format(cwd, times, fname)
            if arguments['--case']:
                that = "{}/{}/{}/{}".format(cwd, arguments['--case'], times, fname)
            else:
                that = None
            ftype = ftype.replace('tensor','symTensor')
            yield ftype, fname, times, this, that

if __name__ == '__main__':
    arguments = docopt(__doc__)
    for ftype, fname, times, ours, theirs in file_names(arguments):
        origins_this, this = read_data_file(ours, 1, 0, {})
        origins_that, that = read_data_file(theirs, 1, 0, {})
        boundaries = read_boundary_names("{}/{}/{}".format(os.getcwd(), times, fname))
        diff, avg = this-that, 0.5*(this+that)
        for name, result in {fname+'diff': diff, fname+'avg': avg}.iteritems():
            fullname = "{}/{}/{}".format(os.getcwd(), times, name)
            dataframe_to_foam(fullname, ftype, result, boundaries)
