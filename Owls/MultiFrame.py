from __future__  import print_function
from future.builtins import *

from collections import OrderedDict
from . import  plot

class MultiFrame():
    """ Class for storage of multiple case items
        or faceted data from FoamFrame
    """
    #TODO:  implememt multi-facetting
    #       e.g. (cases.by_index('Loc')    <- returns a MultiFrame
    #               .by_case(overlay=True) <- MultiFrame method
    #               .show('T')
    #TODO: implement __repr__ method
    def __repr__(self):
        s = "MultiFrame with {} entries:\n".format(len(self.cases))
        s += "\n".join(["{}\n{}:\n{}".format(80*"=",name,c.describe())
            for name,c in self.cases.items()])
        return s

    def __init__(self, cases=None):
        if type(cases) == list:
            self.cases = OrderedDict([(case.name,case) for case in cases])
        elif type(cases) == OrderedDict:
            self.cases=cases
        else:
            self.cases={}

    def __getitem__(self, field):
        return [serie[field] for serie in self.cases.values()]

    def names(self):
        return [name for name in self.cases]

    def select(self, case):
        """ select a specific item """
        return self.cases[case]

    def filter(self, selector):
        """ select a specific item """
        if type(selector) == list:
            return MultiFrame({name:case for name,case in self.cases if
                            name in selector})
        else:
            return MultiFrame({name:case for name,case in self.cases if
                            func(name)})

    def items(self):
        for name, case in self.cases.items():
            yield name, case

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
            for name, instance in self.cases.items():
                figure=bk.figure()
                rows.append(
                        getattr(instance, inst_func)
                            (x=x, y=y, title=str(name),figure=figure, **kwargs) #FIXME num cars
                    )
            rows = np.array(rows).reshape(greatest_divisor(len(rows)),-1).tolist()
            return bk.GridPlot(children=rows, title="Scatter")
        else:
           figure=bk.figure()
           colors = plot.next_color()
           exp_legend = kwargs.get("legend", None)
           if exp_legend != None:
                kwargs.pop("legend")
           exp_title = kwargs.get("title", None)
           if exp_title != None:
                kwargs.pop("title")
           for name, instance in self.cases.items():
                color = next(colors)
                legend = (exp_legend if exp_legend != None else name)
                title = (exp_title if exp_title != None else "")
                getattr(instance, inst_func)(
                    x=x, y=y, title=title, color=color,
                    legend=legend, figure=figure, **kwargs)
           return figure
