import pytest

import os
import Owls as ow

exec_path = os.getcwd()

@pytest.fixture(scope="session")
def readEul():
    path = exec_path + "/examples/buoyantCavity"
    return ow.read_eul(folder=path, files=["T","U"], validate=False)

@pytest.fixture(scope="session")
def readSets():
    path = exec_path + "/examples/buoyantCavity"
    return ow.read_sets(folder=path, validate=False)

def test_eul(readEul):
    ff = readEul
    assert ff.times
    assert type(ff.latest)
    assert type(ff.filter('T', field=lambda x: x>293.0))

def test_sets(readSets):
    ff = readSets
    assert ff.times
    assert type(ff.latest)
    assert type(ff.filter('T', field=lambda x: x>293.0))
    assert ff.by_index('Loc')
