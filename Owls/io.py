#!/usr/bin/ipython
'''
Reads and converts OpenFoam logfiles and data
to Pandas DataFrames and Series


Bad Karma:
    * read_data_file returns field names which is redundant to data.columns
    * rename to FoamAna.io

'''

import numpy as np
import re
import os
from pandas import *
from collections import defaultdict
from collections import OrderedDict
from IPython.display import display, clear_output
from case import *
from plot import *

FOAM_HEADER = """
/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  2.0.x                                 |
|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |
|    \\/     M anipulation  |                                                 |
\\*---------------------------------------------------------------------------*/
FoamFile
{{
    version     2.0;
    format      ascii;
    class       vol{}Field;
    location    {};
    object      {};
}}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 0 0 0 0 0 0];

internalField   nonuniform List<{}>
"""

DEBUG = True

####################### helper functions ################################
def match(d, event):
    """ returns d.item if reg_exp_key matches event """
    for reg_exp_key in d.keys():
        if re.match(reg_exp_key, event):
            return d[reg_exp_key]

def find_datafiles(
        fold=False,
        filelist=False,
        subfolder="{}",
    ):
    """ Find all datafiles in each time folder,
        
        Returns a dictionary of lists containing data 
        files for every found time step
        
        Subfolders: specify wheter to search in cwd or in a specific subfolder
                    accepting a search pattern
    """
    search_folder = (subfolder if not subfolder.startswith('./{}') else "./{}/")
    try:
        times = (fold if fold else find_times(search_folder.format("")))
        od = OrderedDict()
        return  OrderedDict(
            [(time, _get_datafiles_from_dir(subfolder.format(time), filelist)) #FIXME use ordered dict here
                for time in times]
            )
    except:
        return dict()

def _get_datafiles_from_dir(path=False, fn_filter=False):
    """ Return file names of Foam files from cwd if no path 
        is specified explicitly. 
        If no filter list is given the complete list of files will be returned 
        else only files matching that list
    """
    search_dir = (path if path else os.getcwd() + "/")
    cur_dir = os.walk(search_dir)
    root, dirs, files = next(cur_dir)
    if fn_filter:
        l = [search_dir + f for f in files if f in fn_filter]
    else:
        l = [search_dir + f for f in files if not f.startswith('.')]
    l.sort()
    return l

def is_time(time):
    try:
        return float(time)
    except:
        return False

def find_times(fold=None):
    """ Find time folders in given or current folder
        Returns sorted list of times as strings
    """
    search_folder = (fold if fold else os.getcwd())
    cur_dir = os.walk(search_folder)
    root, dirs, files = next(cur_dir)
    times = [time for time in dirs if is_time(time) is not False]
    times.sort()
    return times

def dataframe_to_foam(fullname, ftype, dataframe, boundaries):
    """ writes an OpenFOAM field file from given dataframe """
    with open(fullname, 'w') as f:
        fname = fullname.split('/')[-1]
        time = fullname.split('/')[-2]
        print "writing %s : %s" % (time, fname)
        f.write(FOAM_HEADER.format(ftype.capitalize(), time, fname, ftype))
        f.write(str(len(dataframe)))
        f.write("\n(\n")
        out=""
        for count, row in dataframe.iterrows():
            if len(row) == 1:
                out = "{}\n".format(row[0])
            elif len(row) == 3:
                out = "({} {} {})\n".format(row[0], row[1], row[2])
            elif len(row) == 6:
                out = "({} {} {} {} {} {})\n".format(row[0], row[1], row[2], row[3], row[4], row[5])
            f.write(out)
        f.write(");\n")
        f.write("boundaryField {\n")
        for bound in boundaries:
            f.write(bound)
            f.write("\t{type zeroGradient;}\n")
        f.write("}")
        f.write("\n// ************************************************************************* //")

class ProgressBar():

    def __init__(self, n_tot, bins=10):
        #FEATURE: Add timings 
        self.tot = float(n_tot)
        self.count = 0.0
        self.cur = 0.0

    def next(self):
        self.count += 1.0 
        if self.count/self.tot > self.cur:
            print "#",
            self.cur += 0.1

    def done(self):
        print "[done]"

