#!/usr/bin/ipython
'''
Reads and converts OpenFoam logfiles and data
to Pandas DataFrames and Series


Bad Karma:
    * read_data_file returns field names which is redundant to data.columns


'''

import numpy as np
import re
import os
from pandas import *
from collections import defaultdict
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
    """
    search_folder = (subfolder if not subfolder.startswith('./{}') else "./{}/")
    try:
        times = (fold if fold else find_times(search_folder.format("")))
        return {time: _get_datafiles_from_dir(subfolder.format(time), filelist)
                for time in times}
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
        return [search_dir + f for f in files if f in fn_filter] 
    else:
        return [search_dir + f for f in files if not f.startswith('.')] 

def is_time(time):
    try:
        return float(time)
    except:
        return "False"

def find_times(fold=None):
    """ Find time folders in given or current folder
        Returns list of times as strings
    """
    search_folder = (fold if fold else os.getcwd())
    cur_dir = os.walk(search_folder)
    root, dirs, files = next(cur_dir)
    return [time for time in dirs if is_time(time) != "False"]

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

def foam_to_DataFrame(search_format, file_names,
                      skiplines=1, maxlines=0,
                      plot_props=None):
    """ returns a Dataframe for every file in fileList """
    fileList = find_datafiles(subfolder=search_format, filelist=file_names)
    origins = dict() 
    if not fileList:
        print "no files found"
        return origins, [] 
    samples = defaultdict(int)
    oldperc = 0.10
    file_count = 0 
    n_files_tot = 0
    n_files_tot = sum([len(l) for l in fileList.itervalues()])
    for time,files in fileList.iteritems():
            df = DataFrame()
            for fn in files:
                file_count +=1
                perc = float(file_count)/float(n_files_tot)
                if perc > oldperc:
                    print "#",
                    oldperc += 0.1
                ret = read_data_file(fn, skiplines, maxlines, plot_props)
                if not ret:
                    continue
                columns, x = ret
                origin = {(key,time): fn for key in columns} 
                origins.update(origin)
                df = df.combine_first(x)
            samples[time] = df
    print "[done]"
    return origins, samples


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

def read_data_file(fn, skiplines=1, maxlines=False, plot_props={}):
    '''
    A function to read any foam data files returning data and 
    index after header
    '''

    # print "opening file {}".format(fn)
    try:
        if not os.path.exists(fn):
            print "Can not open file " + fn
            return None
        with open(fn) as f:
            field = fn.split('/')[-1]
            content = f.readlines()
            content.append('bla')
            start, num_entries = if_header_skip(content)
            entries = len(content[start].split())
            is_a_vector = (True if entries > 1 else False)
            line_numbers = range(0, num_entries, skiplines)   # unused atm
            end = start + num_entries
            label = plot_props.get('label', 'no label')
            
            if is_a_vector:
                data = map(subst_split, content[start:end:skiplines])
                names = evaluate_names(fn, entries)
                df = DataFrame(data=data, columns=names) 
                return names, df.astype(float)
            else:
                data = [np.float32(x) for x in content[start:end:skiplines]]
                entries = 1
                df = DataFrame(data=data, columns=[field])
                return field, df
    except Exception as e:
        print "Error processing datafile " + fn
        print e
        return None

def evaluate_names(fullfilename, num_entries):
    """  """
    filename = fullfilename.split('/')[-1]
    name = (filename.replace('.dat','')
            .replace('.xy','')
            .replace('UMean','uMean_vMean_wMean')
            .replace('UPrime2Mean','uu_uv_uw_vv_vw_ww')
            .replace('Uc','uc_vc_wc')
            .replace('U','u_v_w')
           )
    fields = name.split('_')
    if num_entries == len(fields):
        if '.dat' in filename or '.xy' in filename:
            pos = fields[0]
            fields = [pos + '_' + val for val in fields[1:]]
            fields.insert(0, pos)
        return fields
    else:
        basename = filename.split('/')[-1]
        return [basename + '_' + str(i) for i in range(num_entries)]

def subst_split(entry):
    entry = re.sub(r'[()]', '', entry)
    return entry.split()

def req_file(file_name, requested):
    """ True if file name is list of requested files """
    if requested == True:
        return requested
    else:
        return file_name.split('/')[-1] in requested

def key_lines(lines, keys):
    for line in lines:
        if "Time = " in line and not "s" in line:
            yield 'time', line
        for key, key_w in keys.iteritems():
            if key_w in line:
                yield key, line


def find_start_of_log(log):
    for i, line in enumerate(log):
        if "Time = " in line and not "s" in line:
            return i


def extractFromLog(keys, path, logString):
    '''
        A function using grep to search for a string (ss) in a logfile

        Using regexep to extract only numbers
        converts to  floats and returns the data
    '''
    logs = get_ipython().getoutput("ls {0}{1}".format(path, logString))
    logInd = []
    old_it = 0
    df0 = DataFrame()
    for log_number, log_name in enumerate(logs):
        dataDict = defaultdict(list)
        try:
            with open(log_name) as log:
                f = log.readlines()
                start = find_start_of_log(f)
                for key, line in key_lines(f[start:-1], keys):
                    readAndCleanLinesDict(line, dataDict, key)
            print "finished log file {} of {} ".format(log_number+1, len(logs))

            for key, value in dataDict.iteritems():
                cur_it = old_it + len(value)
                dataDict[key] = Series(value, index=range(old_it, cur_it))

            df = DataFrame(dataDict)
            df['log'] = log_number
            df2 = DataFrame(df.describe())
            inner = int(max(df2.ix['count']))
            tot = inner + old_it
            logInd = logInd + [log_number] * inner
            df0 = df0.combine_first(df)
            old_it = tot
        except:
            pass
    return df0


def readAndCleanLinesDict(line, dic, key):
    ''' Takes a string splits it and converts it to a number '''
    conv = []
    line = line.replace(',', '')             # move to caller
    for i, elem in enumerate(line.split()):
        try:
            conv.append(np.float32(elem))
        except:
            pass
    for i, elem in enumerate(conv):
        dic[key + str(i)].append(elem)


def begins_with_int(line):
    try:
        num = int(line)
        return num
    except:
        return False


def if_header_skip(content):
    first_line = content[0]
    if not first_line.startswith('#') and not first_line.startswith('/*'):
        return 0, -1
    elif first_line.startswith('#'):
        return 1, -2 #FIXME dont append bla
    elif first_line.startswith('/*'):
        for line_number, line in enumerate(content):
            entries = begins_with_int(line)
            if entries or line_number >= 100:
                return line_number + 2, entries
