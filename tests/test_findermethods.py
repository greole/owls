import pytest
import os
import shutil

from Owls import io

@pytest.fixture
def create_directory_tree(tmpdir):
    folders = range(10)
    folders.extend([str(float(_)) for _ in folders])
    folders.extend(["1.23e-09"]) 
    ignored = ["system", "constant", "0-bck", "0.old"]
    for folder in folders:
       tmpdir.mkdir(str(folder))
    for folder in ignored:
       tmpdir.mkdir(folder)
    return tmpdir.dirname, folders, ignored

def test_findtimes(create_directory_tree):
    base, folders, ignored = create_directory_tree
    def contains_all(files, exp):
        for e in exp:
            if str(e) in files:
                continue
            else:
                print "Missing ", e
                return False
        return True
    
    found = io.find_times(base + "/test_findtimes0/")
    assert contains_all(
        found,
        folders)
