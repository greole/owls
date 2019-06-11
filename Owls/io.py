'''
Reads and converts OpenFoam logfiles and data
to Pandas DataFrames and Series


Bad Karma:
    * read_data_file returns field names which is redundant to data.columns
    * rename to FoamAna.io

'''
from __future__  import print_function
from future.builtins import map, filter, open, next, range, zip, dict, str

import numpy as np
import re
import os
import hashlib
from pandas import DataFrame, concat
from collections import defaultdict, OrderedDict
from IPython.display import display, clear_output
import multiprocessing

FPNUMBER = "[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?"

HASH_RESULTS = False # saves approx 30%
MULTIPROCESS = 0

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
        path=False,
        files=False,
        search=FPNUMBER,
        exclude=None,
        times_slice=None,
    ):
    """ Find all datafiles in each time folder,

        Returns a dictionary of lists containing data
        files for every found time step

        fold: list of time folders to look for data files
              if False time folders in cwd will be taken
        filelist: A list of file names which are accepted,
                  if false all files will be returned
        subfolder: specify wheter to search in cwd or in a specific subfolder
                   accepting a search pattern
        Returns:
            Ordered dict with times as key and
            list of found files
    """
    data_folders = find_datafolders(search, path, exclude, times_slice)
    return OrderedDict(
        [(time, _get_datafiles_from_dir(time, files))
            for time in data_folders]
        )


def find_datafolders(regex, path=False, exclude=None, slice_=None):
    """ Find data folders according to regex
        replaces old find_times function
        Returns sorted list of times as strings """
    path = (path if path else os.getcwd())
    if not path.endswith('/'):
        path = path + '/'
    complete_regex = path + regex + "$"
    folders = []
    for fold, dirs, _ in os.walk(path):
        if exclude:
            dirs[:] = [d for d in dirs for ex in exclude if not re.match(ex, d)]
        folders.append(fold)

    folders = [_ for _ in folders if re.match(complete_regex, _)]
    folders.sort()

    # TODO This legacy slicing should be removed
    # and replaced by folders[slice_]
    # if slice_ == "all":
    #     return folders
    if slice_ == "latest":
        return folders[-1]
    else:
        return folders

    # FIXME raise Exception
    # return (folders if not slice_ else folders(slice_))


def _get_datafiles_from_dir(path=False, fn_filter=False):
    """ Return file names of Foam files from cwd if no path
        is specified explicitly.
        If no filter list is given the complete list of files will be returned
        else only files matching that list
    """
    path = (path if path else os.getcwd() + "/")
    path = (path + "/" if not path.endswith("/") else path)
    cur_dir = os.walk(path)
    root, dirs, files = next(cur_dir)
    if fn_filter:
        l = [path + f for f in files if f in fn_filter]
    else:
        l = [path + f for f in files if not f.startswith('.')]
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
    with open(fullname, 'w', encoding='utf-8') as f:
        fname = fullname.split('/')[-1]
        time = fullname.split('/')[-2]
        print("writing %s : %s" % (time, fname))
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

class Origins():
    """ Class to manage fields to file relation and store hashes

        dct = {'hash':34jd
               0.0:{'hash':234s                     #time
                    'centreline':{'hash':94143e     #loc
                                  'U':filename,3424}
                    }
              }
    """
    def __init__(self):
       self.dct = defaultdict(dict)

    @classmethod
    def from_dict(cls, dct):
        pass

    def to_dict(self):
        pass

    def insert(self, time, loc, field, filename, fieldhash):
        try:
            self.dct[time][loc][field] = filename, fieldhash
        except:
            self.dct[time].update({loc:{field: (filename, fieldhash)}})

    def update_hashes(self):
        for time_key, time in self.dct.iteritems():
            if time_key == "hash":
                continue
            for loc_key, loc in time.iteritems():
                if loc_key == "hash":
                    continue
                self.dct[time_key][loc_key]["hash"] = sum(
                    [field[1] for key,field in loc.iteritems() if key != "hash"]
                )
            self.dct[time_key]["hash"] = sum(
                    [field["hash"] for key,field in time.iteritems() if key != "hash"]
            )
        self.dct["hash"] = sum([field["hash"] for key,field in self.dct.iteritems()
                                    if key != "hash"]
        )

    def hashes(self):
        """ generator """
        # self.update_hashes()
        for time_key, time in self.dct.iteritems():
            if time_key == "hash":
                continue
            for loc_key, loc in time.iteritems():
                if loc_key == "hash":
                    continue
                for field, item in loc.iteritems():
                    if field == "hash":
                        continue
                    fn, field_hash = item
                    yield ((time_key, self.dct["hash"]),
                           (loc_key,  time["hash"]),
                           (field, loc["hash"]),
                           (fn, field_hash)
                          )

    def find(self, search_hash):
        for time, loc, field, item in self.hashes():
            time_name, time_hash   = time
            loc_name, loc_hash     = loc
            field_name, field_hash = field
            filename, item_hash    = item
            if (search_hash == item_hash):
                return field_name, filename
        else:
            return None,None

