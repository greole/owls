"""
Reads and converts OpenFoam logfiles and data
to Pandas DataFrames and Series
"""
import re
import pandas as pd
import os
import errno
import logging

from subprocess import check_output
from .FoamDict import separator_str
from warnings import warn
from pathlib import Path
from file_read_backwards import FileReadBackwards
from copy import deepcopy


class Matcher:
    """Base class for a simple matcher that matches exactely one line of a log file
    based on a given regex"""

    count = 1

    def match(self, line: str):
        """Call and return re.match on the given line with the child class re"""
        ret = re.match(self.re, line)
        if ret:
            ret_dict = ret.groupdict()
            ret_dict[self.name + "_count"] = self.count
            self.count += 1
            return ret_dict
        else:
            return {}

    def reset(self):
        self.count = 1


def apply_line_parser_(line: str, matcher: Matcher) -> dict:
    """Applies a line parser and return results"""
    m = matcher.match(line)
    return m if m else {}


class customMatcher(Matcher):
    def __init__(self, name, re):
        self.name = name
        self.re = re


class transportEqn(Matcher):
    def __init__(self, name):
        self.name = name

    @property
    def re(self):
        return (
            rf"(?P<{self.name}_solverName>\w+):  Solving for {self.name}, Initial"
            r" residual ="
            rf" (?P<{self.name}_InitialResidual>[\w+.\-]*), Final residual ="
            rf" (?P<{self.name}_FinalResidual>[\w+.-]*), No Iterations"
            rf" (?P<{self.name}_NoIterations>[0-9]*)"
        )


class Spliter:
    """Base class for a splitter, where a splitter gets a list of lines and
    yields one or more sub lists and a new state"""

    inner = None

    def split(self, lines: list[str]):
        """Call and return re.match on the given line with the child class re"""
        line_buffer = []
        state = {}
        for line in lines:
            state, start = self.check_line(line)
            # depending on kind of splitter we either start or end a match
            # NOTE assume start of match for now
            if state and start:
                # Yield everything collected so far
                # flush the buffer and reset all inner Spliter states
                if self.inner:
                    self.inner.reset()
                while line_buffer:
                    yield state, line_buffer.pop(0)

            line_buffer.append(line)

        # yield the remaining state and buffer
        for line in line_buffer:
            yield self.state, line

    def reset(self):
        """ABC function, in case concrete child does not implement a reset  function"""
        pass


class PimpleMatcher(Spliter, Matcher):
    def __init__(self):
        self.state = {}
        self.name = "PIMPLE"

    @property
    def re(self):
        return r"PIMPLE: iteration (?P<PIMPLEIteration>[0-9]*)"

    def check_line(self, line):
        # The PimpleMatcher delays its state since
        # we first find the PIMPLE: iteration No key
        # and collect till next ocurrance
        new_state = apply_line_parser_(line, self)
        if new_state:
            return_state = self.state
            self.state = new_state
            return return_state, True
        else:
            return {}, True


class simpleMatcher(Matcher):
    pass


class LogKey:
    def __init__(
        self,
        search_string: str,
        columns: list[str],
        post_fix: list[str] = None,
        append_search_to_col: bool = False,
        prepend_search_to_col: bool = False,
    ):
        """Class to hold search strings for the log parser and map search
        into DataFrame columns and names. This log key expects as many results
        per time steps as post_fixes are present.

        For example create a LogKey(
            search_string='Solving for U',
            columns=['init', 'final', 'iter'],
            post_fix=[_Ux, _Uy, _Uz])

        it will create a DataFrame with init_Ux, final_Ux, iter_Ux, init_Uy, ... iter_Uz columns
        where the post fix distinguish values on different lines of the log file

        Parameter:
            - search_string: string to look for in log file
            - columns: names of the columns in resulting DataFrame
            - post_fix: append this str to all column names
        """
        self.search_string = search_string
        self.columns = columns
        self.column_names = columns
        self.post_fix = None
        if post_fix:
            self.post_fix = post_fix
            self.column_names = []
            for p in post_fix:
                for c in self.columns:
                    self.column_names.append(c + p)
        if append_search_to_col:
            self.post_fix = [search_string] * len(columns)
            self.column_names = [n + "_" + search_string for n in self.column_names]
        if prepend_search_to_col:
            self.post_fix = [search_string] * len(columns)
            self.column_names = [search_string + n for n in self.column_names]
        self.next_key_ = 0

    def __repr__(self):
        return f"{self.search_string}: {','.join(self.column_names)}"

    def reset_next_key(self):
        """Resets the post_fix counter"""
        self.next_key_ = 0


