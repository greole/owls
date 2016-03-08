# for snappy
import subprocess, os, json
from IPython.display import HTML, display
from glob import glob
import shutil
import bokeh.plotting as bk
from subprocess import call


import numpy as np

from itertools import cycle


class Bokeh():

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


    def figure(self, **kwargs):
        return bk.figure(tools=self.TOOLS, **kwargs)

    def draw(self, x, y, z, data, title, func, figure,
            legend_prefix="", titles=None, properties=None, **kwargs):
        # TODO Rename to _draw
        def _label(axis, field):
            label = kwargs.get(axis + '_label', False)
            if label:
                properties.plot_properties.insert(
                    field, {axis + '_label': label})
            else:
                label = properties.plot_properties.select(
                    field, axis + '_label', "None")
            return label

        def _range(axis, field):
            from bokeh.models import Range1d
            p_range_args = kwargs.get(axis + '_range', False)
            if p_range_args:
                properties.plot_properties.insert(
                    field, {axis + '_range': p_range})
            else:
                p_range = properties.plot_properties.select(
                    field, axis + '_range')
            if not p_range:
                return False
            else:
                return Range1d(start=p_range[0], end=p_range[1])

        figure_properties = {"title": title}

        if kwargs.get('x_range', False):
            figure_properties.update({"x_range": kwargs.get('x_range')})
        figure.set(**figure_properties)

        if func == "quad":
            getattr(figure, func)(
                    top=y, bottom=0, left=x[:-1], right=x[1:], **kwargs)
            return figure

        colors = self.next_color()
        spec_color = kwargs.get("color", False)
        spec_legend = kwargs.get("legend", False)

        # Iterate requested Data
        y = (y if isinstance(y, list) else [y])
        for yi in y:
            x_data, y_data = data[x], data[yi]
            # TODO FIXME
            for k in ['symbols', 'order', 'colors', 'symbol']:
                if k in kwargs.keys():
                    kwargs.pop(k)
            if not spec_color:
                kwargs.update({"color": next(colors)})
            if not spec_legend:
                # NOTE title overrides legend, does that make sense always?
                yi = (yi if not title else "")
                if yi and legend_prefix:
                    legend = legend_prefix + "-" + yi
                if not yi and legend_prefix:
                    legend = legend_prefix
                if not legend_prefix:
                    legend = yi

                kwargs.update({"legend": legend})

            getattr(figure, func)(x=x_data,
                                  y=y_data,
                                  **kwargs)

        # set axis ranges and labels
        for ax, data in {'x': x, 'y': y[0]}.items():
            if _label(ax, data):
                getattr(figure, ax+'axis')[0].axis_label = _label(ax, data)
            # setattr(getattr(figure, ax + 'axis'),
            #         'axis_label', _label(ax, data))
            if _range(ax, data):
                r = setattr(figure, ax+'_range', _range(ax, data))

        return figure


    def GridPlot(self, row, filename, arangement, show):
        gp = bk.GridPlot(
                children=style(rows=arangement(list(row.values()))))

        # plotinterface.show
        if filename:
            bk.save(gp, filename)
        if show:
            return bk.show(gp)
        else:
            return gp

    def next_color(self):
        for col in cycle(self.config['color_cycle']):
            yield col


    def next_symbol(self):
        for sym in cycle(self.config['symbol_cycle']):
            yield sym

intersperse = lambda e,l: sum([[x, e] for x in l],[])[:-1]

class GnuplotFigure():

    def __init__(self, **kwargs):
        self.x = []
        self.y = []
        self.lt = []

        self.x_label = "None"
        self.y_label = "None"

        self.x_range = [None, None]
        self.y_range = [None, None]

        self.lw = 2
        self.title = "TEST"
        self.legends = []

    def add(self, x, y, legend, lt, plotProperties):
        self.legends.append(legend)
        self.x.append(x)
        self.y.append(y)
        self.lt.append(lt)


    @property
    def xrange(self):
        if list(map(lambda x: x != None, self.x_range))[0]:
            return self.x_range
        else:
            return [min([min(x) for x in self.x]),
                    max([max(x) for x in self.x])]

    @property
    def yrange(self):
        if list(map(lambda x: x != None, self.y_range))[0]:
            return self.y_range
        else:
            return [min([min(y) for y in self.y]),
                    max([max(y) for y in self.y])]

