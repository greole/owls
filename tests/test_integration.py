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

@pytest.fixture(scope="session")
def readExp():
    path = exec_path + "/examples/buoyantCavity/sets/100"
    return ow.read_exp(folder=path, validate=False, search="")

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

def test_exp(readExp):
    ff = readExp
    assert ff.times
    ow.multi_merge(
        ff.latest.by_index('Loc'),
        ff.latest.by_index('Loc'),
        x='Pos', y='T')
