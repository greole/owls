"""
Reads and converts OpenFoam logfiles and data
to Pandas DataFrames and Series
"""
import re
import pandas as pd

from subprocess import check_output
from .FoamDict import separator_str
from warnings import warn


class LogKey:
    def __init__(
        self,
        search_string: str,
        columns: list[str],
        post_fix: list[str] = None,
        append_search_to_col: bool = False,
    ):
        """Class to hold search strings for the log parser and map search
        into DataFrame columns and names. This log key expects as many results
        per time steps as post_fixes are present.

        For example create a LogKey(
            search_string='Solving for U',
            columns=['init', 'final', 'iter'],
            post_fix=[_Ux, _Uy, _Uz])

        it will create a DataFrame with init_Ux, final_Ux, iter_Ux, init_Uy, ... iter_Uz columns

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
            # TODO this makes post_fix and append_search_to_col mutually exclusive
            self.post_fix = ["_" + search_string] * len(columns)
            self.column_names = [n + "_" + search_string for n in self.column_names] 
        self.next_key_ = 0

    def __repr__(self):
        return f"{self.search_string}: {','.join(self.column_names)}"

    @property
    def next_key(self):
        if not self.post_fix:
            return None
        ret = self.post_fix[self.next_key_]
        self.next_key_ = (
            self.next_key_ + 1 if self.next_key_ < len(self.post_fix) - 1 else 0
        )
        return ret


class LogHeader:
    def __init__(self, fn):
        self._read_header(fn)
        self.host = re.findall("Host[ ]*: ([\w.-]*)", self.header_str_)[0]

    def _read_header(self, fn):
        self.header_str_ = ""
        with open(fn, encoding="utf-8") as fh:
            for line in fh.readlines():
                if separator_str in line:
                    break
                self.header_str_ += line


class LogFile:
    def __init__(self, keys: list[LogKey], time_key: str = "^Time = "):
        self.keys = keys
        self.keys.append(LogKey(time_key, ["Time"]))

    def find_start_(self, log: str) -> int:
        """Fast forward through file till 'Starting time loop'"""
        for i, line in enumerate(log):
            if "Starting time loop" in line:
                return i

    def extract_(self, line: str):
        """Returns key and values as list
        eg "ExecutionTime":[0,1]
        """

        for logkey in self.keys:
            key = logkey.search_string
            col_names = logkey.columns

            if re.search(key, line):
                return (
                    key,
                    col_names,
                    list(
                        map(
                            float,
                            filter(
                                lambda x: x,
                                re.findall("[0-9\-]+[.]?[0-9]*[e]?[\-\+]?[0-9]*", line),
                            ),
                        )
                    ),
                    logkey.next_key,
                )
        return None, None, None, None

    def parse_to_records(self, log_str: str) -> list[dict]:
        """Parse a given log_str to a list of dictionaries"""
        log_str = log_str.split("\n")

        start = self.find_start_(log_str)
        self.records = []
        time = 0
        tmp_record = {}
        for line in log_str[start:-1]:
            key, col_names, values, post_fix = self.extract_(line)
            if line == "End":
                return self.records
            if not col_names or not values or not line:
                continue
            if col_names[0] == "Time":
                # a new time step has begun
                time = values[0]
            else:
                for i, col in enumerate(col_names):
                    tmp_record["Time"] = time
                    col_name = col if not post_fix else col + post_fix
                    tmp_record[col_name] = values[i]
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
            warn(f"{self.keys} produced empty sets of records for {log_name}")
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

        df = DataFrame()

        for log_name in logs:
            df2 = self.parse_to_df(log_name)
            if df2.empty:
                continue
            df = concat([df, df2])
        return df