class ProgressBar():
    """ A class providing progress bars """

    def __init__(self, n_tot, bins=10):
        #FEATURE: Add timings
        self.tot = float(n_tot)
        self.count = 0.0
        self.cur = 0.0

    def next(self):
        self.count += 1.0
        if self.count/self.tot > self.cur:
            print("#", end="")
            self.cur += 0.1

    def done(self):
        print("[done]")

def strip_time(path, base):
    """ try to extract time from path """
    wo_base = path.replace(base, '')
    wo_proc = re.sub('processor[0-9]?', '', wo_base)
    match = re.search(FPNUMBER, wo_proc)
    if match:
        time = float(match.group())
        return time
    else:
        return 0.0

def import_foam_mesh(path, exclude=None, times_slice=None):
    """ returns a Dataframe containing the raw mesh data """
    mesh_loc = "constant/polyMesh"
    if mesh_loc not in path:
        path = os.path.join(path, mesh_loc)

    fileList = find_datafiles(
            path,
            search="[.\/A-Za-z]*",
            files=['faces', 'points', 'owner', 'neighbour'],
            exclude=exclude,
            times_slice=times_slice,
        )
    if not fileList:
        print("no mesh files found")
        return
    p_bar = ProgressBar(n_tot=sum([len(l) for l in fileList.values()]))
    df = DataFrame()
    from collections import defaultdict
    origins = Origins()
    els = list(fileList.items())
    time, files = els[0]
    df_tmp = dict()
    for fn in files:
        ret = read_data_file(fn, skiplines=1, maxlines=False)
        p_bar.next()
        field_names, x, hashes = ret
        df_tmp[fn] = x
    return df_tmp


def import_foam_folder(
        path,
        search,
        files,
        skiplines=1,
        maxlines=0,
        skiptimes=slice(0,None),
        exclude=None,
        times_slice=None,
        ):
    """ returns a Dataframe for every file in fileList """
    #import StringIO
    fileList = find_datafiles(
        path, search=search, files=files,
        exclude=exclude, times_slice=times_slice
    )
    if not fileList:
        print("no files found")
        return None, DataFrame()
    p_bar = ProgressBar(n_tot=sum([len(l) for l in fileList.values()]))
    df = DataFrame()
    #df.index = MultiIndex.from_tuples(zip([],[]),names=['Loc',0])
    from collections import defaultdict
    origins = Origins()
    els = list(fileList.items())[skiptimes]
    for fullpath, files in els:
        time = strip_time(fullpath, path)
        df_tmp = DataFrame()

        # for fn in files:
        #     #ret = read_table(StringIO.StringIO(foam_to_csv(fn)))
        #     ret = read_data_file(fn, skiplines, maxlines)
        #     p_bar.next()

        args = [(fn, skiplines, maxlines, p_bar) for fn in files]
        if MULTIPROCESS:
            with multiprocessing.Pool(processes=MULTIPROCESS) as pool:
                rets = pool.map(read_data_file_args, args)
        else:
            rets = map(read_data_file_args, args)


        for fn, ret in zip(files, rets):
            if not ret or ret[1].empty:
                continue
            field_names, x, hashes = ret
            loc = x.index.values[-1][0]
            if df_tmp.empty:
                df_tmp = x
            else:
                try:
                    df_tmp = df_tmp.combine_first(x)
                except Exception as e:
                    print("failed to concat: ",
                            df_tmp, "and", x, "new_loc ",
                            x.index.levels[0][0], " existing_locs ",
                            df_tmp.index.levels[0] )
                    print(e)
            field_names = ([field_names] if not type(field_names) == list else field_names)
            for field in field_names:
                if field == "Pos":
                    continue
                origins.insert(time, loc, field, fn, hashes[field])
        df_tmp['Time'] = time
        if df.empty:
            df = df_tmp
        else:
            df = df.append(df_tmp)
    df.set_index('Time', append=True, inplace=True)
    if not "Loc" in  df.index.names:
        print(df)
        # df = df.reorder_levels(['Time', ])
    else:
        df = df.reorder_levels(['Time', 'Loc', 'Pos'])
    p_bar.done()
    return origins, df

