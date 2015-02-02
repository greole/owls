import pytest
import os
import shutil

from Owls import io

@pytest.fixture
def create_directory_tree(tmpdir):
    files = ["U", "UMean", "U_0", "foo.xy"]
    folders = range(10)
    folders.extend([str(float(_)) for _ in folders])
    folders.extend(["1.23e-09"]) 
    ignored = ["system", "constant", "0-bck", "0.old", "sets"]
    for folder in folders:
       time_fold = tmpdir.mkdir(str(folder))
       for f in files:
           handle = time_fold.join(f)
           handle.write("foo")
    for folder in ignored:
       tmpdir.mkdir(folder)
    folders_str = [str(f) for f in folders]
    return tmpdir.dirname, folders_str, ignored, files

def test_findtimes(create_directory_tree):
    """ based on the  create_directory_tree fixture 
        a list of folder to be found and ignored is
        passed, so we test if finds all in folders
        and none of ignored   
    """
    from operator import truth
    from operator import contains
    from operator import not_

    base, folders, ignored, _ = create_directory_tree
    def _all(files, exp, negate=truth):
        for e in exp:
            if negate(contains(files,e)):
                continue
            else:
                print "Failed on ", e
                return False
        return True
    
    found = io.find_times(base + "/test_findtimes0/")
    assert _all(found, folders)
    assert _all(found, ignored, negate=not_)

def test_findDataFiles(create_directory_tree):
    """ test if all files in the times folder are found """
    path, folders, ignored, files = create_directory_tree
    search_folds = [path + "/test_findDataFiles0/" + fold + "/" for fold in folders]
    found = io.find_datafiles(fold=search_folds)
    for search_fold in search_folds:
        for file_ in files:
            assert search_fold + file_ in found[search_fold] 
