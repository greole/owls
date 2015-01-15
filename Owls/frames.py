import os
import re
import io
import shelve
import plot as plt
from collections import OrderedDict

from pandas import Series
from pandas import DataFrame
from pandas import concat

case_data_base = shelve.open(os.path.expanduser('~') + "/.owls/db")

def items_from_dict(dict, func, **kwargs):
    return Cases([func(folder=folder,name=name, symb=symb, **kwargs)
               for name, (folder,symb) in dict.iteritems()])

def read_sets(folder, name="None", search="./sets/{}/", **kwargs):
    return FoamFrame(folder=folder, search_files=False,
            search_pattern=search, name=name, show_func="plot", **kwargs)

def read_lag(folder, files, skiplines=1,
        name="None", cloud="coalCloud1", **kwargs
    ):
    return FoamFrame(folder=folder, search_files=files,
            search_pattern= "./{}/" + "lagrangian/{}/".format(cloud),
            name=name, skiplines=skiplines, show_func="scatter", **kwargs)

def read_eul(folder, files, skiplines=1, name="None", **kwargs):
    return FoamFrame(folder=folder, search_files=files,
            search_pattern="./{}/", name=name,
            skiplines=skiplines, show_func="scatter",
             **kwargs)

def read_exp(folder, name="None", **kwargs):
    #FIXME make it read exp/*dat directly without 0 folder
    return FoamFrame(folder=folder, search_files=False,
             search_pattern="./{}/", name=name, show_func="scatter", **kwargs)


def read_log(folder, keys, log_name='*log*', plot_properties=False):
    origins,df = io.import_logs(folder,keys)
    ff = FoamFrame(df)
    ff.properties=Props(
            origins=origins,
            name='LogFiles',
            plot_properties=plot_properties,
            folder=folder,
            times=[0],
            symb="-",
            show_func="plot",
            )
    return ff

def merge(*args, **kwargs):
    import bokeh.plotting as bk
    bk.figure()
    bk.hold()
    y = kwargs.get('y',None)
    x = kwargs.get('x','Pos')
    try:
        kwargs.pop('y')
        kwargs.pop('x')
    except:
        pass
    y = (y if type(y) == list else [y]*len(args)) #FIXME do the same for x
    for yi,p in zip(y,args):
        p.show(x=x, y=yi, color=next(kwargs["colors"]), **kwargs)
    return bk.curplot()

def multi_merge(*args, **kwargs):
    """ call merge for all args

        Examples:   mm=multi_merge(
                        sets1.latest.by_index('Loc'),
                        sets2.latest.by_index('Loc'),
                        by='[0-9]+',
                        x='Pos',
                        y='vMean'
                        order=[x-10,x+25])

    """
    import bokeh.plotting as bk
    y = kwargs.get('y',None)
    x = kwargs.get('x','Pos')
    plots=[]
    c = args[0]
    # go through all items to be plotted
    items = (
        ((name,data) for name, data in c.iteritems() if name in kwargs['order'])
        if kwargs.get('order',False) else c.iteritems()
    )
    for name, data in items:
        sub_plots=[data]
        colors = plt.next_color()
        for c_ in args[1:]:
            # and through all sets to be plotted
            for name_, plot_ in c_.iteritems():
                if not kwargs.get('order', False):
                    # select by regex
                    # now see if we have a match
                    selector = kwargs.get('by', "[A-Za-z0-9_\-]")
                    # skip if search is empty 
                    if (not re.search(selector, name) or
                        not re.search(selector, name_)):
                        continue
                    # append to subplot if same schema
                    if (re.search(selector, name).group()
                        == re.search(selector, name_).group()):
                        sub_plots.append(plot_)
                else:
                    #select by name in order list
                    if name_ == name:
                        sub_plots.append(plot_)
        plots.append(merge(*sub_plots, x=x, y=y, title=name, colors=colors))
    return plots