def import_foam_folder(
            search_format,
            file_names,
            skiplines=1,
            maxlines=0,
        ):
    """ returns a Dataframe for every file in fileList """
    #import StringIO
    from pandas import concat
           
    fileList = find_datafiles(subfolder=search_format, filelist=file_names)
    if not fileList:
        print "no files found"
        return 
    p_bar = ProgressBar(n_tot=sum([len(l) for l in fileList.itervalues()]))
    df = DataFrame()
    #df.index = MultiIndex.from_tuples(zip([],[]),names=['Loc',0])
    origins = dict() 
    for time, files in fileList.iteritems(): #FIXME dont iterate twice
        df_tmp = DataFrame()
        for fn in files:
            #ret = read_table(StringIO.StringIO(foam_to_csv(fn)))
            ret = read_data_file(fn, skiplines, maxlines)
            p_bar.next()
            if not ret:
                continue
            field_names, x = ret
            origin = {(key, time): fn for key in field_names} #FIXME use nested dicts 
            origins.update(origin)
            if df_tmp.empty:
                df_tmp = x
            else: 
                try:
                    # use combine first for all df at existing Loc or
                    # if not Loc is specified (Eul or Lag fields)
                    if x.index.levels[0][0] in df_tmp.index.levels[0]:
                        df_tmp = df_tmp.combine_first(x)
                        #df_tmp = concat([df_tmp, x], axis=1)
                        pass
                    else:
                        df_tmp = concat([df_tmp, x])
                except Exception as e:
                    print x
                    print e
        df_tmp['Time'] = float(time)
        if df.empty:
            df = df_tmp
        else:
            df = df.append(df_tmp)
    df.set_index('Time', append=True, inplace=True)
    df = df.reorder_levels(['Time','Loc','Id'])
    p_bar.done()
    return origins, df,

"""
Time Loc        Pos U V
1000 radVel+10  0.1 
                0.2
     radVel+20  0.1
                0.2
"""


def foam_to_csv(fn, ):
    """ helper function for d3.js data conversion 
        prints data directly to std:out
    """
    import re
    try: 
        with open(fn) as f:
            content = f.readlines()
            start, num_entries = if_header_skip(content)
            entries = len(content[start].split())
            for l in content:
                print re.sub("\t",",",re.sub("[\(\)\\n]","",l))
    except Exception as e:
        print e

def read_boundary_names(fn):
    """ Todo use iterator method to avoid reading complete file """
    with open(fn) as f:
        boundary_names = []
        lines  = reversed(f.readlines())
        for line in lines:
            if "{" in line:
                follower = next(lines)
                if "boundaryField" in follower:
                    return boundary_names
                try:
                     boundary_names.append(follower)
                except:
                    pass
            else:
                pass

def read_data_file(fn, skiplines=1, maxlines=False):
    """  A function to read any foam data files returning data and 
         index after header
    """

    # print "opening file {}".format(fn)
    if not os.path.exists(fn):
        print "Can not open file " + fn
        return None
    try:
        with open(fn) as f:
            field = fn.split('/')[-1]
            content = f.readlines()
            content.append('bla')
            start, num_entries = if_header_skip(content)
            entries = len(content[start].split())
            is_a_vector = (True if entries > 1 else False)
            end = start + num_entries
            if is_a_vector:
                data = map(lambda x: re.sub(r'[()]', '', x).split(),
                            content[start:end:skiplines])
                loc, names = evaluate_names(fn, entries)
                df = DataFrame(data=data, columns=names)
                if loc:
                    df['Loc'] = loc
                else: 
                    df['Loc'] = range(len(df))
                df.set_index('Loc', append=True, inplace=True)
                df.index.names=['Id','Loc']
                df = df.reorder_levels(['Loc','Id'])
                return names, df.astype(float)
            else:
                data = [np.float32(x) for x in content[start:end:skiplines]]
                entries = 1
                df = DataFrame(data=data, columns=[field])
                df['Loc'] = "Field"
                df.set_index('Loc', append=True, inplace=True)
                df.index.names=['Id','Loc'] 
                df = df.reorder_levels(['Loc','Id'])
                return field, df
    except Exception as e:
        if DEBUG:
            print "Error processing datafile " + fn
            print e
        return None

