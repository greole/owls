from __future__ import print_function
from future.builtins import *

import os
# import re
import shelve
from collections import OrderedDict

from pandas import Series, DataFrame, Index
# from pandas import concat

from . import MultiFrame as mf
from . import plot as plt
from . import io


# Series.__repr__ = (lambda x: ("Hash: {}\nTimes: {}\nLoc: {}\nValues: {}".format(
#                     io.hash_series(x),
#                     list(set(x.keys().get_level_values('Time'))), # avoid back and forth conversion
#                     list(set(x.keys().get_level_values('Loc'))),
#                     x.values))) #TODO monkey patch to use hashes
Database = False

if Database:
    case_data_base = shelve.open(os.path.expanduser('~') + "/.owls/db")
else:
    case_data_base = dict()


def from_dict(input_dict, func, **kwargs):
    return {name: func(folder=folder, name=name, **kwargs)
            for name, folder in input_dict.items()}


def read_sets(folder, name="None",
              search=io.FPNUMBER,
              **kwargs):
    def setsfolder(folder):
        p = os.path.join(folder, "postProcessing")
        return (os.path.join(p, "sets") if os.path.exists(p)
                else os.path.join(folder, "sets"))

    return FoamFrame(folder=setsfolder(folder), search_files=False,
                     search_pattern=search, name=name,
                     show_func="plot", preHooks=None,
                     exclude=['processor'], **kwargs)


def read_lag(folder, files, skiplines=1,
             name="None", cloud="[A-Za-z]*Cloud1",
             preHooks=None, decomposed=False, **kwargs):
    search = io.FPNUMBER + "/lagrangian/" + cloud,
    search = (search if not decomposed else "processor[0-9]?/" + search)
    return FoamFrame(folder=folder, search_files=files,
                     search_pattern=search, name=name,
                     skiplines=skiplines, show_func="scatter",
                     **kwargs)


def read_eul(folder, files, skiplines=1, name="None",
             decomposed=False, preHooks=None, **kwargs):
    search = io.FPNUMBER
    search = (search if not decomposed else "processor[0-9]?/" + search)
    return FoamFrame(folder=folder, search_files=files,
                     search_pattern=search, name=name,
                     skiplines=skiplines, show_func="scatter",
                     preHooks=preHooks, **kwargs)


def read_exp(folder, name="None", search="", **kwargs):
    return FoamFrame(folder=folder, search_files=False,
                     search_pattern=search, name=name,
                     show_func="scatter", **kwargs)


def read_log(folder, keys, log_name='*log*', plot_properties=False):
    origins, df = io.import_logs(folder, keys)
    ff = FoamFrame(df)
    ff.properties = Props(
        origins=origins, name='LogFiles',
        plot_properties=plot_properties,
        folder=folder, times=[0], symb="-",
        show_func="plot")
    return ff

""" Filter Helper Functions """

isIn = lambda x: lambda y: x in y
isNotIn = lambda x: lambda y: x not in y


class PlotProperties():

    def __init__(self):
        from collections import defaultdict
        self.properties = defaultdict(dict)

    def insert(self, field, properties):
        self.properties[field].update(properties)
        return self

    def set(self, inserts):
        for k, d in inserts.items():
            self.insert(k, d)

    def select(self, field, prop, default=None):
        field = self.properties[field]
        if not field:
            return
        else:
            return field.get(prop, default)


class Props():

    def __init__(self, origins, name,
                 plot_properties, folder,
                 times, symb, show_func):
        self.origins = origins
        self.name = name
        self.plot_properties = plot_properties
        self.folder = folder
        self.times = times
        self.latest_time = max(times)
        self.symb = symb
        self.show_func = show_func