class MultiItem():
    """ Class for storage of multiple case items
        or faceted data from FoamFrame
    """
    #TODO:  implememt multi-facetting
    #       e.g. (cases.by_index('Loc')    <- returns a MultiItem
    #               .by_case(overlay=True) <- MultiItem method
    #               .show('T')
    #TODO: implement __repr__ method
    def __init__(self, cases=None):
        if type(cases) == list:
            self.cases = OrderedDict([(case.name,case) for case in cases])
        elif type(cases) == OrderedDict:
            self.cases=cases
        else:
            self.cases={}

    def __getitem__(self, field):
        return [serie[field] for serie in self.cases.itervalues()]

    def names(self):
        return [name for name in self.cases]

    def select(self, case):
        """ select a specific item """
        return self.cases[case]

    def filter(self, selector):
        """ select a specific item """
        if type(selector) == list:
            return MultiItem({name:case for name,case in self.cases if 
                            name in selector})
        else:
            return MultiItem({name:case for name,case in self.cases if 
                            func(name)})

    def iteritems(self):
        for name,case in self.cases.iteritems():
            yield name,case

    def by(self, overlay=True):
        """
            recursiv grouping function
            
            Examples:
            
                mi.by(overlay=True) -> { cat1_1:{cat2_1:FoamFrame1,
                                                 cat2_2:FoamFrame2,
                                                    ...            }
                                         cat1_2:{cat2_1:FoamFrame3,
                                                    ...            }
                                        }
                
                m1.by(overlay=False) -> { (cat1_1,cat2_1): FoamFrame1,
                                          (cat1_1,cat2_2): FoamFrame2,
                                            ...
                                        }
        
               needs .show() to check if self.data is recursive
        """
        pass

    def scatter(self, y, x='Pos', z=False, overlay=False, **kwargs):
        import bokeh.plotting as bk
        return self._draw(x, y, z=z, overlay=overlay,
                    inst_func="scatter", **kwargs)

    def plot(self, y, x='Pos', z=False, overlay=False, **kwargs):
        return self._draw(x, y, z=z, overlay=overlay,
                    inst_func="plot", **kwargs)

    def show(self, y, x='Pos', z=False, overlay=False, **kwargs):
        return self._draw(x, y, z=z, overlay=overlay,
                    inst_func="show", **kwargs)

    def _draw(self, x, y, z, overlay, inst_func, **kwargs):
        import bokeh.plotting as bk
        import numpy as np
        def greatest_divisor(number):
            if number == 1:
                return 1
            for i in reversed(range(number)):
                if number % i == 0:
                    return i
            else:
                return 1

        if not overlay:
            rows=[]
            for name, instance in self.cases.iteritems():
                bk.figure()
                rows.append(
                        getattr(instance, inst_func)
                            (x=x, y=y, title=name, **kwargs) #FIXME num cars
                    )
            rows = np.array(rows).reshape(greatest_divisor(len(rows)),-1).tolist()
            return bk.GridPlot(children=rows, title="Scatter")
        else:
           bk.hold()
           colors = plt.next_color()
           for name, instance in self.cases.iteritems():
                color = next(colors)
                getattr(instance, inst_func)(x=x, y=y, title="", color=color, legend=name, **kwargs)
           bk.hold(False)
           return bk.curplot()

class PlotProperties():

    def __init__(self):
        from collections import defaultdict
        self.properties = defaultdict(dict)

    def insert(self, field, properties):
        self.properties[field].update(properties)

    def select(self, field, prop, default=None):
        field = self.properties[field]
        if not field:
            return
        else:
            return field.get(prop, default)