class LogHeader:
    """Content till the // * * // separator line"""

    def __init__(self, fn):
        self._read_header(fn)
        self.Build = self._finder("Build")
        self.Arch = self._finder("Arch").replace('"', "")
        self.Exec = self._finder("Exec")
        self.nProcs = int(self._finder("nProcs"))
        self.Time = self._finder("Time")
        self.Host = self._finder("Host")
        self.PID = int(self._finder("PID"))
        self.IO = self._finder("I/O")
        self.Case = self._finder("Case")

    def _finder(self, name):
        return re.findall(name + r"[ ]*: ([\w.\-=:;\"\"\/]*)", self.header_str_)[0]

    def _read_header(self, fn):
        self.header_str_ = ""
        with open(fn, encoding="utf-8") as fh:
            for line in fh.readlines():
                if separator_str in line:
                    break
                self.header_str_ += line

    @property
    def content(self):
        return self.header_str_


class Initialisation:
    def __init__(self):
        pass


class LogFooter:
    """Content till last ExecutionTime ocurence"""

    def __init__(self, fn):
        self._read_footer(fn)

    @property
    def content(self):
        return self.footer_str_

    def _read_footer(self, fn):
        footer_lst_ = []
        with FileReadBackwards(fn, encoding="utf-8") as frb:
            for line in frb:
                if "ExecutionTime" in line:
                    break
                footer_lst_.insert(0, line)
        self.footer_str_ = "\n".join(footer_lst_[::-1])


class TimeStep:
    """Content from Time = till the next occurance"""

    def __init__(self, fn):
        pass


class LogFile:
    def __init__(
        self,
        fn: str,
        matcher: list[Matcher] = None,
        spliter: Spliter = None,
        frequency=1,
    ):
        self.fn = fn
        self.frequency = frequency
        self.matcher = matcher
        self.spliter = spliter if spliter else PimpleMatcher()
        if not Path(self.fn).exists():
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.fn)

    @property
    # The PimpleMatcher delays its state since
    # we first find the PIMPLE: iteration No key
    # and collect till next ocurrance
    def header(self):
        self.header_ = LogHeader(self.fn)
        return self.header_

    @property
    def timesteps(self):
        self.footer_ = LogFooter(self.fn)
        return self.footer_

    @property
    def footer(self):
        self.footer_ = LogFooter(self.fn)
        return self.footer_

    def find_start_(self, log: str) -> int:
        """Fast forward through file till 'Starting time loop'"""
        for i, line in enumerate(log):
            if "Starting time loop" in line:
                return i

    def time_steps_(self, frequency=None):
        if not frequency:
            frequency = self.frequency

        found_starting_time_loop = False
        found_first_time = False
        line_buffer = []

        remaining = frequency
        # TODO skip reading of lines if remaining > 1 entirely
        # instead of just clearing the buffer

        with open(self.fn, encoding="utf-8") as fh:
            for line in fh.readlines():
                if ("Starting time loop" in line) and not found_starting_time_loop:
                    found_starting_time_loop = True
                if line.startswith("Time =") and found_starting_time_loop:
                    time = float(re.findall(r"Time = ([\w.\-]*)", line)[0])
                    line_buffer = []
                elif "ExecutionTime = " in line:
                    line_buffer.append(line)
                    remaining -= 1
                    if remaining == 0:
                        remaining = frequency
                        ret_buffer = deepcopy(line_buffer)
                        line_buffer = []
                        yield time, ret_buffer
                elif found_starting_time_loop:
                    line_buffer.append(line)

    def parse_inner_loops_(
        self, timestep: [str], matcher: list[Matcher], spliter: Matcher, state
    ):
        """Given a parsed time step, this function parses for innner loops

        Yields: a records
        """
        prev_inner_state = {}
        for inner_state, line in spliter.split(timestep):
            state.update(inner_state)
            if not inner_state == prev_inner_state:
                prev_inner_state = deepcopy(inner_state)
                for m in matcher:
                    m.reset()
            for m in matcher:
                res = apply_line_parser_(line, m)
                if res:
                    ret = deepcopy(state)
                    ret.update(res)
                    yield ret

    def parse_to_records(self) -> list[dict]:
        for time_name, content in self.time_steps_(self.frequency):
            for record in self.parse_inner_loops_(
                content, self.matcher, self.spliter, {"Time": time_name}
            ):
                yield record

    def parse_to_df(self):
        records = list(self.parse_to_records())
        df = pd.DataFrame.from_records(records)

        # FIXME currently all parsing results without a p count
        # are assigned to first p
        df["p_count"] = df["p_count"].fillna(1)
        return df.groupby(["Time", "p_count"]).first().reset_index()
