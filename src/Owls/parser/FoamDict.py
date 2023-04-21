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
            pp.Word(pp.alphanums)
            + pp.Suppress("(")
            + pp.OneOrMore(pp.Word(pp.alphanums + '_-."/'), stopOn=pp.Literal(")"))
            + pp.Suppress(")")
            + pp.Suppress(";")
        ).setResultsName("of_list")

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
        ).setResultsName("of_variable")

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
            pp.Word(pp.alphanums)
            + pp.Suppress("[")
            + pp.delimitedList(pp.pyparsing_common.number * 7, delim=pp.White())
            + pp.Suppress("]")
            + pp.Word(pp.alphanums + '_-."/')
            + pp.Suppress(";")
        ).setResultsName("of_dimension_set")

    def to_str(self):
        pass


class FileParser:
    """Abstraction of OpenFOAMs config files which contain key value pairs or key block pairs
    """

    def __init__(self, **kwargs):
        self.path = kwargs['path']
        self._parsed_file = self.parse_file_to_dict()

    @property
    def footer(self):
        """the footer of a OpenFOAM file"""
        return "//" + "*" * 73 + "//\n"

    @property
    def separator(self):
        return "// " + "* " * 26 + "//"

    def get(self, key):
        try:
            return self._dict[key]
        except KeyError as e:
            print(e)

    @property
    def key_value_pair(self):
        """matches a b; or a (a b c); or a {foo bar;}"""
        of_dict = pp.Forward()
        key_val_pair = (
            pp.Group(
                # a OpenFOAM list
                # try to match a list first because it could be matched as a keyword accidentally
                OFList.parse()
                # a variable
                ^ OFVariable.parse()
                ^ OFDimensionSet.parse()
                ^ (
                    pp.Word(pp.alphanums + '"#(),|*').setResultsName("key")
                    + (
                        pp.OneOrMore(pp.Word(pp.alphanums + '".-')) + pp.Suppress(";")
                        # all kinds of values delimeted by ;
                        ^ of_dict
                        ^ pp.Word(
                            pp.alphanums + '"_.-/'
                        )  # for includes which are single strings can contain /
                    ).setResultsName("value")
                )
            )
            .ignore(pp.cStyleComment | pp.dblSlashComment)
            .setResultsName("key_value_pair")
        )
        of_dict <<= (
            pp.Suppress("{") + pp.ZeroOrMore(key_val_pair) + pp.Suppress("}")
        ).setResultsName("of_dict")
        return key_val_pair

    @property
    def single_line_comment(self):
        """matches a b; or a (a b c);"""
        return pp.Group(
            pp.Literal("//") + pp.ZeroOrMore(pp.Word(pp.alphanums + '#_-."/'))
        ).setResultsName("single_line_comment")

    @property
    def config_parser(self):
        return pp.Group(
            pp.ZeroOrMore(self.single_line_comment) ^ pp.ZeroOrMore(self.key_value_pair)
        )

    def convert_to_number(self, inp):
        """converts to number if possible, return str otherwise"""
        s = " ".join(inp)
        try:
            return eval(s)
        except:
            return s

    def key_value_to_dict(self, parse_result):
        """converts a ParseResult of a list of  key_value_pair to a python dict"""
        ret = {}
        for res in parse_result:
            # probe if next result is str or ParseResult
            if isinstance(res, pp.ParseResults):
                if res.getName() == "key_value_pair":
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
                        tmp_list = res.get("of_list").asList()
                        key = tmp_list[0]
                        values = list(
                            map(
                                lambda x: x.replace("'", "").replace('"', ""),
                                tmp_list[1:],
                            )
                        )
                        ret.update({key: values})
                    elif res.get("value"):
                        ret.update({key: self.convert_to_number(res.get("value"))})
                    elif res.get("of_variable"):
                        ret.update({key: res[1]})
                    elif res.get("of_dimension_set"):
                        tmp_list = res.get("of_dimension_set").as_list()
                        key = tmp_list[0]
                        values = tmp_list[1:-1]
                        values.append(float(tmp_list[-1]))
                        ret.update({key: tuple(values)})
            else:
                return res
        return ret

    def parse_file_to_dict(self):
        """parse an OpenFOAM file to an Ordered dict"""
        list_text = self.read(self.path)
        self.of_comment_header = list_text[0:7]
        self.of_header = list_text[7:15]
        self.text = "\n".join(list_text[15:])
        self._dict = self.parse_str_to_dict(self.text)
        return self._dict

    def parse_str_to_dict(self, s) -> dict:
        """Parse a given FoamDict body str to a python dictionary"""
        self.parse = self.config_parser.searchString(s)
        # if len(self.parse) is bigger than one the parse function
        # did not consume the file entirely and something went most likely wrong
        return self.key_value_to_dict(self.parse[0][0])

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

    def set_key_value_pairs(self, dictionary: dict, flush: bool = True):
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