class Props():

    def __init__(self, origins, name,
            plot_properties, folder, times, symb,show_func,):
        self.origins=origins
        self.name=name
        self.plot_properties=plot_properties
        self.folder=folder
        self.times=times
        self.latest_time = max(times)
        self.symb=symb
        self.show_func=show_func



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
      name = kwargs.get('name', 'None')
      symb = kwargs.get('symb', 'o')
      files = kwargs.get('search_files', None)
      properties = kwargs.get('properties', None)
      lines = kwargs.get('maxlines', 0)
      search = kwargs.get('search_pattern', "{}")
      folder = kwargs.get('folder', None)
      plot_properties = kwargs.get('plot_properties', None)
      show_func = kwargs.get('show_func', None)

      keys = [
          'skiplines',
          'name',
          'symb',
          'search_files',
          'properties',
          'maxlines',
          'search_pattern',
          'folder',
          'plot_properties',
          'show_func']

      for k in keys:
        try:
            kwargs.pop(k)
        except:
            pass

      #TODO explain what happens here 
      if folder == None:
           #super(FoamFrame, self).__init__(*args, **kwargs)
           DataFrame.__init__(self, *args, **kwargs)
      else:
           os.chdir(folder) #FIXME necessary for read in?
           if case_data_base.has_key(folder):
                print "re-importing ",
           else:
                print "importing ",
           print name + ": ",
           origins, data = io.import_foam_folder(
                       search_format=search,
                       file_names=files,
                       skiplines=skip,
                       maxlines=lines,
                  )
           DataFrame.__init__(self, data)
           self.properties = Props(
                origins,
                name,
                plot_properties,
                folder,
                # FIXME fix it for read logs
                data.index.levels[0],
                symb,
                show_func)
           self.validate_origins(folder, origins)
           # register to database
           case_data_base.sync()

    def validate_origins(self, folder, origins):
        if case_data_base.has_key(folder):
            if (case_data_base[folder]["hash"] == origins["hash"]):
                print " [consistent]"
            else:
                for time_key, time in origins.iteritems():
                    if time_key == "hash":
                        continue
                    if not case_data_base[folder].get(time_key, False):
                        print " [new timestep] " + str(time_key)
                    else:
                        print " [inconsistent]",
                        for loc_key, loc in time.iteritems():
                            if loc_key == "hash":
                                loc_hash = loc_key
                                continue
                            for field_key, files in loc['fields'].iteritems():
                                if field_key == "hash":
                                    field_hash = fields_key
                                    continue
                                if files[1] != case_data_base[folder][time_key][loc_key]['fields'][field_key][1]:
                                    # FIXME for all fields it prints that one column is corrupted
                                    print "corrupted: " + field_key + " in file: " +  files[0] 
                print "overwriting" 
                # TODO think what to do
                # raise an error, flag as dirty, backup old
                case_data_base[folder] = origins
        else:
             print "[stored]"
             case_data_base[folder] = origins

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
        ret =  "FoamFrame: \n" + super(FoamFrame,self).__str__()
        return ret

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
        ret = self.loc[[self.properties.latest_time]]
        ret.properties = self.properties
        return ret

    def at(self, idx_name, idx_val):
        """ select from foamframe based on index name and value"""
        ret = self[self.index.get_level_values(idx_name) == idx_val]
        ret.properties = self.properties
        return ret

    def id(self, loc):
        """ Return FoamFrame based on location """
        return self.at(idx_name='Id', idx_val=loc)

    def location(self, loc):#
        """ Return FoamFrame based on location """
        return self.at(idx_name='Loc', idx_val=loc)

    def loc_names(self, key):
        """ search for all index names matching keyword"""
        return [_ for _ in  self.index.get_level_values("Loc") if key in _]

    def field_names(self, key):
        """ search for all field names matching keyword"""
        return [_ for _ in  self.columns if key in _]

    def rename(self, search, replace):
        """ rename field names based on regex """
        import re
        self.columns = [re.sub(search, replace, name) for name in self.columns]


    def _is_idx(self, item):
        """ test if item is column or idx """
        return item in self.index.names

    def __getitem__(self, item):
        """ call pandas DataFrame __getitem__ if item is not
            an index
        """
        if self._is_idx(item):
            level = self.index.names.index(item)
            return zip(*self.index.values)[level]
        else:
           return super(FoamFrame, self).__getitem__(item)

    def draw(self, x, y, z, title, func, **kwargs):
        import bokeh.plotting as bk
        #TODO: change colors if y is of list type
        y = (y if type(y) == list else [y]) # wrap y to a list so that we can iterate

        kwargs.update({ "outline_line_color":"black", #FIXME refactor
                        "plot_width":300,
                        "plot_height":300,
                      })
        bk.hold(True)
        for yi in y:
            x_data, y_data = self[x], self[yi]
            func(x=x_data,
                 y=y_data,
                 title=title,
                 **kwargs)
        bk.hold(False)
        ret = bk.curplot()

        def _label(axis, field):
           label = kwargs.get(axis + '_label', False)
           if label:
               self.properties.plot_properties.insert(field, {'label':label})
           else:
               label = self.properties.plot_properties.select(field, 'label', "None")
           return label

        bk.xaxis().axis_label = _label('x', x)
        bk.yaxis().axis_label = _label('y', y[0]) #TODO can this make sense for multiplots?
        return ret

    def scatter(self, y, x='Pos', z=False, title="", **kwargs):
        import bokeh.plotting as bk
        return self.draw(x, y, z, title, func=bk.scatter, **kwargs)

    def plot(self, y, x='Pos', z=False, title="", **kwargs):
        import bokeh.plotting as bk
        return self.draw(x, y, z, title, func=bk.line, **kwargs)


    def show(self, y, x=None, **kwargs):
        if x:
            return getattr(self,self.properties.show_func)(y=y, x=x, **kwargs)
        else:
            return getattr(self,self.properties.show_func)(y=y, **kwargs)


    def filter(self, name, index=None, field=None):
        """ filter on index or field values by given functioni

            Examples:

                .filter(name='T', field=lambda x: 1000<x<2000)
                .filter(name='Loc', index=lambda x: 0.2<field_to_float(x)<0.8)
        """
        if index:
            ret = self[map(index,self.get_level_values(name))]
            ret.properties = self.properties
            return ret
        elif field:
            ret = self[map(field,self[name])]
            ret.properties = self.properties
            return ret
        else:
            return self

    def by_index(self, field, func=None):
        func = (func if func else lambda x: x)
        return self.by(field, index=func)


    def by_field(self, field, func=None):
        func = (func if func else lambda x: x)
        return self.by(field, field=func)

    def by(self, name, index=None, field=None):
        """ facet by given function

            Examples:

            .by(index=lambda x: x)
            .by(field=lambda x: ('T_high' if x['T'] > 1000 else 'T_low'))
        """
        if index:
            ret = OrderedDict(
                   [(index(val),self[self.index.get_level_values(name) == val])
                        for val in self.index.get_level_values(name)]
                  )
            for _ in ret.itervalues():
                _.properties = self.properties
            return MultiItem(ret)
        else:
            self['cat'] = map(field, self[name])
            cats = self.groupby('cat').groups.keys()
            ret =  OrderedDict(
                    [(cat,self[self['cat'] == cat]) for cat in cats]
                )
            for _ in ret.itervalues():
                _.properties = self.properties
            return MultiItem(ret)

    ############################################################################
    @property
    def vars(self):
        # if self.data.empty:
        #     return
        """ delete this methode and replace by columns ??"""
        print "This Method is obsolete and will be replaced by .columns"
        return self.columns

    # def __getitem__(self, field):
    #     try:
    #         print field
    #         return self.loc[self.latest_time][field]
    #     except Exception as e:
    #         print "%s Warning: requested field %s not in data base" %(self.name, field)
    #         print e
    #         return Series()
    
  #   def __str__(self):
  #       return """Foam case object
  # Data Fields: {}
  # Total number of items {} 
  # Data root: {}""".format(
  #   str([_ for _ in self.vars]), "unknown", self.folder)
                    
    # def reread(self):
    #     """ re-read foam data """ 
    #     self.origins, self.data = self._read_data()

