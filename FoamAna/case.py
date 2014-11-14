import os
import analysis as ana
import plot as plt

from pandas import Series
from pandas import DataFrame
from pandas import concat


def items_from_dict(dict, func, **kwargs):
    return Cases([func(folder=folder,name=name, symb=symb, **kwargs)
               for name, (folder,symb) in dict.iteritems()])

def read_sets(folder, name="None", search="./sets/{}/", **kwargs):
    return FoamFrame(folder=folder, search_files=False, search_pattern=search, name=name, **kwargs)

def read_lag(folder, files, skiplines=1, name="None", cloud="coalCloud1", **kwargs):
    return FoamFrame(folder=folder, search_files=files,
            search_pattern= "./{}/" + "lagrangian/{}/".format(cloud),
            name=name, skiplines=skiplines, **kwargs)

def read_eul(folder, files, skiplines=1, name="None", **kwargs):
    return FoamFrame(folder=folder, search_files=files, 
            search_pattern="./{}/", name=name, skiplines=skiplines, **kwargs)

def read_exp(folder, name="None",**kwargs):
    #FIXME make it read exp/*dat directly without 0 folder
    return FoamFrame(folder=folder, search_files=False,
             search_pattern="./{}/", name=name, **kwargs)


def read_log(folder, keys, log_name='*log*', plot_properties=False):
    origins,df = ana.import_logs(folder,keys)
    ff = FoamFrame(df)
    ff.properties=Props(
            origins=origins,
            name='LogFiles',
            plot_properties=plot_properties,
            folder=folder,  
            times=[0],
            symb="-")
    return ff
    

class MultiItem():
    """ Class for storage of multiple case items 
        or faceted data from FoamFrame    
    """
    def __init__(self, cases=None):
        if type(cases) == list:
            self.cases = {case.name:case for case in cases}
        elif type(cases) == dict:
            self.cases=cases
        else:
            self.cases={}

    def __getitem__(self, field):
        return [serie[field] for serie in self.cases.itervalues()]

    def names(self):
        return [name for name in self.cases]

    def select(self, case):
        """ select a specific case """
        return self.cases[case]

    def scatter(self, y, x='Pos', z=False, overlay=False, **kwargs):
        import bokeh.plotting as bk
        return self.draw(x, y, z=z, overlay=overlay, inst_func="scatter", **kwargs)

    def plot(self, y, x='Pos', z=False, overlay=False, **kwargs):
        return self.draw(x, y, z=z, overlay=overlay, inst_func="plot", **kwargs)

    def draw(self, x, y, z, overlay, inst_func, **kwargs):
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
                rows.append(
                        getattr(instance, inst_func)(x=x, y=y, title=name, **kwargs)
                    )
            rows = np.array(rows).reshape(greatest_divisor(len(rows)),-1).tolist()
            return bk.GridPlot(children=rows, title="Scatter") 
        else:
           bk.hold()
           colors = plt.next_color()
           for name, instance in self.cases.iteritems():
                color = next(colors)
                getattr(instance, inst_func)(x=x, y=y, title="", color=color, **kwargs)


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

    def __init__(self, origins, name, plot_properties, folder, times, symb):
        self.origins=origins
        self.name=name
        self.plot_properties=plot_properties
        self.folder=folder
        self.times=times
        self.latest_time = max(times)
        self.symb=symb



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

      skip = kwargs.get('skiplines',1)
      name = kwargs.get('name','None')
      symb = kwargs.get('symb','o')
      files = kwargs.get('search_files',None)
      properties = kwargs.get('properties',None)
      lines = kwargs.get('maxlines',0)
      search = kwargs.get('search_pattern',"{}")
      folder = kwargs.get('folder',None)
      plot_properties = kwargs.get('plot_properties',None)

      keys = [
          'skiplines',
          'name',
          'symb',
          'search_files',
          'properties',
          'maxlines',
          'search_pattern',
          'folder',
          'plot_properties']

      for k in keys:
        try:
            kwargs.pop(k)  
        except:
            pass

      if folder == None:
           #super(FoamFrame, self).__init__(*args, **kwargs)   
           DataFrame.__init__(self, *args, **kwargs)
      else: 
           os.chdir(folder) #FIXME necessary for read in?
           print name + ": ",
           origins, data = ana.import_foam_folder(
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
                symb)


    def add(self, data, label):
        """
        Add a given Series

        Usage:
        -------
        case.add(sqrt(uu),'u_rms')
        """
        self.latest[label] = data
        return self

    def source(self,):
        """ find corresponding file for given time and column """
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
    def latest_time(self):
        """ return latest time for case """
        return max(self.times)

    @property
    def latest(self):
        """ return latest time for case """
        ret = self.loc[[self.properties.latest_time]]
        ret.properties = self.properties
        return ret

    def location(self, loc):
        """ Return FoamFrame based on location """
        ret = self[self.index.get_level_values("Loc") == loc]
        ret.properties = self.properties
        return ret

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


    def draw(self, x, y, z, title, func, **kwargs):
        import bokeh.plotting as bk
        kwargs.update({ "outline_line_color":"black",
                        "plot_width":300,
                        "plot_height":300,
                      })
        x_data, y_data = self[x], self[y]
        ret = func(x=x_data,
                   y=y_data,
                   title=title,
                   **kwargs)

        def _label(axis, field):
           label = kwargs.get(axis + '_label', False)
           if label:
               self.properties.plot_properties.insert(field, {'label':label})
           else:
               label = self.properties.plot_properties.select(field, 'label', "None")
           return label
        
        bk.xaxis().axis_label = _label('x', x)
        bk.yaxis().axis_label = _label('y', y)
        return ret

    def scatter(self, y, x='Pos', z=False, title="", **kwargs):
        import bokeh.plotting as bk
        return self.draw(x, y, z, title, func=bk.scatter, **kwargs)
    
    def plot(self, y, x='Pos', z=False, title="", **kwargs):
        import bokeh.plotting as bk
        return self.draw(x, y, z, title, func=bk.line, **kwargs)

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
            ret = {index(val):self[self.index.get_level_values(name) == val] 
                        for val in self.index.get_level_values(name)}   
            for _ in ret.itervalues():
                _.properties = self.properties
            return MultiItem(ret)
        else:
            self['cat'] = map(field, self[name])
            cats = self.groupby('cat').groups.keys()
            ret =  {cat:self[self['cat'] == cat] for cat in cats}
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

