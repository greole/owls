import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy
import os
import shutil
import hashlib
from collections import Counter
import datetime

class Plot():
    ''' wrapper class around mpl
        supported styles: [classic, jet, wide, dcol, row]
    '''

    def __init__(self, geom=[1,1], leg=[0],
            style='classic',
            cmap=mpl.cm.gray,
            case="",
            figurename="figure",
            backupdir="",
            fileformat="eps",
            ):

        self.nx, self.ny = ((1,1) if not geom else (geom[0], geom[1]))
        self.leg = leg
        self.cmap = cmap
        self.style = style
        self.plots = []
        self.origins = []
        self.backupdir = backupdir
        self.case_dir = backupdir + case + "/"
        self.sets_dir = self.case_dir + "sets/"
        self.data_dir = self.sets_dir + figurename
        self.figurename = "{}{}.{}".format(self.case_dir,
                                        figurename,
                                        fileformat)
        time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
        self.figurename_date = "{}{}_at_{}.{}".format(self.case_dir,
                                        figurename,
                                        time,
                                        fileformat)
        self._create_backup_dir()

    def _create_backup_dir(self):
        try:
            os.makedirs(self.data_dir)
        except:
            pass

    def _md5sum(self, filename):
        """ compute md5sum of origin """
        md5 = hashlib.md5()
        with open(filename,'rb') as f: 
            for chunk in iter(lambda: f.read(128*md5.block_size), b''): 
                 md5.update(chunk)
        return md5.hexdigest()[:8]

    def objects(self):
        """ find all plot objects in self.plots """
        for p in self.plots:
            for name, item in p.iteritems():
                if name in ('x','y','z'):
                    yield item

    def backup_origin(self):
        """ copy origins to backup dest"""
        for obj in self.objects():
            origin = obj.origin
            try:
                file_hash = self._md5sum(origin)
                file_dest = "{}/{}_{}_{}".format(self.data_dir,
                        origin.split('/')[-1],
                        obj.name,
                        file_hash)
                shutil.copy2(origin, file_dest)
            except:
                pass

    def _savefig_and_origins(self):
        self.backup_origin()
        self.f.savefig(self.figurename)
        self.f.savefig(self.figurename_date)


    def add(self,
          **kwargs
        ):
        self.plots.append(kwargs)

    def create_plot_array(self):
        height = 4
        width = (2*height if self.style == "wide" else height)
        return  plt.subplots(self.ny, self.nx,
                    figsize=(self.nx*width, self.ny*height)
                    )

    def first_col(self, index):
        ''' return true if given subplot index is in first col'''
        return (True if (index) % self.nx == 0 else False)

    def last_col(self, index):
        ''' return true if given subplot index is in last col'''
        return (True if (index+1) % self.nx == 0 else False)

    def last_row(self, index):
        ''' return true if given subplot index is in last row'''
        return (True if index >=  self.nx * (self.ny-1) else False)

    def decorate_x(self, index):
        ''' returns true when ax is in last row or style is matrix '''
        if self.style == 'matrix':
            return True
        else:
            return (True if self.last_row(index) else False)

    def decorate_y(self, index):
        ''' returns true if ax is in first col or style is matrix '''
        if self.style == 'matrix':
            return True
        elif self.style in ('jet', 'dcol'):
            return self.first_col(index) or self.last_col(index)
        else:
            return self.first_col(index)

    def invert_x(self, index):
        ''' returns true for jet style if plot is on left side'''
        if self.style == 'jet':
            return self.first_col(index)
        else:
            return False

    def mirror_label(self, index):
        ''' true if in jet and dcol mode and on last col '''
        if self.style in ('jet', 'dcol') :
            return self.last_col(index)
        else:
            return False

    def add_legend(self, index):
        ''' adds a legend if requested '''
        return (True if index in self.leg else False)


    def ax_labels(self):
        ''' create a list of ax labels for every plot '''
        self.xlabels = ['no label' for i in range(self.nx*self.ny)]
        self.ylabels = ['no label' for i in range(self.nx*self.ny)]
        self.xranges = [(0, 1) for i in range(self.nx*self.ny)]
        self.yranges = [(0, 1) for i in range(self.nx*self.ny)]
        for plot in self.plots:
            plot_index = plot.get('subplot',0)
            try:
                self.xlabels[plot_index] = plot['x'].label
                self.ylabels[plot_index] = plot['y'].label
                self.xranges[plot_index] = plot['x'].data_range
                self.yranges[plot_index] = plot['y'].data_range
            except:
                 self.xlabels[plot_index] = "None"
                 self.ylabels[plot_index] = "None"

    def iterate_axis(self):
        if type(self.ax) != numpy.ndarray:
            yield 0, self.ax[0]
        else:
            axs = self.ax.flatten()
            for i, a in enumerate(axs):
                yield i, a

    def decorate_axis(self):
        st = self.style
        for index, a in self.iterate_axis():
            self.add_legend(index)
            if self.decorate_y(index):
                a.set_ylabel(self.ylabels[index]) # move to decorate func
                if self.mirror_label(index):
                    a.yaxis.set_ticks_position("right")
                    a.yaxis.set_label_position("right")
            else:
                a.set_yticklabels([])
            if self.decorate_x(index):
                a.set_xlabel(self.xlabels[index]) # move to decorate func
            else:
                a.set_xticklabels([])
            x_range = self.xranges[index]
            if self.invert_x(index):
                a.set_xlim(x_range[1], x_range[0])
            else:
                a.set_xlim(x_range[0], x_range[1])
            y_range = self.yranges[index]
            a.set_ylim(y_range[0], y_range[1])
            a.locator_params(nbins=10)
            a.grid(True)

    def draw(self, plot):
        style = plot.get('plot_type', 'scatter')
        x = plot['x']
        y = plot['y']
        z = plot.get('z', False)
        l = (plot.get('name') if plot.get('name',False) else "None")
        i = plot.get('subplot', 0)
        s = plot.get('symbol', '.')
        c = plot.get('color', False)


        if s in ['o', '.', ',', '+', 'x' ]:
            style = "scatter"
        else:
            style = "plot"

        if style == 'scatter' and type(z) is not bool:
            return self.ax[i].scatter(x, y, c=z, s=40, cmap=self.cmap,
                                     marker='.', lw=0, label=l)

        elif style == 'scatter' and not z:
            return self.ax[i].scatter(x, y, s=40, marker=s,
                                 lw=2, label=l, facecolors='none')

        if not style == 'scatter':
            if c:
                return self.ax[i].plot(x, y, label=l, lw=3, linestyle=s, color=c)
            else:
                return self.ax[i].plot(x, y, label=l, lw=3, linestyle=s)


    def show(self):
        self.f, ax = self.create_plot_array()
        try:
            self.ax = ax.flatten()
        except:
            self.ax = [ax]
        self.ax_labels()
        self.decorate_axis()
        for plot in self.plots:
            self.draw(plot)
        for i, ax in self.iterate_axis():
            if self.add_legend(i):
                ncol = (1 if len(self.plots)/len(self.ax) < 3 else 2)
                ax.legend(ncol=ncol)
        if self.backupdir:
            self._savefig_and_origins()

    def zoom(self, subplot=0, x=None, y=None):
        if x:
            self.ax[subplot].set_xlim(x[0],x[1])
        if y:
            self.ax[subplot].set_ylim(y[0],y[1])

    def annotate(self, subplot=0, annotation="", position="ul", x=False, y=False):
        """ add an annotation to a subplot """
        posx = (x if x else max(self.ax[subplot].get_xlim())*0.2)
        posy = (y if y else max(self.ax[subplot].get_ylim())*0.8)
        self.ax[subplot].annotate(annotation,
            xytext=(posx, posy),
            xy=(posx, posy),
            )


    def pci_style(self):
        plt.rcParams.update({'font.size': 14, 'family': 'Helvetica'})
        plt.rcParams.update({'weight': 'bold'})
        plt.rcParams.update({'axes.linewidth': 2.0})
        plt.rcParams.update({'axes.titlesize': 'medium'})
        plt.rcParams.update({'figure.subplot.hspace': 0.1,})
        plt.rcParams.update({'figure.subplot.wspace': 0.1,})
        plt.rcParams.update({'axes.labelweight': 'medium'})
        plt.rcParams.update({'legend.scatterpoints': 1})
        plt.rcParams.update({'legend.numpoints': 1})
        plt.rcParams.update({'axes.color_cycle': ['k']})

    def color_style(self):
        plt.rcParams.update({'font.size': 14, 'family': 'Helvetica'})
        plt.rcParams.update({'weight': 'bold'})
        plt.rcParams.update({'axes.linewidth': 2.0})
        plt.rcParams.update({'axes.titlesize': 'medium'})
        plt.rcParams.update({'figure.subplot.hspace': 0.1,})
        plt.rcParams.update({'figure.subplot.wspace': 0.1,})
        plt.rcParams.update({'axes.labelweight': 'medium'})
        plt.rcParams.update({'legend.scatterpoints': 1})
        plt.rcParams.update({'legend.numpoints': 1})
        plt.rcParams.update({'axes.color_cycle': ['k','r', 'g', 'b', 'y','c', 'm']})