"""
Time Loc        Pos U V
1000 radVel+10  0.1
              2
     radVel+20  0.1
                0.2
"""


def foam_to_csv(fn, ):
    """ helper function for d3.js data conversion
        prints data directly to std:out
    """
    try:
        with open(fn, encoding="utf-8") as f:
            content = f.readlines()
            start, num_entries = if_header_skip(content)
            entries = len(content[start].split())
            for l in content:
                print(re.sub("\t",",",re.sub("[\(\)\\n]","",l)))
    except Exception as e:
        print(e)

def read_boundary_names(fn):
    """ Todo use iterator method to avoid reading complete file """
    with open(fn, encoding="utf-8") as f:
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

def read_data_file_args(a):
    return read_data_file(a[0], skiplines=a[1], maxlines=a[2], p_bar=a[3])

def read_data_file(fn, skiplines=1, maxlines=False, p_bar=None):
    """  A function to read any foam data files returning data and
         index after header
    """

    # TODO check if sorting the index gives any performance benefits
    # print "opening file {}".format(fn)
    if not os.path.exists(fn):
        print("Can not open file " + fn)
        return None
    try:
        with open(fn, encoding="utf-8") as f:
            field = fn.split('/')[-1]
            content = f.readlines()
            content.append('bla')
            start, num_entries = if_header_skip(content)
            entries = len(content[start].split())
            is_a_vector = (True if entries > 1 else False)
            end = start + num_entries
            # FIXME this fails for eulerian/lagrangian vector fields
            # since no positional entry is produced
            if isinstance(p_bar, ProgressBar):
                p_bar.next()
            if is_a_vector:
                data = list(map(lambda x: re.sub("[0-9]*\(|\)", '', x).split(),
                            content[start:end:skiplines]))
                loc, names = evaluate_names(fn, entries)
                df = DataFrame(data=data, columns=names)
                if loc:
                    df['Loc'] = loc
                else:
                    df['Loc'] = range(len(df))
                if "Pos" in df:
                    df.set_index('Loc', append=False, inplace=True)
                    df["Pos"] = df["Pos"].astype(float)
                    df.set_index('Pos', append=True, inplace=True)
                else:
                    # if no pos is availible we have either
                    # an eulerian or lagrangian field
                    df.set_index('Loc', append=True, inplace=True)
                    df.index.names = ['Pos', 'Loc']
                    df = df.reorder_levels(['Loc', 'Pos'])
                df = df.astype(float)
                hashes = {}
                for row in df.columns:
                    hashes.update({row: hash_series(df[row])})
                return names, df, hashes
            # DataFile with a single row are seen as Eulerian or Lagrangian fields
            else:
                data = [np.float32(x) for x in content[start:end:skiplines]]
                entries = 1
                df = DataFrame(data=data, columns=[field])
                df['Loc'] = "Field"
                df.set_index('Loc', append=True, inplace=True)
                df.index.names=['Pos', 'Loc']
                df = df.reorder_levels(['Loc', 'Pos'])
                if HASH_RESULTS:
                    hashes = {field: int(hashlib.md5(str(data).encode('utf-8')).hexdigest(),16)}
                else:
                    hashes = {field: 0}
                return field, df, hashes
    except Exception as e:
        if DEBUG:
            print("Error processing datafile " + fn)
            print(e)
        return None

def hash_series(series):
    d = series.values
    d.flags.writeable = False #TODO needed?
    s = str(list(d)).encode('utf-8')
    if HASH_RESULTS:
        return int(hashlib.md5(s).hexdigest(),16) #NOT
    else:
        return 0



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
        return "Field", [filename + '_' + str(i) for i in range(num_entries)]


def req_file(file_name, requested):
    """ True if file name is list of requested files """
    if requested == True:
        return requested
    else:
        return file_name.split('/')[-1] in requested


def import_logs(folder, search, keys, time_key="^Time = "):
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
        for key, col_names in keys.items():
            if re.search(key, line):
                return col_names, list(
                        map(float,filter(lambda x:
                        x, re.findall("[0-9\-]+[.]?[0-9]*[e]?[\-\+]?[0-9]*", line))))
        return None, None

    fold, dirs, files = next(os.walk(folder))
    logs = [fold + "/" + log for log in files if search in log]
    p_bar = ProgressBar(n_tot = len(logs))
    # Lets make sure that we find Timesteps in the log
    keys.update({time_key: ['Time']})

    for log_number, log_name in enumerate(logs):
        with open(log_name, encoding="utf-8") as log:
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
                    df = concat([df, DataFrame(dataDict)])
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
            print(log_name)
            print("failed to process")
            print(e)
            return {}, None
    return {}, df #DataFrame()



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
