import os

import Owls.parser.FoamDict as fd

import pytest


exec_path = os.getcwd()

control_dict = r"""/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  10
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{
    format      ascii;
    class       dictionary;
    location    "system";
    object      controlDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

application     simpleFoam;

startFrom       startTime;

startTime       0;

stopAt          endTime;

endTime         500;

deltaT          1;

writeControl    timeStep;

writeInterval   50;

purgeWrite      0;

writeFormat     ascii;

writePrecision  6;

writeCompression off;

timeFormat      general;

timePrecision   6;

runTimeModifiable true;


// ************************************************************************* //
"""


@pytest.fixture
def setup_tmp_cDict(tmp_path):
    f1 = tmp_path / "tmpControlDicts/controldict"
    f1.parent.mkdir()
    f1.touch
    f1.write_text(control_dict)
    return f1


def test_setup_parser(setup_tmp_cDict):
    parser = fd.FileParser(path=setup_tmp_cDict)
    assert isinstance(parser, fd.FileParser)


def test_parser_get(setup_tmp_cDict):
    parser = fd.FileParser(path=setup_tmp_cDict)

    w_prec = parser.get("writePrecision")  # should return 6
    t_prec = parser.get("timePrecision")  # should return 6
    e_time = parser.get("endTime")  # should return 500

    assert w_prec == 6
    assert t_prec == 6
    assert e_time == 500
