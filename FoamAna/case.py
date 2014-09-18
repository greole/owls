import os
import analysis as ana
from pandas import Series
from pandas import concat


def items_from_dict(dict, func, **kwargs):
    return {name: func(folder=folder,name=name, symb=symb, **kwargs)
               for name, (folder,symb) in dict.iteritems()}

def read_sets(folder, plot_props={}, name="None", **kwargs):
    return Item(folder, search_files=False, search_pattern="./sets/{}/",
            plot_props=plot_props, name=name, **kwargs)

def read_lag(folder, files, plot_props={}, skiplines=1,
            name="None", cloud="coalCloud1", **kwargs):
    return Item(folder, search_files=files,
            search_pattern= "./{}/" + "lagrangian/{}/".format(cloud),
            plot_props=plot_props, name=name, skiplines=skiplines, **kwargs)

def read_eul(folder,  files, plot_props={}, skiplines=1, name="None", **kwargs):
    return Item(folder, search_files=files, search_pattern="./{}/",
            plot_props=plot_props, name=name, skiplines=skiplines, **kwargs)

def read_exp(folder, plot_props={}, name="None",**kwargs):
    return Item(folder, search_files=False, plot_props=plot_props,
            search_pattern="./{}/", name=name, **kwargs)


def read_logs(folder, log_name='*log*', keys=None):
    os.chdir(folder)
    if keys:
        print "reading logs"
        return extractFromLog(keys, older, log_name)

