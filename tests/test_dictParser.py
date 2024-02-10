import Owls.parser.FoamDict as pfd


def test_simple_parse():
    parser = pfd.FileParser()

    def parse_and_convert_back(text):
        result_dict = parser.parse_str_to_dict(text)
        result_text = ""
        for k, v in result_dict.items():
            result_text += pfd.dispatch_to_str((k, v), "", "") + "\n"
        result_text = result_text[0:-1]
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

    text = """key
{
\tfoo bar;
}

"""
    result_dict, result_text = parse_and_convert_back(text)
    assert result_dict == {"key": {"foo": "bar"}}
    assert result_text == text

    text = '#include "foo/bar"'
    result_dict, result_text = parse_and_convert_back(text)
    assert result_dict == {'#include_"foo/bar"': '"foo/bar"'}
    assert result_text == text

    # as single variable
    text = """foo
{
\t$bar;
}

"""
    result_dict, result_text = parse_and_convert_back(text)
    assert result_dict == {"foo": {"$_bar": "bar"}}
    assert result_text == text

    # as key value pair
    text = "foo $bar;"
    result_dict, result_text = parse_and_convert_back(text)
    assert result_dict == {"foo": "$ bar"}
    assert result_text == text

    text = """inletPatch "CFDWT_In.*";
outletPatch "CFDWT_Out.*";
wallPatches "(Windsor_Body.*|Windsor_Pins.*|Windsor_Base.*|CFDWT_Floor.*)";
forcesWallPatches "(Windsor_Body|Windsor_Pins|Windsor_Base)";
"""
    result_dict, result_text = parse_and_convert_back(text)
    # assert result_dict == {}
    assert len(result_dict.items()) == 4
    assert result_dict == {
        "inletPatch": '"CFDWT_In.*"',
        "outletPatch": '"CFDWT_Out.*"',
        "wallPatches": '"(Windsor_Body.*|Windsor_Pins.*|Windsor_Base.*|CFDWT_Floor.*)"',
        "forcesWallPatches": '"(Windsor_Body|Windsor_Pins|Windsor_Base)"',
    }
    assert result_text + "\n" == text