def intToColor(i, itot=4):
    cmap = mpl.cm.jet  # I set colomap to 'jet'
    norm = mpl.colors.Normalize(vmin=0, vmax=itot)
    return cmap(norm(i))


def add_colorbar(data, cs, f):
        cb = f.colorbar(cs, pad=0.05)
        cb.set_label(data.get('z_label', 'None'))


def makeHistogram(Series, nbins=50, limits=[], labels=[], legends=[]):
    plt.rcParams.update({'font.size': 18})
    plt.rcParams.update({'family': 'Helvetica'})
    plt.rcParams.update({'weight': 'bold'})

    f, ax = plt.subplots(1, 1, figsize=(15, 6))
    for i, serie in enumerate(Series):
        count, bins = np.histogram(serie, bins=nbins)
        cs = ax.plot(bins, count)
    ax.set_xlim(lim[0], lim[1])
    ax.set_ylim(lim[2], lim[3])
    ax.set_xlabel(title[0])
    ax.set_ylabel(title[1])
    ax.locator_params(nbins=8)
    return f, ax


def fenceAve(serie):
    avg = []
    for i in range(len(serie)-1):
        avg.append((serie[i]+serie[i+1])/2)
    return avg


def get_data(data, time, log, x):
    data_type = x[4]
    base_file = x[2]
    data_loc = x[3]
    if log:
        try:
            d = data[data_type][base_file]
            return d
        except:
            print "trying to acess {} {}".format(base_file, data_loc)
            return 0
    else:
        d = data[data_type][time]['{}_{}'.format(base_file, data_loc)]
        return d


