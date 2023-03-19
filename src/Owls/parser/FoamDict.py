#!/usr/bin/env python3

import os
import pyparsing as pp


extended_alphanum = pp.Word(pp.alphanums + '#_-."/')


def dispatch_to_str(item, indent="", nl="\n\n"):
    """dispatch to corresponding methods"""
    key, value = item
    if isinstance(key, str) and key.startswith("#"):
        return OFInclude().to_str(key, value, indent=indent, nl=nl)
    if isinstance(key, str) and key.startswith("$"):
        return OFVariable().to_str(key, value, indent=indent, nl=nl)
    if key == "functions":
        return OFFunctions().to_str(key, value, indent=indent, nl=nl)
    if isinstance(value, dict):
        s = "{}{}\n{}{{\n".format(indent, key, indent)
        new_indent = indent + "\t"
        for k, v in value.items():
            s += dispatch_to_str((k, v), new_indent, nl="\n")
        s += indent + "}\n\n"
        return s
    elif isinstance(value, list):
        return OFList().to_str(key, value, indent=indent, nl=nl)
    try:
        return indent + "{}\t{};{}".format(key, str(value), nl)
    except Exception:
        # print(e, item)
        return ""


class OFList:
    @staticmethod
    def parse():
        """matches (a b c)"""
        # TODO make it recursive
        return (
            pp.Suppress("(")
            + pp.delimitedList(pp.Word(pp.alphanums + '_-."/'), delim=" ")
            + pp.Suppress(")")
            + pp.Suppress(";")
        ).set_results_name("of_list")

    def to_str(self, *args, **kwargs):
        """Convert a python list to a str with OF syntax"""
        key = args[0]
        values = args[1]
        return (
            f'{kwargs.get("indent", "")}{key} ({" ".join(map(str,values))});{kwargs.get("nl",os.linesep)}'
        )


class OFVariable:
    @staticmethod
    def parse():
        """matches $p;"""
        # TODO make it recursive
        return (
            pp.Literal("$") + pp.Word(pp.alphanums) + pp.Suppress(";")
        ).set_results_name("of_variable")

    def to_str(self, *args, **kwargs):
        """Convert a python list to a str with OF syntax"""
        value = args[1]
        return f'{kwargs.get("indent", "")}${value};{kwargs.get("nl",os.linesep)}'


class OFFunctions:
    def to_str(self, *args, **kwargs) -> str:
        """Convert a python list to a str with OF syntax"""
        args[0]
        value = args[1]
        indent = kwargs.get("indent", "")
        ret = "functions {\n"
        for k, v in value.items():
            ret += dispatch_to_str((k, v), indent + "\t", nl="\n")
        ret += "}\n\n"
        return ret


class OFInclude:
    def to_str(self, *args, **kwargs) -> str:
        """Convert a python list to a str with OF syntax"""
        key = args[0].split("_")[0]
        value = args[1]
        return f'{kwargs.get("indent", "")}{key} {value}{kwargs.get("nl",os.linesep)}'


class OFDimensionSet:
    @staticmethod
    def parse():
        """Parse OF dimension set eg  [0 2 -1 0 0 0 0]"""
        return (
            pp.Suppress("[")
            + pp.delimitedList(pp.pyparsing_common.number * 7, delim=pp.White())
            + pp.Suppress("]")
            + pp.Word(pp.alphanums + '_-."/')
            + pp.Suppress(";")
        ).set_results_name("of_dimension_set")

    def to_str(self):
        pass


