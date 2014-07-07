import os
import analysis as ana

def read_sets(folder, plot_props, name="None"):
    return Item(folder, search_files=False, search_pattern="./sets/{}/",
            plot_props=plot_props, name=name)

def read_lag(folder, files, plot_props, skiplines=1,
            name="None", cloud="coalCloud1"):
    return Item(folder, search_files=files,
            search_pattern= "./{}/" + "lagrangian/{}/".format(cloud),
            plot_props=plot_props, name=name, skiplines=skiplines)

def read_eul(folder,  files, plot_props, skiplines=1, name="None"):
    return Item(folder, search_files=files, search_pattern="./{}/",
            plot_props=plot_props, name=name, skiplines=skiplines)

def read_exp(folder, plot_props, name="None"):
    return Item(folder, search_files=False, plot_props=plot_props,
            search_pattern="./{}/", name=name)


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
                ):

        self.plot_props = plot_props
        self.folder = folder
        self.name = name
        os.chdir(folder)
        self.search_files=search_files
        self.search_pattern=search_pattern
        self.times = ana.find_times(self.folder)
        self.skiplines = skiplines
        self.origins, self.data = self._read_data()
        self.append_plot_props()

    def _read_data(self):
        """ call foam_to_DataFrame for all entries in read_list """
        search = self.search_pattern
        origins, data = ana.foam_to_DataFrame(search_format=search,
                                 file_names=self.search_files,
                                 plot_props=self.plot_props,
                                 skiplines=self.skiplines
                                 )
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
        latest_time = max(self.data.keys())
        return latest_time

    def iteratetimes(self, delta=0):
        """ iterator to iterate over all sets entries
            to create convergence check plots """
        for time, df in self.data.iteritems():
            for col in df.columns:
                df[col].name = "{} @{:1.4}s".format(self.name, float(time))
            yield time, df

    ############################################################################

    def __getitem__(self, field):
        return self.data[self.latest_time][field]

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