def plot_dict_histogram(data, name, x, legend="", time=False, nbins=100):
    set_ = x[4]
    if not time:
        time = str(max(data[name][set_].keys()))

    id_ = name + legend

    data_ = '{}_{}'.format(x[2],x[3])
    count, bins = np.histogram(data[name][set_][time][data_],
                               bins=nbins, density=True,
                              )

    dict_ = {id_: {'x': fenceAve(bins),
                   'y': count,
                   'x_label': x[0],
                   'y_label': 'density',
                   'x_lim': x[1],
                   'y_lim': [0,1.1*max(count)],
                   }}
    dict_[id_]['plot_type'] = "plot"
    return dict_

def sort_by_pos(data, name, x, y, pos):
    setx = x[4]
    time = str(max(data[name][setx].keys()))
    datax = '{}_{}'.format(x[2],x[3])
    datay = '{}_{}'.format(y[2],y[3])
    data_m = '{}_-_{}'.format(x[2],x[3])
    data_p = '{}_+_{}'.format(x[2],x[3])

    data[name][setx][time][data_m] = data[name][setx][time][datax][ data[name][setx][time][datay] < pos]
    data[name][setx][time][data_p] = data[name][setx][time][datax][ data[name][setx][time][datay] > pos]

def calc_diff(name, x, y):
    setx = x[4]
    time = str(max(name[setx].keys()))
    datax = '{}_{}'.format(x[2],x[3])
    datay = '{}_{}'.format(y[2],y[3])
    data_diff = '{}diff{}_{}'.format(x[2],y[2],x[3])

    name[setx][time][data_diff] = name[setx][time][datax] - name[setx][time][datay]


def plot_dict_rhistogram(data, name, x, legend="", time=False, nbins=100):
    set_ = x[4]
    if not time:
        time = str(max(data[name][set_].keys()))

    id_ = name + legend

    data_ = '{}_{}'.format(x[2],x[3])
    count, bins = np.histogram(data[name][set_][time][data_],
                               bins=nbins, density=True,
                              )

    dict_ = {id_: {'y': fenceAve(bins),
                   'x': count,
                   'y_label': x[0],
                   'x_label': 'density',
                   'y_lim': x[1],
                   'x_lim': [0,1.1*max(count)],
                   }}
    dict_[id_]['plot_type'] = "plot"
    return dict_
