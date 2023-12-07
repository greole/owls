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
from typing import Generator


class Matcher:
    """Base class for a simple matcher that matches exactly one line of a log file
    based on a given regex"""

    count = 1
    name: str = None

    def match(self, line: str):
        """Call and return re.match on the given line with the child class re"""
        ret = self.re.match(line)
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


def eval_dict(d: dict) -> dict:
    """maps eval over the dict values"""
    def eval_f(s):
        if isinstance(s, str):
            return eval(s)
        return s
    return {k: eval_f(v) for k, v in d.items()}


class customMatcher(Matcher):
    def __init__(self, name, re_txt):
        self.name = name
        self.re = re.compile(re_txt)


class transportEqn(Matcher):
    def __init__(self, name):
        self.name = name
        self.re = re.compile(
            rf"(?P<{self.name}_solverName>\w+):  Solving for {self.name}, Initial"
            r" residual ="
            rf" (?P<{self.name}_InitialResidual>[\w+.\-]*), Final residual ="
            rf" (?P<{self.name}_FinalResidual>[\w+.-]*), No Iterations"
            rf" (?P<{self.name}_NoIterations>[0-9]*)"
        )


class CourantNumber(Matcher):
    def __init__(self):
        self.name = "CourantNumber"
        self.re = re.compile(
            rf"Courant Number mean: (?P<{self.name}_mean>[0-9e.\-]*) max:"
            rf" (?P<{self.name}_max>[0-9e.\-]*)"
        )


class ExecutionTime(Matcher):
    def __init__(self):
        self.name = "ExecutionTime"
        self.re = re.compile(
            rf"ExecutionTime = (?P<ExecutionTime>[0-9e.\-]*) s  ClockTime ="
            rf" (?P<ClockTime>[0-9e.\-]*) s"
        )


class timeStepContErrors(Matcher):
    def __init__(self):
        self.name = "timeStepContErrors"
        self.re = re.compile(
            r"time step continuity errors : sum local ="
            rf" (?P<{self.name}_sumLocal>[\w+.\-]*), global ="
            rf" (?P<{self.name}_sumGlobal>[\w+.\-]*), cumulative ="
            rf" (?P<{self.name}_cumulative>[\w+.\-]*)"
        )


class Spliter:
    """Base class for a splitter, where a splitter gets a list of lines and
    yields one or more sub lists and a new state"""

    inner = None

    def check_line(self, line: str):
        pass

    def split(self, lines: list[str]):
        """Call and return re.match on the given line with the child class re"""
        line_buffer: list[str] = []
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
                line_buffer_ret = list(line_buffer)
                line_buffer = []
                for line_ret in line_buffer_ret:
                    yield state, line_ret

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
        self.re = re.compile(r"PIMPLE: iteration (?P<PIMPLEIteration>[0-9]*)")

    def check_line(self, line):
        # The PimpleMatcher delays its state since
        # we first find the PIMPLE: iteration No key
        # and collect till next occurrence
        new_state = apply_line_parser_(line, self)
        if new_state:
            return_state = self.state
            self.state = new_state
            return return_state, True
        else:
            return {}, True


class simpleMatcher(Matcher):
    pass


class LogHeader:
    """Content till the // * * // separator line"""

    def __init__(self, fn):
        self.__read_header(fn)
        self.Build = self.__finder("Build")
        self.Arch = self.__finder("Arch").replace('"', "")
        self.Exec = self.__finder("Exec")
        self.nProcs = int(self.__finder("nProcs"))
        self.Time = self.__finder("Time")
        self.Host = self.__finder("Host")
        self.PID = int(self.__finder("PID"))
        self.IO = self.__finder("I/O")
        self.Case = self.__finder("Case")

    def __finder(self, name):
        return re.findall(name + r"[ ]*: ([\w.\-=:;\"\"\/]*)", self.__header_str)[0]

    def __read_header(self, fn):
        self.__header_str = ""
        with open(fn, encoding="utf-8") as fh:
            for line in fh.readlines():
                if separator_str in line:
                    break
                self.__header_str += line

    @property
    def content(self):
        return self.__header_str


