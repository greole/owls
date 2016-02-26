# for snappy
import subprocess, os, json
from IPython.display import HTML, display
from glob import glob
import shutil

import numpy as np

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

colored = ["black", "blue", "fuchsia", "gray", "green",
           "lime", "maroon", "navy", "olive", "orange", "purple",
           "red", "silver", "teal", "yellow", "aqua"]

symbols_full = ["circle", "square", "triangle", "diamond", "inverted_triangle"]

white2black = [
    '#000000', '#0D0D0D', '#1A1A1A', '#262626', '#333333',
    '#404040', '#4C4C4C', '#595959', '#666666', '#737373',
    '#808080', '#8C8C8C', '#999999', '#A6A6A6', '#B2B2B2',
    '#BFBFBF', '#CCCCCC', '#D9D9D9', '#E6E6E6', '#F2F2F2',
    '#FFFFFF'][::-1]

config = {
    "color_cycle": colored,
    "symbol_cycle": symbols_full,
    }


class Gnuplot():


    def __init__(self, path):
        self.path = path


    def add_line(self, data, line_type, subplot):
        pass


    def write(self):
        """ write gnuplot file to disk """
        pass


def head(elems):
    return [elems[0]]


def tail(elems):
    return elems[1:]


def all(elems):
    return elems


def rtail(elems):
    return elems[:-1]


def last(elems):
    return [elems[-1]]


# def adjustRow(style, whereRow, whereFigs=None, rows=None):
#     """ adjusts a list of figures to given geometry """
#     for f in where(figs):
#         for key, value in style.items():
#             if '.' in key:
#                 _ = key.split('.')
#                 f = getattr(f, _[0])
#                 key = _[1]
#             setattr(f, key, value)
#     return figs

def adjustColumn(style, whereRow, whereFigs=None, rows=None):
    for row in whereRow(rows):
        row = (whereFigs(row) if whereFigs else row)
        for fig in row:
            for key, value in style.items():
                if '.' in key:
                    _ = key.split('.')
                    fig = getattr(fig, _[0])
                    key = _[1]
                setattr(fig, key, value)
    return rows


def figure(**kwargs):
    import bokeh.plotting as bk
    return bk.figure(tools=TOOLS, **kwargs)

def plot_cases(cases, y, order, x='Pos', legend=True, **kwargs):
    from .FoamFrame import FoamFrame
    """ plot all cases in cases dict at specified locations
        and latest time step """
    elems = [x.by_index('Loc') for x in cases.values() if type(x) is FoamFrame]
    return multi_merge(*elems, x=x, y=y, order=order, legend=legend, **kwargs)


def next_color():
    from itertools import cycle
    for col in cycle(config['color_cycle']):
        yield col


def next_symbol():
    from itertools import cycle
    for sym in cycle(config['symbol_cycle']):
        yield sym

# Themes

from functools import partial
from functools import reduce as freduce
from functional import compose


rcParams = {
    'fig_size': {'min_border': 12,
                 'plot_height': 350,
                 'plot_width': 300},
    'font': {'axis.axis_label_text_font_size': "14pt",
             #'legend.label_text_font_size': "10pt",
             #'axis.major_label_text_font_style': 'bold',
             #'axis.axis_label_text_font_style': 'bold'
             },
    'color': {"outline_line_color": "black"}
    }

multi_compose = partial(freduce, compose)
compose_styles = lambda x, y: multi_compose(x + y)

#axis_label_text_font_style, major_label_text_font_style or axis_label_text_font_size
#'min_border':12, 'plot_height': 350, 'plot_width': 350,
rowLabel = partial(
    adjustColumn,
    {'yaxis.visible': False},
    all, tail)

size = partial(adjustColumn, rcParams['fig_size'], all, all)
font = partial(adjustColumn, rcParams['font'], all, all)
color = partial(adjustColumn, rcParams['color'], all, all)

cleanTitle = partial(adjustColumn, {'title': ""}, tail, all)
cleanXAxis = partial(adjustColumn, {'xaxis.visible': False}, rtail, all)
cleanYAxis = partial(adjustColumn, {'yaxis.visible': False}, all, tail)