class GnuplotMultiplot():
    # data is a OrderedDict of the form
    # {"id": [ GnuplotDataSet  ]}
    # self.data = OrderedDict()
    def __init__(self, data, filename):

        self.filename = filename

        n_sub_figs = len(data.items())
        n_sub_figs = (greatest_divisor(n_sub_figs), n_sub_figs/greatest_divisor(n_sub_figs))
        with open(filename + "-svg.gp", 'w+') as f:
            f.write(self.header(".svg").format(
                300*n_sub_figs[1],
                250*n_sub_figs[0],
                os.path.basename(filename)))
            self.write_body(data, f, n_sub_figs)

        with open(filename + ".gp", 'w+') as f:
            f.write(self.header(".eps").format(
                7.5*n_sub_figs[1],
                5.75*n_sub_figs[0],
                os.path.basename(filename)))
            self.write_body(data, f, n_sub_figs)


        os.system("cd " + os.path.dirname(filename) + "; gnuplot " + os.path.basename(filename) + "-svg.gp")
        os.system("cd " + os.path.dirname(filename) + "; gnuplot " + os.path.basename(filename) + ".gp")

    def header(self, ext):
        if ext == ".svg":
            # return "set terminal svg enhanced size {}, 250\nset output '{}.svg'\n"
            return "set terminal svg enhanced size {}, {} fname 'Arial bold'\nset output '{}.svg'\n"
        if ext == ".eps":
            # return "set terminal epslatex color size {}cm, 5.75cm \nset out '{}.eps'\n"
            return "set terminal epslatex color size {}cm, {}cm ',bx'\nset out '{}.eps'\n"


    def write_body(self, data, f, n_sub_figs):
            f.write("set multiplot layout {},{} \n".format(*n_sub_figs))
            f.write("set border 31 lw 2\n")
            for pid, d in data.items():
                for i, (x, y) in enumerate(zip(d.x, d.y)):
                    f.write("${}_{} << EOD\n".format(pid, i))
                    x_ = (x if isinstance(x,tuple) else x.values)
                    y_ = y.values
                    for i in range(len(x)):
                        f.write("{} {} \n".format(x_[i], y_[i]))
                    f.write("EOD\n")

            for pid, d in data.items():
                f.write("\nset xrange [{}: {}]\n".format(d.xrange[0], d.xrange[1]))
                f.write("\nset yrange [{}: {}]\n".format(d.yrange[0], d.yrange[1]))
                f.write("\nset xlabel \"{}\" offset 0,0.5 \n".format(d.x_label))
                f.write("\nset ylabel \"{}\" offset 2.5,0 \n".format(d.y_label))
                f.write("\nplot ")
                data_blocks = [" ${}_{} title '{}' w l lw 2 dashtype {}".format(pid, i, l, i+1)
                                for i, l in enumerate(d.legends)]
                f.write("".join(intersperse(", ", data_blocks)))
            f.write("\nunset multiplot")

    def _repr_svg_(self):
        return open(self.filename + ".svg", 'r').read()


    # def _repr_latex_(self):
    #     import IPython
    #     return IPython.display.Latex(filename = self.filename + ".tex")

class Gnuplot():

    # example colors
    # https://www2.uni-hamburg.de/Wiss/FB/15/Sustainability/schneider/gnuplot/colors.htm
    colored = ['#0072bd', '#d95319', '#edb120',
               '#7e2f8e', '#77ac30', '#4dbeee',
               '#a2142f']

    def figure(self, **kwargs):
        return GnuplotFigure(**kwargs)

    def draw(self, x, y, z, data, title, func,
            figure, legend_prefix="", titles=None,
            properties=None, **kwargs):
        """ takes a figure and draws data to it """
        # print("draw", x, y, z, title, func, figure, legend_prefix, titles)
        # TODO merge with bokeh methods
        def _label(axis, field):
            label = kwargs.get(axis + '_label', False)
            if label:
                properties.plot_properties.insert(
                    field, {axis + '_label': label})
            else:
                label = properties.plot_properties.select(
                    field, axis + '_label', "None")
            return label

        def _range(axis, field):
            Range1d = []
            p_range_args = kwargs.get(axis + '_range', False)
            if p_range_args:
                properties.plot_properties.insert(
                    field, {axis + '_range': p_range})
            else:
                p_range = properties.plot_properties.select(
                    field, axis + '_range')
            if not p_range:
                return False
            else:
                Range1d.append(p_range[0])
                Range1d.append(p_range[1])
                return Range1d

        # Iterate requested Data
        y = (y if isinstance(y, list) else [y])
        for yi in y:
            x_data, y_data = data[x], data[yi]

            figure.add(x=x_data, y=y_data,
                    legend=legend_prefix + properties.name,
                    lt=func, plotProperties=properties.plot_properties)


        # set axis ranges and labels
        for ax, data in {'x': x, 'y': y[0]}.items():
            if _label(ax, data):
                setattr(figure, ax+'_label', _label(ax, data))
            # setattr(getattr(figure, ax + 'axis'),
            #         'axis_label', _label(ax, data))
            if _range(ax, data):
                r = setattr(figure, ax+'_range', _range(ax, data))

        return figure

    def GridPlot(self, row, filename, arangement, show):
        return GnuplotMultiplot(row, filename)

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


# def plot_cases(cases, y, order, x='Pos', legend=True, **kwargs):
#     from .FoamFrame import FoamFrame
#     """ plot all cases in cases dict at specified locations
#         and latest time step """
#     elems = [x.by_index('Loc') for x in cases.values() if type(x) is FoamFrame]
#     return multi_merge(*elems, x=x, y=y, order=order, legend=legend, **kwargs)



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