class FoamFrame(DataFrame):
    """ Data reprensentation of OpenFOAM field (eulerian and lagrangian)
    and set files. Instantiated through read methods, e.g:
    read_sets, read_lag, read_eul, read_exp


    Examples:
    ----------

    case = read_sets(folder="home/user/case",plot_properties={})
    case.data # access data frame

    Parameters:
    ----------
    folder: data location containing a time or sets folder
    files: search only for files with given name, None for all files
    plot_properties: dictionary for consistent plotting of ranges and ax labels
    skiplines: read only every n-th entry
    cloud: name of lagrangian cloud
    name: case name for plot legends

    Note:
    ----------

    If data is accessed through [] only latest item is returned. For full times
    access iteratetimes() can be used.

    Categories:

        { "rad_pos": lambda field -> position
          "centreLine": [] lambda field -> i of []

        }

        example:
            lambda field: re.search('[0-9]*\.[0-9]*').group()[0]

    TODO:
        use case as cases ojects with a 3-level index
             case['u']
             acces time of all cases -> df.iloc[df.index.isin([1],level=1)]
        refactor plot into case objects itself,
            ?case.show('t','u', time_series = False)
        refactor origins
        make iteratetimes() access a delta
    """
    def __init__(self, *args, **kwargs):

        skip = kwargs.get('skiplines', 1)
        times = kwargs.get('skiptimes', 1)
        name = kwargs.get('name', 'None')
        symb = kwargs.get('symb', 'o')
        files = kwargs.get('search_files', None)
        properties = kwargs.get('properties', None)
        lines = kwargs.get('maxlines', 0)
        search = kwargs.get('search_pattern', io.FPNUMBER)
        folder = kwargs.get('folder', None)
        plot_properties = kwargs.get('plot_properties', PlotProperties())
        show_func = kwargs.get('show_func', None)
        validate = kwargs.get('validate', True)
        preHooks = kwargs.get('preHooks', None)
        exclude = kwargs.get('exclude', [" "])  # FIXME

        keys = ['skiplines',
                'skiptimes',
                'preHooks',
                'name',
                'symb',
                'search_files',
                'properties',
                'maxlines',
                'search_pattern',
                'folder',
                'plot_properties',
                'show_func',
                'exclude',
                ]

        for k in keys:
            if k in kwargs:
                kwargs.pop(k)

        # TODO explain what happens here
        if folder is None:
            # super(FoamFrame, self).__init__(*args, **kwargs)
            DataFrame.__init__(self, *args, **kwargs)
        else:
            if preHooks:
                for hook in preHooks:
                    hook.execute()
            if (folder in case_data_base) and Database:
                print("re-importing", end=" ")
            else:
                print("importing", end=" ")
            print(name + ": ", end="")
            origins, data = io.import_foam_folder(
                path=folder,
                search=search,
                files=files,
                skiplines=skip,
                maxlines=lines,
                skiptimes=times,
                exclude=exclude,
                )
            try:
                DataFrame.__init__(self, data)
            except:
                pass
            self.properties = Props(
                origins,
                name,
                plot_properties,
                folder,
                # FIXME fix it for read logs
                data.index.levels[0],
                symb,
                show_func)
            if validate and Database:
                self.validate_origins(folder, origins)
            # register to database
            if Database:
                case_data_base.sync()

    def validate_origins(self, folder, origins):
        origins.update_hashes()
        if case_data_base.has_key(folder):
            if (case_data_base[folder]["hash"] == origins.dct["hash"]):
                print(" [consistent]")
            else:
                entries_new = len(origins.dct.keys())
                entries_old = len(case_data_base[folder].keys())
                if entries_new > entries_old:
                    print("[new timestep] ")
                    # print origins.dct.keys()
                    case_data_base[folder] = origins.dct
                elif entries_new < entries_old:
                    # print folder
                    # print origins.dct.keys()
                    # print case_data_base[folder].keys()
                    print("[missing timestep]")
                    case_data_base[folder] = origins.dct
                elif entries_new == entries_old:
                    print("[corrupted]", end="")
                    for time, loc, field, item in origins.hashes():
                        time_name, time_hash   = time
                        loc_name, loc_hash     = loc
                        field_name, field_hash = field
                        filename, item_hash    = item
                        try:
                            orig_hash = case_data_base[folder][time_name][loc_name][field_name][1]
                        except:
                            orig_hash = item_hash
                        if (item_hash != orig_hash):
                            print("")
                            print("corrupted fields:")
                            print("\t" + field_name + " in " +  filename)
                    case_data_base[folder] = origins.dct
        else:
            case_data_base[folder] = origins.dct

    def add(self, data, label):
        """
        Add a given Series

        Usage:
        ------ing-
        case.add(sqrt(uu),'u_rms')
        """
        self.latest[label] = data
        return self

    def source(self, col):
        """ find corresponding file for column """
        # return get time loc  and return dict for every column
        # latest.source['u']
        return

    def __str__(self):
        return "FoamFrame: \n" + super(FoamFrame, self).__str__()

    @property
    def _constructor(self):
        # override DataFrames constructor
        # to enable method chaining
        return FoamFrame

    @property
    def times(self):
        """ return times for case """
        return set([_[0] for _ in self.index.values])

    @property
    def locations(self):
        """ return times for case """
        return set([_[1] for _ in self.index.values])

    @property
    def latest(self):
        """ return latest time for case """
        import pandas as pd
        ret = self.loc[[self.properties.latest_time]]
        ret.properties = self.properties
        return ret

    # def _iter_names(self)
    #     pass
    #
    # def get_hashes(self):
    #     """ returns hashes of current selection based
    #         on the data read from disk """
    #     pass

    def at(self, idx_name, idx_val):
        """ select from foamframe based on index name and value"""
        # TODO FIX This
        ret = self[self.index.get_level_values(idx_name) == idx_val]
        # match = [(val in idx_val)
        #      for val in self.index.get_level_values(idx_name)]
        # ret = self[match]
        ret.properties = self.properties
        return ret

    def id(self, loc):
        """ Return FoamFrame based on location """
        return self.at(idx_name='Id', idx_val=loc)

    def location(self, loc):
        """ Return FoamFrame based on location """
        return self.at(idx_name='Loc', idx_val=loc)

    def loc_names(self, key):
        """ search for all index names matching keyword"""
        return [_ for _ in  self.index.get_level_values("Loc") if key in _]

    def field_names(self, key):
        """ search for all field names matching keyword"""
        return [_ for _ in self.columns if key in _]

    def rename(self, search, replace):
        """ rename field names based on regex """
        import re
        self.columns = [re.sub(search, replace, name) for name in self.columns]

    def rename_idx(self, search, replace):
        """ rename field names based on regex """
        self.index = Index(
            [(t, replace if x == search else x, i) for t, x, i in list(self.index)],
            names=self.index.names)

    def rename_idxs(self, rename_map):
        """ rename multiple field names based dictionary
            of {search: replace} """
        for s, r in rename_map.items():
            self.rename_idx(s, r)


    def _is_idx(self, item):
        """ test if item is column or idx """
        itemt = type(item)
        # if item is Series of booleans
        # it cant be an index
        from past.builtins import unicode
        from past.builtins import str as text
        if itemt not in [int, str, float, unicode, text]:
            return False
        else:
            return item in self.index.names

    def __getitem__(self, item):
        """ call pandas DataFrame __getitem__ if item is not
            an index
        """
        if self._is_idx(item):
            level = self.index.names.index(item)
            return list(zip(*self.index.values))[level]
        else:
            if (type(item) is str) and item not in self.columns:
                return Series()
            else:
                return super(FoamFrame, self).__getitem__(item)

    def draw(self, x, y, z, title, func, figure, **kwargs):

        def _label(axis, field):
            label = kwargs.get(axis + '_label', False)
            if label:
                self.properties.plot_properties.insert(
                    field, {axis + '_label': label})
            else:
                label = self.properties.plot_properties.select(
                    field, axis + '_label', "None")
            return label

        def _range(axis, field):
            from bokeh.models import Range1d
            p_range_args = kwargs.get(axis + '_range', False)
            if p_range_args:
                self.properties.plot_properties.insert(
                    field, {axis + '_range': p_range})
            else:
                p_range = self.properties.plot_properties.select(
                    field, axis + '_range')
            if not p_range:
                return False
            else:
                return Range1d(start=p_range[0], end=p_range[1])

        # TODO: change colors if y is of list type
        # wrap y to a list so that we can iterate
        y = (y if type(y) == list else [y])

        figure_properties = {"title": title}

        if kwargs.get('x_range', False):
            figure_properties.update({"x_range": kwargs.get('x_range')})
        figure.set(**figure_properties)
        for yi in y:
            x_data, y_data = self[x], self[yi]
            # TODO FIXME
            for k in ['symbols', 'order', 'colors', 'symbol']:
                if k in kwargs.keys():
                    kwargs.pop(k)
            getattr(figure, func)(x=x_data,
                                  y=y_data,
                                  **kwargs)

        for ax, data in {'x': x, 'y': y[0]}.items():
            if _label(ax, data):
                getattr(figure, ax+'axis')[0].axis_label = _label(ax, data)
            # setattr(getattr(figure, ax + 'axis'),
            #         'axis_label', _label(ax, data))
            if _range(ax, data):
                r = setattr(figure, ax+'_range', _range(ax, data))
        return figure

    def scatter(self, y, x='Pos', z=False, title="", figure=False, **kwargs):
        figure = (figure if figure else plt.figure())
        return self.draw(x, y, z, title, func="scatter", figure=figure, **kwargs)

    def plot(self, y, x='Pos', z=False, title="", figure=False, **kwargs):
        figure = (figure if figure else plt.figure())
        if kwargs.get('symbol', None):
            kwargs.pop('symbol')
        return self.draw(x, y, z, title, func="line", figure=figure, **kwargs)


    def show(self, y, x=None, figure=False, **kwargs):
        figure = (figure if figure else plt.figure())
        if x:
            return getattr(self, self.properties.show_func)(y=y, x=x, figure=figure, **kwargs)
        else:
            return getattr(self, self.properties.show_func)(y=y, figure=figure, **kwargs)

    def show_func(self, value):
        """ set the default plot style
            valid arguments: scatter, plot """
        self.properties.show_func = value

    def set_plot_properties(self, **values):
        """ set plot properties  """
        self.properties.plot_properties.set(values)

    def filterLocs(self, index):
        """ filter based on locations """
        return self.filter(name='Loc', index=index)

    def filter(self, name, index=None, field=None):
        """ filter on index or field values by given functioni

            Examples:

                .filter(name='T', field=lambda x: 1000<x<2000)
                .filter(name='Loc', index=lambda x: 0.2<field_to_float(x)<0.8)
        """
        if index:
            ret = self[list(map(index, self.index.get_level_values(name)))]
            ret.properties = self.properties
            return ret
        elif field:
            ret = self[list(map(field,self[name]))]
            ret.properties = self.properties
            return ret
        else:
            return self

    def by_index(self, field, func=None):
        func = (func if func else lambda x: x)
        return self.by(field, index=func)

    # def map_level(self, dct, level=0):
    #     index = self.index
    #     index.set_levels([[dct.get(item, item)
    #         for item in names] if i==level else names
    #         #for i, names in enumerate(index.levels)], inplace=True)
    #         for i, names in enumerate(index.levels)], inplace=False)
    #     self.index = index
    #     return self

    def by_field(self, field, func=None):
        func = (func if func else lambda x: x)
        return self.by(field, field=func)

    def by(self, name, index=None, field=None):
        """ facet by given function

            Examples:

            .by(index=lambda x: x)
            .by(field=lambda x: ('T_high' if x['T'] > 1000 else 'T_low'))
        """
        ret = OrderedDict()
        if index:
            index_values = self.index.get_level_values(name)
            idx_values = sorted(set(index_values))
            for val in idx_values:
                ret.update([(index(val), self[index_values == val])])
        else:
            selection = self[name].apply(field)
            for cat in set(selection):
                ret.update([(cat, self[selection == cat])])
        for _ in ret.values():
            _.properties = self.properties
        return mf.MultiFrame(ret)
