import os
import analysis as ana
from pandas import Series
from pandas import concat

#FIXME fix all the if self.data.empty tests

def items_from_dict(dict, func, **kwargs):
    return Cases([func(folder=folder,name=name, symb=symb, **kwargs)
               for name, (folder,symb) in dict.iteritems()])

def read_sets(folder, name="None", search="./sets/{}/", **kwargs):
    return Item(folder, search_files=False, search_pattern=search, name=name, **kwargs)

def read_lag(folder, files, skiplines=1, name="None", cloud="coalCloud1", **kwargs):
    return Item(folder, search_files=files,
            search_pattern= "./{}/" + "lagrangian/{}/".format(cloud),
            name=name, skiplines=skiplines, **kwargs)

def read_eul(folder, files, skiplines=1, name="None", **kwargs):
    return Item(folder, search_files=files, 
            search_pattern="./{}/", name=name, skiplines=skiplines, **kwargs)

def read_exp(folder, name="None",**kwargs):
    return Item(folder, search_files=False,
             search_pattern="./{}/", name=name, **kwargs)


def read_logs(folder, log_name='*log*', keys=None):
    os.chdir(folder)
    if keys:
        print "reading logs"
        return extractFromLog(keys, older, log_name)

class Cases():
    """ Class for storage of multiple case items """
    def __init__(self, cases=[]):
        self.cases = {case.name:case for case in cases}

    def __getitem__(self, field):
        return [serie[field] for serie in self.cases.itervalues()]

    def names(self):
        return [name for name in self.cases]

    def select(self, case):
        """ select a specific case """
        return self.cases[case]