class Item():
    """ Data reprensentation of OpenFOAM field (eulerian and lagrangian)
    and set files. Instantiated through read methods, e.g:
    read_sets, read_lag, read_eul, read_exp


    Examples:
    ----------

    case = read_sets(folder="home/user/case",plot_props={})
    case.data # access data frame

    Parameters:
    ----------
    folder: data location containing a time or sets folder
    files: search only for files with given name, None for all files
    plot_props: dictionary for consistent plotting of ranges and ax labels
    skiplines: read only every n-th entry
    cloud: name of lagrangian cloud
    name: case name for plot legends

    Note:
    ----------

    If data is accessed through [] only latest item is returned. For full times
    access iteratetimes() can be used.


    TODO:

        make iteratetimes() access a delta
    """
    def __init__(self, folder,
                 search_files,
                 search_pattern,
                 plot_props=None,
                 files=None,
                 skiplines=1,
                 name="None",
                 symb="o",
                 maxlines=0,
                ):

        self.plot_props = plot_props
        self.folder = folder
        self.name = name
        os.chdir(folder)
        self.maxlines=maxlines
        self.search_files=search_files
        self.search_pattern=search_pattern
        self.times = ana.find_times(self.folder)
        self.skiplines = skiplines
        self.origins, self.data = self._read_data()
        if self.data:
            self.append_plot_props()
        self.symb=symb

    def _read_data(self):
        """ call foam_to_DataFrame for all entries in read_list """
        search = self.search_pattern
        print self.name + ": ",
        origins, data = ana.foam_to_DataFrame(search_format=search,
                                 file_names=self.search_files,
                                 plot_props=self.plot_props,
                                 skiplines=self.skiplines,
                                 maxlines=self.maxlines
                                 )
        return origins, data

    def add(self, data, label):
        """
        Add a given Series

        Usage:
        -------
        case.add(sqrt(uu),'u_rms')
        """
        if not self.data:
            return
        time = max(self.data.keys())
        self.data[time][label] = data
        self.append_plot_props()
        return self.data[time][label]

    def _column_to_file(self, time, col):
        """ find corresponding file for given time and column """
        for key, value in self.origins.iteritems():
            if time in key and col in key:
                    return value
        else:
            return "NONE"

    def append_plot_props(self):
        """ """
        if not self.data:
            return
        for time, df in self.data.iteritems():
            for col in df.columns:
                prop = ana.match(self.plot_props, col)
                df[col].name = self.name
                df[col].origin = self._column_to_file(time, col)
                if prop:
                        df[col].label = prop[0]
                        df[col].data_range = prop[1]
                else:
                    df[col].label = 'no label'
                    df[col].data_range = [df[col].min(), df[col].max()]

    ############################# Time access ##################################
    @property
    def latest_time(self):
        """ return latest time instance """
        if not self.data:
            return
        latest_time = max(self.data.keys())
        return latest_time

    def iteratetimes(self, delta_t=0):
        """ iterator to iterate over all sets entries
            to create convergence check plots """
        if not self.data:
            return
        for time, df in self.data.iteritems():
            for col in df.columns:
                df[col].name = "{} @{:1.4}s".format(self.name, float(time))
            yield time, df

    def values_at_position(self, field, position):
        if not self.data:
            return
        times = Series()
        values = Series()
        field_ind = field.split('_')[0]
        for time, df in self.data.iteritems():
            val = df[field].where(df[field_ind] == position).dropna()
            times.append(Series(time))
            values.append(Series(val))
        return times, values

    #########################################################################
    def _get_idx_names(self, keyword):
        """ search for all index names matching keyword"""
        if type(keyword) != list:
            return [field for field in self.vars
                 if keyword in field and self._is_index(field)]
        else:
            return [_ for key in keyword for _ in self._get_idx_names(key)]

    def _get_field_names(self, keyword):
        """ search for all field names matching keyword"""
        if type(keyword) != list:
            return [field for field in self.vars
                 if keyword in field and not self._is_index(field)]
        else:
            return [_ for key in keyword for _ in self._get_field_names(key)]

    #########################################################################


    def combine(self, inp):# idxs, name):
        """ combines multiple separate index fields 
        """
        if not self.data:
            return
        def replace_names(lst, new_name, old_idxs):
            return [field.replace(_, new_name)
                         for field in lst
                         for _ in old_idxs if _ in field]

        def unique(lst):
            return list(set(lst))

        from collections import defaultdict
        d = defaultdict(dict)
        for combined_name, fields in inp.iteritems():
            concat_fields = unique(self._get_field_names(fields))
            concat_idx = self._get_idx_names([_.split('_')[0] for _ in concat_fields])
            new_idx = replace_names(concat_idx, combined_name, concat_idx)
            new_fields = replace_names(concat_fields, combined_name, unique(concat_idx))
            for time, df in self.data.iteritems():
                ids = concat([Series([_ for _ in concat_fields for i in df[_]])])
                concat_idx_vals = [df[_] for _ in concat_idx]
                concat_val = [df[_] for _ in concat_fields]
                new_idx_name = new_idx[0]
                new_idx = concat(concat_idx_vals).reset_index(level=0,drop=True)
                d[time].update({new_idx_name:new_idx})
                d[time].update({"ids"+new_idx_name:ids})
                new_val_concat = concat(concat_val).reset_index(level=0,drop=True)
                """
                print concat_fields
                for i,val in enumerate(new_val_concat):
                    print i, new_idx[i], new_val_concat[i], ids[i]
                print new_val_concat
                """
                for i, target in enumerate(concat_fields):
                    selection_mask = ids.isin([target])#[concat_fields[i]])
                    new_val = new_val_concat[selection_mask]
                    d[time].update({new_fields[i]:new_val})
                    d[time].update({"select" + new_fields[i]:selection_mask})

        for time, fields in d.iteritems():
            self.data[time] = self.data[time].reindex(range(1000))
            for name, field in fields.iteritems():
                self.data[time][name] = field

    def rename(self, names):
        if not self.data:
            return
        for time, df in self.data.iteritems():
            renamed=[]
            for name in df.columns:
                if name in names:
                    renamed.append(names[name])
                else:
                    renamed.append(name)
            df.columns = renamed
            self.append_plot_props()

    def get(self, form, pos, vals, times=False):
        pos_inserted = form.split('_')[0].format(pos) #FIXME support pos lists
        index = self.__getitem__(pos_inserted)
        vals_inserted = [self.__getitem__(form.format(pos,val)) 
                            for val in vals]
        return [index] + vals_inserted

    def _is_index(self, name):
        """ test if given column name is an index """
        _ = name.split('_')
        if len(_) == 1 or _[-1] == '0':
            return True
        else:
            return False

    ############################################################################
    @property
    def vars(self):
        if not self.data:
            return
        """ return names of all entries for latest timestep """
        latest_time = max(self.data.keys())
        return self.data[latest_time].columns

    def __getitem__(self, field):
        try:
            return self.data[self.latest_time][field]
        except:
            print "%s Warning: requested field %s not in data base" %(self.name, field)
            return Series()

    @staticmethod
    def condition(field, target, condition, operator):
        return eval('{field}[{target} {condition}]'.format(field,
                                                           target,
                                                           condition))
    ############### REV !! ####################################################

    def refresh(self, name):
        print "refresh"
        find_times()
        refreshed = getattr(self, 'read_' + name)()
        setattr(self, name, refreshed)

