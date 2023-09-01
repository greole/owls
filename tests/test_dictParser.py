import Owls.parser.FoamDict as pfd


def test_simple_parse():
    parser = pfd.FileParser()

    def parse_and_convert_back(text):
        result_dict = parser.parse_str_to_dict(text)
        k, v = list(result_dict.items())[0]
        result_text = pfd.dispatch_to_str((k, v), "", "")
        return result_dict, result_text

    text = "key value;"
    result_dict, result_text = parse_and_convert_back(text)
    assert result_dict == {"key": "value"}
    assert result_text == text

    text = "key 10;"
    result_dict, result_text = parse_and_convert_back(text)
    assert result_dict == {"key": 10}
    assert result_text == text

    text = "key 0.01;"
    result_dict, result_text = parse_and_convert_back(text)
    assert result_dict == {"key": 0.01}
    assert result_text == text

    text = "key 1e-05;"
    result_dict, result_text = parse_and_convert_back(text)
    assert result_dict == {"key": 0.00001}
    assert result_text == text

    text = "key foo bar;"
    result_dict, result_text = parse_and_convert_back(text)
    assert result_dict == {"key": "foo bar"}
    assert result_text == text

    text = "key {foo bar;}"
    result_dict, result_text = parse_and_convert_back(text)
    assert result_dict == {"key": {"foo": "bar"}}
    # NOTE Dont test for now since string is reformated
    # assert result_text == text

    text = '#include "foo/bar"'
    result_dict, result_text = parse_and_convert_back(text)
    assert result_dict == {'#include_"foo/bar"': '"foo/bar"'}
    assert result_text == text

    text = "foo $bar;"
    result_dict, result_text = parse_and_convert_back(text)
    assert result_dict == {"foo": "$ bar"}
    assert result_text == text
