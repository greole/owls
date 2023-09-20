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


class Matcher:
    def match(self, line: str):
        """Call and return re.match on the given line with the child class re"""
        ret = re.match(self.re, line)
        if ret:
            return ret.groupdict()
        else:
            return {}


class transportEqn(Matcher):
    def __init__(self, name):
        self.name = name

    @property
    def re(self):
        return (
            rf"(?P<{self.name}_solverName>\w+):  Solving for {self.name}, Initial residual ="
            rf" (?P<{self.name}_InitialResidual>[\w+.\-]*), Final residual ="
            rf" (?P<{self.name}_FinalResidual>[\w+.-]*), No Iterations (?P<{self.name}_NoIterations>[0-9]*)"
        )


class PimpleMatcher(Matcher):
    @property
    def re(self):
        return r"PIMPLE: iteration (?P<PIMPLEIteration>[0-9]*)"


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
    def __init__(self, fn: str, inner_loop_parser=None, frequency=1):
        self.fn = fn
        self.frequency = frequency
        if not Path(self.fn).exists():
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.fn)

    @property
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
        line_buffer = ""

        remaining = frequency
        # TODO skip reading of lines if remaining > 1 entirely
        # instead of just clearing the buffer

        with open(self.fn, encoding="utf-8") as fh:
            for line in fh.readlines():
                if ("Starting time loop" in line) and not found_starting_time_loop:
                    found_starting_time_loop = True
                if line.startswith("Time =") and found_starting_time_loop:
                    time = float(re.findall(r"Time = ([\w.\-]*)", line)[0])
                    line_buffer = ""
                elif "ExecutionTime = " in line:
                    line_buffer += line
                    remaining -= 1
                    if remaining == 0:
                        remaining = frequency
                        yield time, line_buffer
                elif found_starting_time_loop:
                    line_buffer += line

    def parse_inner_loops_(
        self, timestep: str, matcher: list[Matcher], spliter: list[Matcher], state
    ):
        """Given a parsed time step, this function parses for innner loops

        Returns:
            A tuple of the parse content and additional indices
        """
        # if not self.inner_loop_parser:
        #     yield timestep, ()
        #
        def inner_loops(timestep):
            # TODO we need to distinguish between matches that start and end
            # a block
            line_buffer = []
            state = {}
            for line in timestep.split("\n"):
                for s in spliter:
                    state = self.apply_line_parser_(line, s)
                    print("test match", line, state)
                    if state:
                        ret = line_buffer
                        line_buffer = []
                        yield state, ret
                line_buffer.append(line)
            yield state, line_buffer

        for state, lines in inner_loops(timestep):
            print(state, lines)
            for line in lines:
                for m in matcher:
                    state.update(self.apply_line_parser_(line, m))
        return state

    def apply_line_parser_(self, line: str, matcher: Matcher):
        """Applies a line parser and return results"""
        m = matcher.match(line)
        return m if m else {}

    def reset_next_keys(self):
        """Resets all next keys"""
        for logkey in self.keys:
            logkey.reset_next_key()

    def extract_(self, line: str):
        """Returns key and values as list
        eg "ExecutionTime":[0,1]
        """

        for logkey in self.keys:
            key = logkey.search_string
            next_key = logkey.next_key_
            col_names = logkey.column_names[
                next_key * len(logkey.columns) : (next_key + 1) * len(logkey.columns)
            ]
            if re.search(key, line):
                logkey.next_key_ += 1
                return (
                    key,
                    col_names,
                    list(
                        map(
                            float,
                            filter(
                                lambda x: x,
                                re.findall(
                                    r"[0-9\-]+[.]?[0-9]*[e]?[\-\+]?[0-9]*", line
                                ),
                            ),
                        )
                    ),
                )
        return None, None, None

    def parse_to_records(self, log_str: str) -> list[dict]:
        """Parse a given log_str to a list of dictionaries"""
        log_str = log_str.split("\n")

        start = self.find_start_(log_str)
        self.records = []
        time = 0
        tmp_record = {}
        for line in log_str[start:-1]:
            key, col_names, values = self.extract_(line)
            if line == "End":
                return self.records
            if not col_names or not values or not line:
                continue
            if col_names[0] == "Time":
                # a new time step has begun
                time = values[0]
                self.reset_next_keys()
            # TODO check if all post_fixes have been consumed
            # then start a new row
            else:
                for i, col in enumerate(col_names):
                    tmp_record["Time"] = time
                    tmp_record[col_names[i]] = values[i]
                self.records.append(tmp_record)
                tmp_record = {}
        return self.records

    @property
    def is_complete(self) -> bool:
        """Check for End or Finalising parallel run in last line of log"""
        log_tail = check_output(["tail", "-n", "1", self.log_name], text=True)
        return "End" in log_tail or "Finalising parallel run" in log_tail

    def parse(self, log_name: str):
        with open(log_name, encoding="utf-8") as log:
            f = log.read()
            return self.parse_to_records(f)

    def parse_to_df(self, log_name: str) -> pd.DataFrame:
        """Read from log_name and constructs a DataFrame"""
        # TODO call this from __init__
        self.log_name = log_name
        records = self.parse(log_name)
        if not records:
            warning = f"{self.keys} produced empty sets of records for {log_name}"
            warn(warning)
            return pd.DataFrame()
        df = pd.DataFrame.from_records(records)
        df = df.groupby("Time").max().reset_index()
        df.set_index(keys=["Time"], inplace=True)
        self.header = LogHeader(log_name)
        return df

    def import_logs(
        self, folder: str, search: str = "log", time_key: str = "^Time = "
    ) -> pd.DataFrame:
        """ """
        # TODO remove this since LogFile should only support a single log file
        # we should add a LogFileCollection class as a container

        fold, dirs, files = next(os.walk(folder))
        logs = [fold + "/" + log for log in files if search in log]

        df = pd.DataFrame()

        for log_name in logs:
            df2 = self.parse_to_df(log_name)
            if df2.empty:
                continue
            df = pd.concat([df, df2])
        return df