def evaluate_names(fullfilename, num_entries):
    """ Infere field names and Loc from given filename 

        Example: 
            U -> Field, [u,v,w]
            centreLine_U.xy -> centreLine, [Pos,u,v,w]
    """
    filename = fullfilename.split('/')[-1]
    name = (filename.replace('.dat','') #FIXME use regex here
            .replace('.xy','')
            .replace('UMean','uMean_vMean_wMean')
            .replace('UPrime2Mean','uu_uv_uw_vv_vw_ww')
            .replace('Uc','uc_vc_wc')
            .replace('U','u_v_w')
           )
    fields = name.split('_')
    if num_entries == len(fields):
        pos = "Field"
        if '.dat' in filename or '.xy' in filename:
            pos = fields[0]
            fields[0] = "Pos"
        return pos, fields
    else:
        return "Unknown", [filename + '_' + str(i) for i in range(num_entries)]


def req_file(file_name, requested):
    """ True if file name is list of requested files """
    if requested == True:
        return requested
    else:
        return file_name.split('/')[-1] in requested


def import_logs(folder, keys):
    """
        keys = {"ExectionTime": ["ExecTime", "ClockTime"]}
        
        return a DataFrame 
    
              Loc, Time KeyName1 Keyname2
                1   0.1  
                    
                    0.2
                2

    
    """
    def find_start(log):
        """ Fast forward through file till 'Starting time loop' """
        for i, line in enumerate(log):
            if "Starting time loop" in line:
                return i


    def extract(line, keys):
        """ 
            returns key and values as list
                "ExecutionTime":[0,1]
        """
        import re
        for key, col_names in keys.iteritems():
            if re.search(key, line): 
                return col_names, map(float,filter(lambda x: 
                        x, re.findall("[0-9]+[.]?[0-9]*[e]?[\-]?[0-9]*", line)))
        return None, None

    fold,dirs,files = next(os.walk(folder))
    logs = [fold + "/" + log for log in files if 'log' in log]
    p_bar = ProgressBar(n_tot = len(logs))
    # Lets make sure that we find Timesteps in the log
    keys.update({"^Time = ": ['Time']}) 

    for log_number, log_name in enumerate(logs):
        with open(log_name) as log:
            f = log.readlines()
            start = find_start(f)
            dataDict = defaultdict(list)
            df=DataFrame()
            for line in f[start:-1]:
                 col_names, values = extract(line, keys)
                 if not col_names:
                    continue
                 if col_names[0] == 'Time':
                    # a new time step has begun
                    # flush datadict and concat to df
                    # Very slow but, so far the solution
                    # to keep subiterations attached to correct time 
                    # FIXME: still needs handling of different length dictionaries
                    df = concat([df,DataFrame(dataDict)])
                    dataDict = defaultdict(list)
                 for i, col in enumerate(col_names):
                    dataDict[col].append(values[i])
        p_bar.next()
        try:
            df.index=range(len(df))
            df.index.names=['Id']
            df['Loc'] = log_number
            df.set_index('Time', append=True, inplace=True)
            df.set_index('Loc', append=True, inplace=True)
            df = df.reorder_levels(['Loc','Time','Id'])
            p_bar.done()
        except Exception as e:
            print log_name
            print "failed to process"
            print e
            return None
    return {},df



def if_header_skip(content):
    """ go through first lines of file and check if has header
        return start of content and total lines
    """
    def begins_with_int(line):
        try:
            num = int(line)
            return num
        except:
            return False
    first_line = content[0]
    if not first_line.startswith('#') and not first_line.startswith('/*'):
        return 0, -1
    elif first_line.startswith('#'):
        for line_number, line in enumerate(content):
            if not line.startswith('#'):
                return line_number, -line_number-1 #FIXME dont append bla
    elif first_line.startswith('/*'):
        for line_number, line in enumerate(content):
            entries = begins_with_int(line)
            if entries or line_number >= 100:
                return line_number + 2, entries