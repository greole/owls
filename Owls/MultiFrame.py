from __future__ import print_function
from future.builtins import *

from collections import OrderedDict
from itertools import cycle

NumberTypes = (int, float, complex)


from .FoamFrame import FoamFrame, rcParams


def multiframes(folder, names, reader, **kwargs):
    """ create a collection of cases for which
        only the folder is different """
    return MultiFrame([reader(f, name=n, **kwargs)
                       for (f, n) in zip(folder, names)])


class MultiFrame():
    """ Class for storage of multiple case items
        or faceted data from FoamFrame
    """

    @staticmethod
    def from_dict(input_dict, **kwargs):
        return MultiFrame(
                cases=[FoamFrame.from_dict(d, name=name, **kwargs)
                        for name, d in input_dict.items()]
                )

    def __mul__(self, other):
        ''' multiply self with other, e.g. Foo() * 7 '''
        if isinstance(other, NumberTypes):
            return MultiFrame(OrderedDict([(i, c.__mul__(other))
                        for i, c in self.cases.items()]))
        else: # MultiFrame
            return MultiFrame(OrderedDict([(i, c.__mul__(other.cases[i]))
                        for i, c in self.cases.items()]))



    def __rmul__(self, other):
        ''' multiply other with self, e.g. 7 * Foo() '''
        if isinstance(other, NumberTypes):
            return MultiFrame(OrderedDict([(i, c.__rmul__(other))
                        for i, c in self.cases.items()]))
        else: # MultiFrame
            return MultiFrame(OrderedDict([(i, c.__rmul__(other.cases[i]))
                        for i, c in self.cases.items()]))

    def __truediv__(self, other):
        ''' multiply self with other, e.g. Foo() * 7 '''
        if isinstance(other, NumberTypes):
            return MultiFrame(OrderedDict([(i, c.__truediv__(other))
                        for i, c in self.cases.items()]))
        else: # MultiFrame
            return MultiFrame(OrderedDict([(i, c.__rtruediv__(other.cases[i]))
                    for i, c in self.cases.items()]))

    def __rtruediv__(self, other):
        ''' multiply self with other, e.g. Foo() * 7 '''
        if isinstance(other, NumberTypes):
            return MultiFrame(OrderedDict([(i, c.__rtruediv__(other))
                    for i, c in self.cases.items()]))
        else: # MultiFrame
            return MultiFrame(OrderedDict([(i, c.__rtruediv__(other.cases[i]))
                    for i, c in self.cases.items()]))


    def __add__(self, other):
        ''' add self with other '''
        return MultiFrame(OrderedDict([(i, c.__add__(other.cases[i]))
                    for i, c in self.cases.items()]))

    def __radd__(self, other):
        ''' add other with self '''
        return MultiFrame(OrderedDict([(i, c.__radd__(other.cases[i]))
                    for i, c in self.cases.items()]))


    def __sub__(self, other):
        ''' add self with other '''
        return MultiFrame(OrderedDict([(i, c.__sub__(other.cases[i]))
                    for i, c in self.cases.items()]))

    def __rsub__(self, other):
        ''' add other with self '''
        return MultiFrame(OrderedDict([(i, c.__rsub__(other.cases[i]))
                    for i, c in self.cases.items()]))


    def __repr__(self):
        s = "MultiFrame with {} entries:\n".format(len(self.cases))
        s += "\n".join(["{}\n{}:\n{}".format(80*"=", name, c.describe())
                        for name, c in self.cases.items()])
        return s

    def __init__(self, cases=None):
        if type(cases) == list:
            self.cases = OrderedDict([(case.properties.name, case)
                                      for case in cases])
        elif type(cases) == OrderedDict:
            self.cases = cases
        else:
            self.cases = {}

    def __getitem__(self, field):
        """ get field of all cases"""
        return MultiFrame(OrderedDict([(key, serie[field])
                for key, serie in self.cases.items()]))

    def __setitem__(self, key, value):
        for k, v in self.cases.items():
            if isinstance(value, NumberTypes):
                v.__setitem__(key, value)
            else:
                v.__setitem__(key, value.cases[k])

    def fillna(self, value, **kwargs):
        if not kwargs.get("inplace", False):
            return MultiFrame(OrderedDict([(key, serie.fillna(value, **kwargs))
                    for key, serie in self.cases.items()]))
        else:
            for _, s in self.cases.items():
                s.fillna(value, **kwargs)

    @property
    def columns(self):
        cls = []
        for _, case in self.cases.items():
            cls.extend(case.columns)
        return set(cls)

    def extend(self, value):
        for c in self.columns:
            for idx, case in self.cases.items():
                if len(self.cases[idx][c]) == 0:
                    self.cases[idx][c] = value
        return self

    @property
    def latest_times(self):
        return {k: v.latest_time for k, v in self.cases.items()}

    def sensitivity(self, base, params, baseParam):
        from pandas import Series
        baseCase = self.cases[base]
        for fieldName, field in baseCase.items():
            sName = "sens" + fieldName
            for l in baseCase.locations:
                    baseField = baseCase.location(l)[fieldName] * 0.0

                    for (name, case), param in zip(self.cases.items(), params):
                        if (name == base):
                            continue
                        try:
                            # deltaF = Series(abs((case.location(l)[fieldName].values - baseField.values)/baseField.values))
                            deltaF = Series(case.location(l)[fieldName].values - baseField.values)
                            print(deltaF)
                            deltaX = abs((param - baseParam)/baseParam)
                            # NOTE different times
                            foo = deltaF/deltaX / (len(self.cases)-1)
                            foo.index = baseField.index
                            baseField += foo
                        # delta = abs(baseCase[fieldName] - case[fieldName])/abs(baseParam-param)
                        # print(delta)
                        except Exception as e:
                             print(l, fieldName, e)

    def time_average(self, suffix="Avg", time_start=0.0):
        """ compute time average of fields """
        return MultiFrame([case.time_average(suffix, time_start)
                           for cname, case in self.cases.items()])


    def names(self):
        return [name for name in self.cases]

    def select(self, case):
        """ select a specific item """
        return self.cases[case]

    def unselect(self, cases):
        """ select a specific item """

        return MultiFrame(OrderedDict([(key, serie)
                for key, serie in self.cases.items() if key not in cases ]))


    def values(self):
        for case in self.cases.values():
            yield case

    def items(self):
        for name, case in self.cases.items():
            yield name, case

    def insert(self, key, value):
        self.cases[key] = value


    def histogram(self, y, x=None, **kwargs):
        cases = list(self.cases.keys())
        fig = self.cases[cases[0]].histogram(x=x, y=y, **kwargs)
        for c in cases:
            fig = self.cases[c].histogram(x=x, y=y, figure=fig, **kwargs)
        return fig

    def cdf(self, y, x=None, **kwargs):
        cases = list(self.cases.keys())
        fig = self.cases[cases[0]].histogram(x=x, y=y, **kwargs)
        for c in cases:
            fig = self.cases[c].cdf(x=x, y=y, figure=fig, **kwargs)
        return fig


    def show(self, y, x='Pos', z=False, overlay="Field",
             style=None, filename=None, show=True, **kwargs):
        """ Display single quantity y over multiple cases
            if overlay is set all cases are plotted in to single
            graph """
        # TODO if not overlay, common part should be figure title
        #style = (compose_styles(style, []) if isinstance(style, list) else style)
        dashes = cycle([[8, 4], [4, 4], [4, 2], [1, 1]])
        cases = list(self.cases.keys())

        # call show method of first case instance
        # this generates an ordered hashmap (row)
        # of plot into which the subsequent plots
        # are inserted.
        row = self.cases[cases[0]].show(
                x=x, y=y, overlay=overlay,
                legend_prefix=cases[0], style=style,
                post_pone_style=True, titles=y, filename=filename,
                **kwargs)

        for c, d, col in zip(cases[1:], dashes, rcParams["plotWrapper"].colored[1:]):
            row = self.cases[c].show(
                    x=x, y=y, overlay=overlay,
                    legend_prefix=c, style=style,
                    row=row, post_pone_style=True,
                    line_dash=d, titles=y, color=col, **kwargs)

        return row


    # ----------------------------------------------------------------------
    # Filter methods

    def filter(self, name, index=None, field=None):
        for cname, case in self.cases.items():
            self.cases[cname] = case.filter(name, index, field)
        return self

    def filter_fields(self, name, lower, upper):
        """ filter based on field values

            Examples:

                .filter_fields('T', 1000, 2000)
        """
        return self.filter(name, field=lambda x: lower < x < upper)

    def filter_locations(self, index):
        """ filter based on locations

            Examples:

                .filter_location(Owls.isIn('radial'))
                .filter_location(Owls.isNotIn('radial'))

        """
        return self.filter(name='Loc', index=index)

    def filter_items(self, func):
        """ select items based on filter funtion

            Example .filter_items(lambda ff: "Foo" in ff.locations)
        """
        return MultiFrame(filter(func, self.cases.items()))

    # ----------------------------------------------------------------------
    # Selection methods

    def location(self, loc):
        return MultiFrame([c.location(loc) for _, c in self.cases.items()])

    @property
    def latest(self):
        """ Grouping delegator """
        return MultiFrame([case.latest for cname, case in self.cases.items()])

    def on(self, case, func, **kwargs):
        """
            mf.on('Exp', "location", loc='axis')
        """
        n = getattr(self.cases[case], func)(**kwargs)
        return MultiFrame([(case_ if cname != case else n)
                           for cname, case_ in self.cases.items()])

    # ----------------------------------------------------------------------
    # Grouping methods

    def by_index(self, field, func=None):
        func = (func if func else lambda x: x)
        return self.by(field, func)

    def by_field(self, field, func=None):
        func = (func if func else lambda x: x)
        return self.by(field, func)

    def by_location(self, func=None):
        func = (func if func else lambda x: x)
        return self.by("Loc", func)

    def by_time(self, func=None):
        func = (func if func else lambda x: x)
        return self.by("Time", func)

    def by(self, name, func):
        """ Grouping delegator """
        return MultiFrame([case.by(name, func)
                           for cname, case in self.cases.items()])

    def vectorize(self, func):
        """  """
        mfs = [(name, func(mf)) for name, mf in self.cases.items()]
        return MultiFrame(OrderedDict(mfs))

    def update_plot_properties(self, field, d):
        """ update plot properties of all casese """

        for _, c in self.cases.items():
                c.properties.plot_properties.insert(field, d)
        return self
