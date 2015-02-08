import pytest

import os
import Owls as ow

exec_path = os.getcwd()

def test_readEul():
    path = exec_path + "/examples/buoyantCavity"
    ow.read_eul(folder=path, files=["T","U"], validate=False)

def test_readSets():
    path = exec_path + "/examples/buoyantCavity"
    ow.read_sets(folder=path, validate=False)