class FileParser:
    """Abstraction of OpenFOAMs config files which contain key value pairs or key block pairs
    """

    def __init__(self, **kwargs):
        pass

    @property
    def footer(self):
        """the footer of a OpenFOAM file"""
        return "//" + "*" * 73 + "//\n"

    @property
    def separator(self):
        return "// " + "* " * 26 + "//"

    @property
    def key_value_pair(self):
        """matches a b; or a (a b c); or a {foo bar;}"""
        of_dict = pp.Forward()
        key_val_pair = (
            pp.Group(
                (
                    pp.Word(pp.alphanums + '"#(),|*').set_results_name("key")
                    + (
                        OFDimensionSet.parse()
                        ^ of_dict
                        ^ OFList.parse()
                        ^ pp.OneOrMore(
                            pp.Word(pp.alphanums + '".-') + pp.Suppress(";")
                        )  # all kinds of values delimeted by ;
                        ^ pp.Word(
                            pp.alphanums + '"_.-/'
                        )  # for includes which are single strings can contain /
                    ).set_results_name("value")
                )
                # a variable
                ^ OFVariable.parse()
            )
            .ignore(pp.cStyleComment | pp.dblSlashComment)
            .set_results_name("key_value_pair")
        )
        of_dict <<= (
            pp.Suppress("{") + pp.ZeroOrMore(key_val_pair) + pp.Suppress("}")
        ).set_results_name("of_dict")
        return key_val_pair

    @property
    def single_line_comment(self):
        """matches a b; or a (a b c);"""
        return pp.Group(
            pp.Literal("//") + pp.ZeroOrMore(pp.Word(pp.alphanums + '#_-."/'))
        ).set_results_name("single_line_comment")

    @property
    def config_parser(self):
        return pp.Group(
            pp.ZeroOrMore(self.single_line_comment) ^ pp.ZeroOrMore(self.key_value_pair)
        )

    def key_value_to_dict(self, parse_result):
        """converts a ParseResult of a list of  key_value_pair to a python dict"""
        ret = {}
        for res in parse_result:
            # probe if next result is str or ParseResult
            if isinstance(res, pp.results.ParseResults):
                if res.get_name() == "key_value_pair":
                    key = res.key
                    # keys starting with # need special attention to avoid overwriting
                    # them in the return dictionary
                    if key.startswith("#"):
                        key = res[0] + "_" + res[1]
                    if res[0].startswith("$"):
                        key = res[0] + "_" + res[1]

                    # TODO use of_dict over kvp if it works
                    # if res.get("of_dict"):
                    #     ret.update({key: self.key_value_to_dict(res.get("of_dict"))})
                    if res.get("key_value_pair"):
                        d = {key: self.key_value_to_dict([v for v in res.value])}
                        ret.update(d)
                    elif res.get("of_list"):
                        ret.update({key: res.get("of_list").as_list()})
                    elif res.get("value"):
                        ret.update({key: res.get("value")[0]})
                    elif res.get("of_variable"):
                        ret.update({key: res[1]})
                    elif res.get("of_dimension_set"):
                        ret.update({key: res[1]})
            else:
                return res
        return ret

    def parse_file_to_dict(self):
        """parse an OpenFOAM file to an Ordered dict"""
        list_text = self.read(self.path)
        self.of_comment_header = list_text[0:7]
        self.of_header = list_text[7:15]
        self.text = "\n".join(list_text[15:])
        self.parse = self.config_parser.search_string(self.text)
        # if len(self.parse) is bigger than one the parse function
        # did not consume the file entirely and something went most likely wrong
        self._dict = self.key_value_to_dict(self.parse[0][0])
        print(self._dict)
        return self._dict

    def read(self, fn):
        """parse an OF file into a dictionary"""
        with open(fn, "r") as fh:
            return fh.readlines()

    def write_to_disk(self):
        """writes a parsed OF file back into a file"""
        fn = self.path
        dictionary = self._dict

        with open(fn, "w") as fh:
            for line in self.of_comment_header:
                fh.write(line)
            for line in self.of_header:
                fh.write(line)
            fh.write("\n")
            for key, value in dictionary.items():
                fh.write(dispatch_to_str((key, value)))
            fh.write(self.footer)

    def set_key_value_pairs(self, dictionary, flush=True):
        """check if a given key exists and replaces it with the key value pair

        this can be used to modify the value in the file
        """
        sub_dict = dictionary.pop("set", False)
        if sub_dict:
            d = self._dict
            for s in sub_dict.split("/"):
                d = d[s]
        else:
            d = self._dict
        if dictionary.pop("clear", False):
            keys = d.keys()
            for k in keys:
                d[k] = None
        d.update(dictionary)
        if flush:
            self.write_to_disk()