# reset legends
# all but last
cleanLegendIa = partial(adjustColumn, {'legend.legends': []}, rtail, all)
cleanLegendIb = partial(adjustColumn, {'legend.legends': []}, all, rtail)
cleanLegendIIa = partial(adjustColumn, {'legend.border_line_color': None}, all, rtail)
cleanLegendIIb = partial(adjustColumn, {'legend.border_line_color': None}, rtail, all)
cleanLegenda = partial(adjustColumn, {'legend.legends': []}, all, all)
cleanLegendb = partial(adjustColumn, {'legend.border_line_color': None}, all, all)
# all but first
cleanLegendIc = partial(adjustColumn, {'legend.legends': []}, all, tail)
cleanLegendId = partial(adjustColumn, {'legend.legends': []}, tail, all)
cleanLegendIIc = partial(adjustColumn, {'legend.border_line_color': None}, all, tail)
cleanLegendIId = partial(adjustColumn, {'legend.border_line_color': None}, tail, all)
cleanLegendb = partial(adjustColumn, {'legend.border_line_color': None}, all, all)

def legend(pos):
    return partial(adjustColumn, {'legend.orientation': pos}, all, all)

lastLegend = [cleanLegendIa, cleanLegendIb, cleanLegendIIa, cleanLegendIIb]
firstLegend = [cleanLegendIc, cleanLegendId, cleanLegendIIc, cleanLegendIId]
noLegend = [cleanLegenda, cleanLegendb]

legendTopLeft = legend("top_left")
legendBottomLeft = legend("bottom_left")
legendTopRight = legend("top_right")
legendBottomRight = legend("bottom_right")


lastLegend = [cleanLegendIa, cleanLegendIb, cleanLegendIIa, cleanLegendIIb]


arangement = lambda x: np.array(x).reshape(greatest_divisor(len(x)),-1).tolist()

default_style = [size, font, color]

def greatest_divisor(number):
    if number == 1:
        return 1
    for i in reversed(range(number)):
        if number % i == 0:
            return i
    else:
        return 1

style = multi_compose(default_style)
# snapshots


class Snappy():

    def __init__(self, path, config, out_path):
        self.path = path
        self.baseName = os.path.basename(self.path)
        self.config = config
        self.out_path = out_path
        self.snappy_path = os.path.dirname(__file__) + "/../scripts/snap.py"

    def generate(self, animate=False):
        old_dir = os.getcwd()
        os.chdir(self.path)
        args = " -d " if not animate else " -da --gif "
        cmd = "python {} {} --json_config=\'{}\' &".format(
              self.snappy_path, args, self.config)
        subprocess.check_call(cmd, shell=True)
        os.chdir(old_dir)

    def generate_image_list(self, animate=False, ext=".mp4"):
        images = []
        vals = json.loads(self.config)
        def appendr(images, prefix, extension):
            for s in vals["slices"].keys():
                for f in ["vectors", "scalars"]:
                    for v in vals[f].keys():
                        iname = self.baseName + "/" + prefix + s + v + extension
                        images.append(iname)
            return images

        if not animate:
            images = appendr(images, "last_", "_0.png")
            images = appendr(images, "last_", "_1.png")
            images = appendr(images, "last_", "_2.png")
        else:
            images = appendr(images, "", ext)
        self.images=images
        return images

    def copy_to_notebook(self):
        for p in [self.out_path, os.path.join(self.out_path, self.baseName)]:
            if not os.path.exists(p): os.makedirs(p)
        for ext in ["*.png", "*.mp4", "*.gif"]:
            for fn in glob(os.path.join(self.path + "/postProcessing/anim", ext)):
                    shutil.copy(fn, os.path.join(self.out_path, self.baseName))

    def display(self, size, media_type="mp4"):
        if media_type == "mp4":
            i = '<video width={} height="222" controls="controls"> <source src={} type="video/mp4" /></video>'
        else:
            i = "<img style='width: {}px; margin: 0px; float: left; border: 1px solid black;' src='{}' />"
        images = ''.join([i.format(size, s) for s in self.images])
        return display(HTML(images))
