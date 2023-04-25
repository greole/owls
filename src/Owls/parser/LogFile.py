"""
Reads and converts OpenFoam logfiles and data
to Pandas DataFrames and Series
"""
import re
import os
from subprocess import check_output
import pandas as pd


class LogKey:
    def __init__(
        self,
        search_string: str,
        columns: list[str],
        post_fix: list[str] = None,
        append_search_to_col: bool = False,
    ):
        self.search_string = search_string
        self.columns = columns
        self.post_fix = None
        if post_fix:
            self.post_fix = post_fix
        if append_search_to_col:
            self.post_fix = ["_" + search_string] * len(columns)
        self.next_key_ = 0

    @property
    def next_key(self):
        if not self.post_fix:
            return None
        ret = self.post_fix[self.next_key_]
        self.next_key_ = (
            self.next_key_ + 1 if self.next_key_ < len(self.post_fix) - 1 else 0
        )
        return ret


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

    def is_complete(self, log_name: str) -> bool:
        """Check for End or Finalising parallel run in last line of log"""
        log_tail = check_output(["tail", "-n", "1", log_name], text=True)
        return "End" in log_tail or "Finalising parallel run" in log_tail

    def parse(self, log_name: str):
        with open(log_name, encoding="utf-8") as log:
            f = log.read()
            return self.parse_to_records(f)

    def parse_to_df(self, log_name: str) -> pd.DataFrame:
        """"""
        df = pd.DataFrame.from_records(self.parse(log_name))
        df = df.groupby("Time").max().reset_index()
        df.set_index(keys=["Time"], inplace=True)
        return df

    def import_logs(
        self, folder: str, search: str = "log", time_key: str = "^Time = "
    ) -> pd.DataFrame:
        """ """

        fold, dirs, files = next(os.walk(folder))
        logs = [fold + "/" + log for log in files if search in log]

        df = pd.DataFrame()

        for log_name in logs:
            df = pd.concat([df, self.parse_to_df(log_name)])
        return df