class PlotProps():

    def __init__(self):
        from collections import defaultdict
        self.props = defaultdict(dict)

    def insert(self, field, props):
        self.props[field].update(props)

    def select(self,field, prop):
        field = self.props[field]
        if not field:
            return 
        else:
            return field.get(prop,False)

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
        self.times = [float(_) for _ in ana.find_times(self.folder)]
        self.skiplines = skiplines
        self.origins, self.data = self._read_data()
        self.categories = {}
        self.symb=symb

    def _read_data(self):
        """ call foam_to_DataFrame for all entries in read_list """
        search = self.search_pattern
        print self.name + ": ",
        origins, data = ana.import_foam_folder(search_format=search,
                                 file_names=self.search_files,
                                 skiplines=self.skiplines,
                                 maxlines=self.maxlines
                                 )
        #data['Case'] = self.name
        #data.set_index('Case', append=True, inplace=True)
        #data = data.reorder_levels(['Case','Time',0])
        return origins, data

    def add(self, data, label):
        """
        Add a given Series

        Usage:
        -------
        case.add(sqrt(uu),'u_rms')
        """
        time = max(self.data.keys())
        self.data[time][label] = data
        return self.data[time][label]

    def _column_to_file(self, time, col):
        """ find corresponding file for given time and column """
        for key, value in self.origins.iteritems():
            if time in key and col in key:
                    return value
        else:
            return "NONE"

    @property
    def latest_time(self):
        """ return latest time for case """
        return max(self.times)


    def iteratetimes(self, delta_t=0):
        """ iterator to iterate over all sets entries
            to create convergence check plots """
        for time in self.times:
            df = self.data.loc[float(time)]
            for col in df.columns:
                df[col].name = "{} @{:1.4}s".format(self.name, float(time))
            yield time, df

    def values_at_position(self, field, position):
        # if self.data.empty:
        #     return
        #FIXME
        times = Series()
        values = Series()
        field_ind = field.split('_')[0]
        for time, df in self.data.iteritems():
            val = df[field].where(df[field_ind] == position).dropna()
            times.append(Series(time))
            values.append(Series(val))
        return times, values


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

    def rename(self, search, replace):
        import re
        names = self.data.columns
        names = [re.sub(search,replace,name) for name in names]
        self.data.columns = names

    def _is_index(self, name):
        """ test if given column name is an index """
        _ = name.split('_')
        if len(_) == 1 or _[-1] == '0':
            return True
        else:
            return False

    def scatter(self, x, y, title="", rec_call=False, **kwargs):
        import bokeh.plotting as bk
        import numpy as np
        def greates_divisor(number):
            if number == 1:
                return 1
            for i in reversed(range(number)):
                if number % i == 0:
                    return i
            else:
                return 1

        if type(x) == dict:
            rows=[]
            for y_title, y_data in y.iteritems():
                x_data = x[y_title]
                rows.append(self.scatter(
                           x=x_data,
                           y=y_data,
                           title=y_title,
                           **kwargs)
                    )
            rows = np.array(rows).reshape(greates_divisor(len(rows)),-1).tolist()
            return bk.GridPlot(children=rows, title="Scatter") 
        else:
            if type(x) == str and type(y) == str:
                x = self.__getitem__(x)
                y = self.__getitem__(y)
            else:
                x=x
                y=y
            kwargs.update({ "outline_line_color":"black",
                            "plot_width":300,
                            "plot_height":300,
                          })
            return bk.scatter(x=x,
                       y=y,
                       title=title,
                       **kwargs)
    
 
    def plot(self, x, y, title="", **kwargs):
        import bokeh.plotting as bk
        if type(x) == str and type(y) == str:
            x = self.__getitem__(x)
            y = self.__getitem__(y)
        else:
            x=x
            y=y
        return bk.line(x=x,
                   y=y,
                   title=title,
                   plot_width =300,
                   plot_height=300,
                   xlabel="ffo",
                   **kwargs)

    def display(self, data_handler=None, title=False, plot=scatter, geom=[1,1]):
        rows=[]
        for i in geom[0]:
            cols=[]
            for j in geom[1]:
                x_data,y_data=next(data_handler)
                x = x_data.data
                y = y_data.data
                title = y_data.title
                cols.append(plot(x,y), title=title)
            row.append(cols)
        return GridPlot(children=rows)

    def data_handler(self, x="pos",y="u", facet="rad", filter_func=None):
        return 

    def _facet_by_name(self, regex, data=None):
        """ Return series seletected based on its name and given regex """
        import re
        data = (self.data if type(data) == type(None) else data)
        if type(data) == dict:
            return  { k:self._facet_by_name(regexp,inner_data) 
                        for k,inner_data in data.iteritems()}
        else:
            return {s:data[s] for s in data if re.match(regex,s)}

    def _facet_by_loc(self, loc, data=None, field=False):
        """ Return series seletected based on its name and given regex """
        data = (self.data if type(data) == type(None) else data)
        if type(data) == dict:
            return  { k:self._facet_by_loc(loc,inner_data) 
                        for k,inner_data in data.iteritems()}
        else:
            if field:
                return {val:data[data.index.get_level_values(loc) == val][field]
                        for val in data.index.get_level_values(loc)}   
            else:
                return { val:data[data.index.get_level_values(loc) == val] 
                        for val in data.index.get_level_values(loc)}   

    def select(self, field, latest_Time=True, data=None, **kwargs):
        from numpy import array
        from numpy import bitwise_and
        data = (self.data if type(data) == type(None) else data)
        if latest_Time:
            kwargs.update({'Time':self.latest_time})
        if not kwargs:
            return self.data[field]
        mask = [self.data.index.get_level_values(loc) == val 
                for loc, val in kwargs.iteritems()]
        mask = reduce(bitwise_and, mask)
        return self.data[mask][field]
    
    def facet_select(self, inp, field, **kwargs):    
        """ selected from dictionary """
        if type(inp) == dict:
           return [self.select(data=data,field=field)
                    for _,data in inp.iteritems()] 
        else:
           return self.select(field)

    def _facet_by_booleans(self, field, boolean):
        return None

    def _facet_by_category(self, category):
        """ returns position, categorie or False """
        from collections import defaultdict
        ret = defaultdict(list)
        cat_func = self.categories[category]
        for s in self.data:
            try: 
                r = cat_func(s)
                ret[r].append(self.data[s])
            except Exception as e:
                print e      
        return ret 
    
    def add_category(self, entry, func=False):
        if type(entry) == dict:
            self.category.update(entry)
        else:
            self.category[entry] = func


    ############################################################################
    @property
    def vars(self):
        # if self.data.empty:
        #     return
        """ delete this methode and replace by columns ??"""
        return self.data.columns

    def __getitem__(self, field):
        try:
            return self.data.loc[self.latest_time][field]
        except Exception as e:
            print "%s Warning: requested field %s not in data base" %(self.name, field)
            print e
            return Series()
    
    def __str__(self):
        return """Foam case object
  Data Fields: {}
  Total number of items {} 
  Data root: {}""".format(
    str([_ for _ in self.vars]), "unknown", self.folder)
                    
    def reread(self):
        """ re-read foam data """ 
        self.origins, self.data = self._read_data()