class LastTimeStep:
    """Reverse read of log file to get content of last time step"""

    def __init__(self, fn):
        self.__read_last_timestep(fn)

    def __read_last_timestep(self, fn):
        footer_lst_ = []
        with FileReadBackwards(fn, encoding="utf-8") as frb:
            for line in frb:
                footer_lst_.insert(0, line)
                if line.startswith("Time ="):
                    break
        self.__footer_str = "\n".join(footer_lst_)

    @property
    def content(self):
        return self.__footer_str

    @property
    def time(self):
        try:
            ret = float(
                self.__footer_str.split("\n")[0].replace("Time = ", "").replace("s", "")
            )
            return ret
        except Exception as e:
            print("failure to parse:\n", self.__footer_str)

    @property
    def continuity_errors(self):
        for line in self.__footer_str.split("\n"):
            if not line.startswith("time step continuity errors"):
                continue
            return eval_dict(apply_line_parser_(line, timeStepContErrors()))

    @property
    def Courant_number(self):
        for line in self.__footer_str.split("\n"):
            if not line.startswith("Courant Number"):
                continue
            return eval_dict(apply_line_parser_(line, CourantNumber()))
        return {"CourantNumber": 0.0}

    @property
    def execution_time(self):
        for line in self.__footer_str.split("\n"):
            if not line.startswith("ExecutionTime"):
                continue
            return {
                k: float(v)
                for k, v in apply_line_parser_(line, ExecutionTime()).items()
            }
        return {"ExecutionTime": 0.0, "ClockTime": 0.0}


class LogFooter:
    """Content till last ExecutionTime ocurence"""

    def __init__(self, fn):
        self.__read_footer(fn)

    @property
    def content(self):
        return self.__footer_str

    def __read_footer(self, fn):
        footer_lst_ = []
        with FileReadBackwards(fn, encoding="utf-8") as frb:
            for line in frb:
                if "ExecutionTime" in line:
                    break
                footer_lst_.insert(0, line)
        self.__footer_str = "\n".join(footer_lst_[::-1])

    @property
    def completed(self):
        return ("Finalising" in self.__footer_str) or ("End" in self.__footer_str)


class LogFile:
    """A parser class for OpenFOAM log files which gives access to the log file
    header, the parsed content and the log file footer.

    To parse content a list of Matcher objects are used, where a matcher can be
    a transportEqn or an instantiated customMatcher. If the same Matcher matches
    multiple times per time step the matcher_name_count is incremented

    Additionally, a splitter subdivides a timestep
    """

    __header = None

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
    def header(self):
        if not self.__header:
            self.__header = LogHeader(self.fn)
        return self.__header

    @property
    def latestTime(self):
        self.__latestTime = LastTimeStep(self.fn)
        return self.__latestTime

    @property
    def footer(self):
        self.__footer = LogFooter(self.fn)
        return self.__footer

    def __time_steps(self, frequency=None):
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
                    time = float(re.findall(r"Time = ([\w.\-]*)[s]*", line)[0])
                    line_buffer = []
                elif "ExecutionTime = " in line:
                    line_buffer.append(line)
                    remaining -= 1
                    if remaining == 0:
                        remaining = frequency
                        ret_buffer = list(line_buffer)
                        line_buffer = []
                        yield time, ret_buffer
                elif found_starting_time_loop:
                    line_buffer.append(line)

    def __parse_inner_loops(
        self, timestep: [str], matcher: list[Matcher], spliter: Spliter, state
    ):
        """Given a parsed time step, this function parses for innner loops

        Yields: a record
        """
        prev_inner_state: dict[str, str] = {}
        for inner_state, line in spliter.split(timestep):
            state.update(inner_state)
            if not inner_state == prev_inner_state:
                prev_inner_state = dict(inner_state)
                for m in matcher:
                    m.reset()
            for m in matcher:
                res = apply_line_parser_(line, m)
                if res:
                    res.update(state)
                    yield res

    def parse_to_records(self) -> Generator[dict, None, None]:
        for time_name, content in self.__time_steps(self.frequency):
            for record in self.__parse_inner_loops(
                content, self.matcher, self.spliter, {"Time": time_name}
            ):
                yield record

    def parse_to_df(self):
        records = list(self.parse_to_records())
        df = pd.DataFrame.from_records(records)

        # FIXME currently all parsing results without a p count
        # are assigned to first p
        if "p_count" in df.columns:
            df["p_count"] = df["p_count"].fillna(1)
            return df.groupby(["Time", "p_count"]).first().reset_index()
        return df
