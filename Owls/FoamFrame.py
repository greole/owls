# TODO MultiFrame -> GroupedFrame
#      new MultiFrame for multidata

from __future__ import print_function
from future.builtins import *

import os
import shelve
from collections import defaultdict

from pandas import Series, DataFrame, Index, MultiIndex

from .io import FPNUMBER, import_foam_folder, import_logs

import numpy as np

try:
    from Salvia import Gnuplot
except:
    Gnuplot = None
    print("No Salvia installation found")

# Series.__repr__ = (lambda x: ("Hash: {}\nTimes: {}\nLoc: {}\nValues: {}".format(
#                     io.hash_series(x),
#                     list(set(x.keys().get_level_values('Time'))), # avoid back and forth conversion
#                     list(set(x.keys().get_level_values('Loc'))),
#                     x.values))) #TODO monkey patch to use hashes
Database = False

latestTime = slice(-1, None)
allTimes = slice(0, None)

if Database:
    case_data_base = shelve.open(os.path.expanduser('~') + "/.owls/db")
else:
    case_data_base = dict()

rcParams = {
        "plotWrapper": Gnuplot
        }

def read_sets(folder, name="None",
              search=FPNUMBER,
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
    search = FPNUMBER + "/lagrangian/" + cloud
    search = (search if not decomposed else "processor[0-9]?/" + search)
    return FoamFrame(folder=folder, search_files=files,
                     search_pattern=search, name=name,
                     skiplines=skiplines, show_func="scatter",
                     **kwargs)


def read_eul(folder, files, skiplines=1, name="None",
             decomposed=False, preHooks=None, **kwargs):
    search = FPNUMBER
    search = (search if not decomposed else "processor[0-9]?/" + search)
    return FoamFrame(folder=folder, search_files=files,
                     search_pattern=search, name=name,
                     skiplines=skiplines, show_func="scatter",
                     preHooks=preHooks, **kwargs)


def read_exp(folder, name="None", search="", **kwargs):
    return FoamFrame(folder=folder, search_files=False,
                     search_pattern=search, name=name,
                     show_func="scatter", **kwargs)


def read_log(folder, keys, log_name='log', plot_properties=False, name="None", **kwargs):
    origins, df = import_logs(folder, log_name, keys, **kwargs)
    ff = FoamFrame(df)
    plot_properties = plot_properties if plot_properties else PlotProperties()
    ff.properties = Props(
        origins=origins, name=folder,
        plot_properties=plot_properties,
        folder=folder, symb="-",
        show_func="plot")
    return ff

""" Filter Helper Functions """

isIn = lambda x: lambda y: x in y
isNotIn = lambda x: lambda y: x not in y


class PlotProperties():

    def __init__(self):
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
    # TODO default args

    def __init__(self, origins, name,
                 plot_properties, folder,
                 symb, show_func):
        self.origins = origins
        self.name = name
        self.plot_properties = plot_properties
        self.folder = folder
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
        times = kwargs.get('readtime', slice(0, None))
        name = kwargs.get('name', 'None')
        symb = kwargs.get('symb', 'o')
        files = kwargs.get('search_files', None)
        properties = kwargs.get('properties', None)
        lines = kwargs.get('maxlines', 0)
        search = kwargs.get('search_pattern', FPNUMBER)
        folder = kwargs.get('folder', None)
        plot_properties = kwargs.get('plot_properties', PlotProperties())
        show_func = kwargs.get('show_func', None)
        validate = kwargs.get('validate', True)
        preHooks = kwargs.get('preHooks', None)
        exclude = kwargs.get('exclude', [" "])  # FIXME
        times_stride = kwargs.get('times_stride', 1)
        times_range = kwargs.get('times_range', "all") # FIXME implement strides
        times_slice = times_range

        keys = ['skiplines',
                'readtime',
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
                'times_stride',
                'times_range',
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
            origins, data = import_foam_folder(
                path=folder,
                search=search,
                files=files,
                skiplines=skip,
                maxlines=lines,
                skiptimes=times,
                exclude=exclude,
                times_slice=times_slice
                )
            try:
                DataFrame.__init__(self, data)
            except Exception as e:
                print(e)
            self.properties = Props(
                origins,
                name,
                plot_properties,
                folder,
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

    def source(self, col):
        """ find corresponding file for column """
        # return get time loc  and return dict for every column
        # latest.source['u']
        return

    # ----------------------------------------------------------------------
    # Internal helper methods

    @property
    def _constructor(self):
        # override DataFrames constructor
        # to enable method chaining
        return FoamFrame

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


    @property
    def grouped(self):
        return self._is_idx("Group")

    @staticmethod
    def from_dict(input_dict, name="None",
            plot_properties=None, symb=".", show_func="scatter"
            ):
        """ import raw data from python dictionary
            format {(timestep, pos, ): [fields]}
            usage: {(0):[1,2,3]}

        """
        pP = (PlotProperties() if not plot_properties else plot_properties)
        elems = len(input_dict[list(input_dict.keys())[0]])
        zeros = [0 for _ in range(elems)]
        pos = (input_dict[("Pos")] if input_dict.get(("Pos"),False) else zeros)
        nums = list(range(elems))
        if input_dict.get("Pos"):
                input_dict.pop("Pos")
        mi = MultiIndex(
                levels=[zeros, zeros, pos],
                labels=[nums, nums, nums],
                names=['Time', 'Loc', 'Pos'])
        ff = FoamFrame(DataFrame(input_dict, index=mi), folder=None)
        ff.properties = Props("raw", name, pP, "", symb, show_func)
        ff.index = mi
        return ff

    # ----------------------------------------------------------------------
    # Info methods

    def __str__(self):
        return "FoamFrame: \n" + super(FoamFrame, self).__str__()

    @property
    def times(self):
        """ return times for case """
        return set([_[0] for _ in self.index.values])

    @property
    def locations(self):
        """ return times for case """
        return set([_[1] for _ in self.index.values])

    # ----------------------------------------------------------------------
    # Selection methods

    def __getitem__(self, item):
        """ call pandas DataFrame __getitem__ if item is not
            an index
        """
        if self._is_idx(item):
            try:
                level = self.index.names.index(item)
                return list(zip(*self.index.values))[level]
            except:
                return
                # print("failed ", item) NOTE for debugging
        else:
            if (type(item) is str) and item not in self.columns:
                return Series()
            else:
                return super(FoamFrame, self).__getitem__(item)

    @property
    def latest(self):
        """ return latest time for case """
        ret = self.query('Time == {}'.format(self.latest_time))
        ret.properties = self.properties
        return ret

    @property
    def latest_time(self):
        """ return value of latest time step """
        return max(self.index.levels[0])

    @property
    def earliest_time(self):
        """ return value of latest time step """
        return min(self.index.levels[0])

    def after(self, time):
        return self.filter("Time", index=lambda x: x > time)

    def at_time(self, time):
        """ return latest time for case """
        ret = self.query('Time == {}'.format(time))
        ret.properties = self.properties
        return ret


    def at(self, idx_name, idx_val):
        """ select from foamframe based on index name and value"""
        # TODO FIX This
        ret = self[self.index.get_level_values(idx_name) == idx_val]
        # match = [(val in idx_val)
        #      for val in self.index.get_level_values(idx_name)]
        # ret = self[match]
        if idx_name == "Group":
            ret.index = ret.index.droplevel("Group")

        ret.properties = self.properties
        return ret

    def id(self, loc):
        """ Return FoamFrame based on location """
        return self.at(idx_name='Pos', idx_val=loc)

    def location(self, loc):
        """ Return FoamFrame based on location """
        return self.at(idx_name='Loc', idx_val=loc)

    def loc_names(self, key):
        """ search for all index names matching keyword"""
        return [_ for _ in  self.index.get_level_values("Loc") if key in _]

    def field_names(self, key):
        """ search for all field names matching keyword"""
        return [_ for _ in self.columns if key in _]

    # ----------------------------------------------------------------------
    # Manipulation methods

    def add(self, data, label):
        """
        Add a given Series

        Usage:
            case.add(sqrt(uu),'u_rms')
        """
        self.latest[label] = data
        return self

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

    # ----------------------------------------------------------------------
    # Plotting methods

    def draw(self, x, y, z, title, func, figure, data=None,
            legend_prefix="", titles=None, **kwargs):
        data = (data if isinstance(data, DataFrame) else self)
        return rcParams["plotWrapper"].draw(
                    x=x, y=y, z=z, data=data, title=title,
                    func=func, figure=figure,
                    legend_prefix="", titles=None,
                    properties=self.properties, **kwargs)

    def histo_data(self, y, weights, bins):
        return np.histogram(
                y, density=True, weights=weights,
                bins=bins)

    def histogram(self, y, x=None, title="", figure=False, weights=False, **kwargs):
        figure = (figure if figure else rcParams["plotWrapper"].GnuplotFigure())
        if weights:
            weights = self[weights]
        hist, edges = self.histo_data(self[y], weights, kwargs.get("bins", 50))

        centres = [(edges[i] + edges[i+1])*0.5 for i in range(len(edges)-1)]
        df = DataFrame({'centres': centres, 'hist': hist})

        return self.draw(x='centres', y='hist', z=None,
                data=df, title=title, func="quad", figure=figure, **kwargs)

    def cdf(self, y, x=None, title="", figure=False, weights=False, **kwargs):
        a, b = np.histogram(self[y], weights=self[weights], bins=20, normed=True)
        dx = b[1]-b[0]
        cdf = np.cumsum(a)*dx
        df = DataFrame({'centres': b[1:], 'hist': cdf})

        return self.draw(x='centres', y='hist', z=None,
                data=df, title=title, func="line", figure=figure, **kwargs)

    def scatter(self, y, x='Pos', z=None, title="", figure=False, **kwargs):
        figure = (figure if figure else rcParams["plotWrapper"].GnuplotFigure())
        return self.draw(x, y, z, title, func="scatter", figure=figure, **kwargs)

    def plot(self, y, x='Pos', z=None, title="", figure=False, **kwargs):
        figure = (figure if figure else rcParams["plotWrapper"].GnuplotFigure())
        if kwargs.get('symbol', None):
            kwargs.pop('symbol')
        return self.draw(x, y, z, title, func="line", figure=figure, **kwargs)


    def show(self, y, x="Pos", figure=False,
             overlay="Field", style=None,
             legend_prefix="", post_pone_style=False,
             row=None, titles=None, **kwargs):

        if kwargs.get("props", False):
            props = kwargs.pop("props")
            self.properties.plot_properties.set(props)

        def create_figure(y_, f, title="", legend=""):

            # TODO use plot wrapper class here
            if kwargs.get("title"):
                title = kwargs.get("title")
                kwargs.pop("title")
            return getattr(self, self.properties.show_func)(
                            y=y_, x=x, figure=f,
                            legend_prefix=legend_prefix+legend,
                            title=title, **kwargs)

        def create_figure_row(y, arow=None):

            # TODO let arow be an empty mutliplot
            if not arow:
                fn = kwargs.get("filename")
                arow = rcParams["plotWrapper"].GnuplotMultiplot([], filename=fn)

            if not self.grouped:
                y = (y if isinstance(y, list) else [y])
                if overlay == "Field":

                    # SINGLE FIGURE MUTLIPLE FIELDS
                    ids = "".join(y)
                    fig_id, f = (figure if figure else (ids, arow.get(ids)))
                    for yi in y:
                        create_figure(yi, f)
                    arow[fig_id] = f

                if not overlay:

                    # MULTIPLE FIGURES
                    # test if figure with same id already exists
                    # so that we can plot into it
                    # otherwise create a new figure
                    for i, yi in enumerate(y):
                        title = ("" if not titles else titles[i])
                        f = arow.get(yi)
                        arow[yi] = create_figure(yi, f, title=title)

            if self.grouped:
                groups = list(set(self["Group"]) if self["Group"] else set())
                groups.sort()
                if overlay == "Group":
                    # ALIGN ALONG GROUPS
                    # for every yi a new figure is needed
                    for yi in y:

                        f = arow.get(yi)

                        for group in groups:
                            arow[yi] = self.at("Group", group).show(
                                    x=x, y=yi, title=yi, figure=(yi, f),
                                    overlay="Field",
                                    legend_prefix=legend_prefix,
                                    legend=str(group),
                                    **kwargs)[yi]

                if overlay == "Field":
                    for group in groups:

                        f = arow.get(group)

                        field = self.at("Group", group)
                        arow[group] = field.show(x=x, y=y, title=str(group),
                                                 figure=(group, f), overlay="Field",
                                                 post_pone_style=True,
                                                 legend_prefix=legend_prefix,
                                                 **kwargs)[group]
            return arow

        fig_row = create_figure_row(y, row)
        return fig_row

    def show_func(self, value):
        """ set the default plot style
            valid arguments: scatter, plot """
        self.properties.show_func = value

    def set_plot_properties(self, **values):
        """ set plot properties  """
        self.properties.plot_properties.set(values)

    # ----------------------------------------------------------------------
    # Filter methods

    def filter_fields(self, name, lower, upper):
        """ filter based on field values

            Examples:

                .filter_fields('T', 1000, 2000)
        """
        return self.filter(name, field=lambda x: lower < x < upper)

    def filter_locations(self, index):
        """ filter based on locations

            Examples:

                .filter_location(Owls.isIn('radial'))
                .filter_location(Owls.isNotIn('radial'))

        """
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

    # ----------------------------------------------------------------------
    # Grouping methods

    def by_index(self, field, func=None):
        func = (func if func else lambda x: x)
        return self.by(field, func)

    def by_field(self, field, func=None):
        func = (func if func else lambda x: x)
        return self.by(field, func)

    def by_location(self, func=None):
        func = (func if func else lambda x: x)
        return self.by("Loc", func)

    def by_time(self, func=None):
        func = (func if func else lambda x: x)
        return self.by("Time", func)

    def by(self, name, func):
        ret = self.copy() # Too expensive ? pd.concat( [A, pd.DataFrame(s)], axis=1 )
        ret.properties = self.properties
        if self._is_idx(name):
            index_values = ret.index.get_level_values(name)
            ret["Group"] = index_values.map(func)
        else:
            ret["Group"] = ret[name].map(func)
        ret.set_index("Group", append=True, inplace=True)
        ret.reorder_levels(['Time', 'Loc', 'Pos', 'Group'])
        return ret

    # ----------------------------------------------------------------------
    # Compute methods

    def rolling_mean(self, y, x="Pos", n=10, weight=False):
        """ compute a rolling mean, returns a Series """

        lower = min(self[x])
        upper = max(self[x])
        delta = (upper-lower)/n

        bds = [(lower + i*delta, lower + (i+1)*delta)
                for i in range(n)]

        bins = {y:[
                self.filter(name=x, field=lambda x:  (l < x < u))[y].mean()
                for (l,u) in bds]}

        bins.update({x: [(l+u)/2.0 for (l,u) in bds]})

        return self.from_dict(bins,
                name="rl" + self.properties.name,
                plot_properties=self.properties.plot_properties,
                show_func="plot")

    def weighted_rolling_mean(self, y, x="Pos", n=10, weight=False):
        """ compute a rolling mean, returns a Series """

        lower = min(self[x])
        upper = max(self[x])
        delta = (upper-lower)/n

        bds = [(lower + i*delta, lower + (i+1)*delta)
                for i in range(n)]

        bins = {y: [
                np.average(
                    a=self.filter(name=x, field=lambda x:  (l < x < u))[y],
                    weights=self.filter(name=x, field=lambda x:  (l < x < u))[weight])
                for (l, u) in bds]}

        bins.update({x: [(l+u)/2.0 for (l,u) in bds]})

        return self.from_dict(bins,
                name="rl" + self.properties.name,
                plot_properties=self.properties.plot_properties,
                show_func="plot")

    def time_average(self, suffix="Avg", time_start=0.0):
        """ compute time average of fields """
        fs = self.after(time_start)
        ret = fs.mean(level=["Loc", "Pos"])
        latest = fs.latest
        ret.index = latest.index
        for c in self.columns:
            latest[c+suffix] = ret[c]
        return latest


