import Owls.parser.FoamDict as pfd


def test_simple_parse():
    parser = pfd.FileParser()

    text = "key value;"
    assert parser.parse_str_to_dict(text) == {"key": "value"}

    text = "key 10;"
    assert parser.parse_str_to_dict(text) == {"key": 10}

    text = "key 0.01;"
    assert parser.parse_str_to_dict(text) == {"key": 0.01}

    text = "key 1e-5;"
    assert parser.parse_str_to_dict(text) == {"key": 0.00001}

    text = "key foo bar;"
    assert parser.parse_str_to_dict(text) == {"key": "foo bar"}

    text = "key {foo bar;}"
    assert parser.parse_str_to_dict(text) == {"key": {"foo": "bar"}}

    text = '#include "foo/bar"'
    assert parser.parse_str_to_dict(text) == {'#include_"foo/bar"': '"foo/bar"'}
