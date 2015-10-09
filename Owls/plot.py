import re

colored = ["aqua", "black", "blue", "fuchsia", "gray", "green",
           "lime", "maroon", "navy", "olive", "orange", "purple",
           "red", "silver", "teal", "yellow"]

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


def adjustRow(style, whereRow, whereFigs=None, rows=None):
    """ adjusts a list of figures to given geometry """
    for f in where(figs):
        for key, value in style.items():
            if '.' in key:
                _ = key.split('.')
                f = getattr(f, _[0])
                key = _[1]
            setattr(f, key, value)
    return figs


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


def figure():
    import bokeh.plotting as bk
    return bk.figure()


def merge(*args, **kwargs):
    import bokeh.plotting as bk
    figure = (bk.figure() if not kwargs.get('figure', False) else
              kwargs.get('figure'))
    y = kwargs.get('y', None)
    x = kwargs.get('x', 'Pos')
    try:
        kwargs.pop('y')
        kwargs.pop('x')
    except:
        pass
    y = (y if type(y) == list else [y]*len(args))  # FIXME do the same for x
    kwargs.pop('figure')
    legend = kwargs.get('legend')
    if legend:
        kwargs.pop('legend')
    for yi, p in zip(y, args):
        if legend:
            kwargs.update({'legend': p.properties.name})
        override_color = p.properties.plot_properties.properties.get('Color', False)
        color = (override_color if override_color else next(kwargs["colors"]))
        p.show(x=x, y=yi, color=color, symbol=next(kwargs["symbols"]), figure=figure, **kwargs)
    return figure


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
    y = kwargs.get('y', None)
    x = kwargs.get('x', 'Pos')
    if kwargs.get('legend'):
        legend = kwargs.get('legend')
        kwargs.pop('legend')
    else:
        legend = False
        kwargs.pop('legend')
    plots = []
    c = args[0]
    # go through all items to be plotted
    items = (
        ((name, data) for name, data in c.items() if name in kwargs['order'])
        if kwargs.get('order', False) else c.items()
    )
    for nr, (name, data) in enumerate(items):
        sub_plots = [data]
        colors = next_color()
        symbols = next_symbol()
        figure = bk.figure()
        for c_ in args[1:]:
            # and through all sets to be plotted
            for name_, plot_ in c_.items():
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
                    # select by name in order list
                    if name_ == name:
                        sub_plots.append(plot_)
        for kw in ['x', 'y']:
            try:
                kwargs.pop(kw)
            except:
                pass
        if kwargs.get('legend_pos', 0) != nr:
            legend = False
        title = (kwargs.get('titles')[nr] if kwargs.get('titles', False) else name)
        plots.append(merge(
            *sub_plots, x=x, y=y,
            title=title, colors=colors,
            symbols=symbols, figure=figure,
            legend=legend, **kwargs))
    return plots


def plot_cases(cases, y, order, x='Pos', legend=True, **kwargs):
    from .FoamFrame import FoamFrame
    """ plot all cases in cases dict at specified locations
        and latest time step """
    elems = [x.latest.by_index('Loc') for x in cases.values() if type(x) is FoamFrame]
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
                 'plot_width': 900},
    'font': {'axis.axis_label_text_font_size': "14pt",
             #'legend.label_text_font_size': "10pt",
             #'axis.major_label_text_font_style': 'bold',
             #'axis.axis_label_text_font_style': 'bold'
             },
    'color': {"outline_line_color": "black"}
    }

multi_compose = partial(freduce, compose)
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

default_style = [size, font, color]

compose_styles = lambda x, y: multi_compose(x + y)

style = multi_compose(default_style)
