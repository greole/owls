#!/usr/bin/ipython
'''
    Reads and converts OpenFoam logfiles and data
    to Pandas DataFrames and Series
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

def items_in_times(
        fold=False,
        file_names=False,
        search_format='{}',
        ):
    """ find all files in time sub folders """
    results = []
    old_path = os.getcwd()
    time_fold = (fold if fold else find_times(search_format))
    for time in time_fold:
        time_path = search_format.format(time + '/')
        os.chdir(time_path)
        fn_found = items_in_time(file_names)
        files = [fn.replace('./', time_path) for fn in fn_found]
        entry = (time, files)
        results.append(entry)
        os.chdir(old_path)
    return results

def items_in_time(fn_filter):
    """ data files in current path if filenames are in filter list """
    cmd = "find . -maxdepth 1 -type f \( ! -iname '.*' \)"
    fn_found = get_ipython().getoutput(cmd)
    if fn_filter:
        return filter(lambda fn: req_file(fn, fn_filter), fn_found)
    else:
        return fn_found 

def find_times(fold=None):
    if fold:
        fold = fold.split('{}')[0]
    cmd = "ls -t {} | grep ^[0-9]\*[0-9]".format(fold)
    times = get_ipython().getoutput(cmd)
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
    fileList = items_in_times(search_format=search_format, file_names=file_names)
    samples = defaultdict(int)
    oldperc = 0.10
    file_count = 0 
    n_files_tot = 0
    origins = dict() 
    for files in fileList:
        n_files_tot += len(files[1])
    for time, files in enumerate(fileList):
            df = DataFrame()
            for fn in files[1]:
                file_count +=1
                perc = float(file_count)/float(n_files_tot)
                if perc > oldperc:
                    print "#",
                    oldperc += 0.1
                columns,x = read_data_file(fn, skiplines, maxlines, plot_props)
                origin = { (key,files[0]): fn for key in columns} 
                origins.update(origin)
                df = df.combine_first(x)
            samples[files[0]] = df
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

def read_data_file(fn, skiplines, maxlines, plot_props):
    '''
        A function to read any foam data files
        returning data and index after header
    '''
    # print "opening file {}".format(fn)
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
            names = evaluate_names(field)
            if len(names) == entries:
                df = DataFrame(data=data, columns=names) 
            else:
                names = [ fn + '_' + str(i) for i in range(entries)]
                df = DataFrame(data=data, columns=names) 
            return names, df.astype(float)
        else:
            data = [np.float32(x) for x in content[start:end:skiplines]]
            entries = 1
            df = DataFrame(data=data, columns=[field])
            return field, df

def evaluate_names(name):
    if '.dat' in name:
        name = name.replace('.dat','')
    else:
        name = name.replace('.xy','')
        name = name.replace('UMean','uMean_vMean_wMean')
        name = name.replace('UPrime2Mean','uu_uv_uw_vv_vw_ww')
        name = name.replace('Uc','uc_vc_wc')
        name = name.replace('U','u_v_w')
        name = name.replace('positons','x_y_z_cell')
        name = name.replace('points','x_y_z')
    fields = name.split('_')
    pos = fields[0]
    fields = [pos + '_' + val for val in fields[1:]]
    fields.insert(0, pos) 
    return fields

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
    if '#' in first_line:
        return 1,-2
    if '/*-' in first_line:
        for line_number, line in enumerate(content):
            entries = begins_with_int(line)
            if entries or line_number >= 100:
                return line_number + 2, entries
    else:
        return 0, -1
