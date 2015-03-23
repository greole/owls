import re

colored = ["aqua", "black", "blue", "fuchsia", "gray", "green",
            "lime", "maroon", "navy", "olive", "orange", "purple",
            "red", "silver", "teal", "yellow"]

white2black = [
     '#000000', '#0D0D0D', '#1A1A1A', '#262626', '#333333',
     '#404040', '#4C4C4C', '#595959', '#666666', '#737373',
     '#808080', '#8C8C8C', '#999999', '#A6A6A6', '#B2B2B2',
     '#BFBFBF', '#CCCCCC', '#D9D9D9', '#E6E6E6', '#F2F2F2',
     '#FFFFFF'][::-1]

config = {
    "color_cycle": colored,
    }

def CleanLabelRow(row):
    """ remove dublicate labels along a row """
    for figure in row[1:]:
        try:
            figure.y_axis.axis_label = False
        except:
            pass
    return row

def figure():
    import bokeh.plotting as bk
    return bk.figure()
    

def merge(*args, **kwargs):
    import bokeh.plotting as bk
    figure=(bk.figure() if not kwargs.get('figure', False) else
            kwargs.get('figure'))
    y = kwargs.get('y',None)
    x = kwargs.get('x','Pos')
    try:
        kwargs.pop('y')
        kwargs.pop('x')
    except:
        pass
    y = (y if type(y) == list else [y]*len(args)) #FIXME do the same for x
    kwargs.pop('figure')
    for yi,p in zip(y,args):
        p.show(x=x, y=yi, color=next(kwargs["colors"]), figure=figure, **kwargs)
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
    y = kwargs.get('y',None)
    x = kwargs.get('x','Pos')
    plots=[]
    c = args[0]
    # go through all items to be plotted
    items = (
        ((name,data) for name, data in c.items() if name in kwargs['order'])
        if kwargs.get('order',False) else c.items()
    )
    for name, data in items:
        sub_plots=[data]
        colors = next_color()
        figure=bk.figure()
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
                    #select by name in order list
                    if name_ == name:
                        sub_plots.append(plot_)
        plots.append(merge(*sub_plots, x=x, y=y, title=name, colors=colors,figure=figure))
    return plots

def next_color():
    from itertools import cycle
    for col in cycle(config['color_cycle']):
        yield col
