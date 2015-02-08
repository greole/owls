import pytest
import os
import shutil

from Owls import io

@pytest.fixture
def create_directory_tree(tmpdir):
    def create_files(fold, files):
       for f in files:
           handle = fold.join(f)
           handle.write("foo")

    def create_times(basedir, times):
        for time in times:
            time_fold = basedir.mkdir(str(time))
            yield time_fold

    files = ["U", "UMean", "U_0", "foo.xy"]
    folders = range(10)
    folders.extend([str(float(_)) for _ in folders])
    folders.extend(["1.23e-09"])
    ignored = ["system", "constant", "0-bck", "0.old"]
    for folder in create_times(tmpdir, folders):
       particle_fold = folder.mkdir("lagrangian").mkdir("particleCloud1")
       create_files(folder, files)
       create_files(particle_fold, files)
    for folder in ignored:
       tmpdir.mkdir(folder)
    for sets_folder in create_times(tmpdir.mkdir("sets"), folders):
        create_files(sets_folder, files)
    folders_str = [str(f) for f in folders]
    ignored.append("sets")
    return tmpdir.dirname, folders_str, ignored, files

def test_finddatafolders(create_directory_tree):
    """ based on the  create_directory_tree fixture
        a list of folder to be found and ignored is
        passed, so we test if finds all in folders
        and none of ignored
    """
    from operator import truth
    from operator import contains
    from operator import not_

    test_dir = "/test_finddatafolders0/"

    base, folders, ignored, _ = create_directory_tree
    def _all(base, files, exp, negate=truth, expansion=""):
        for e in exp:
            abs_e = base + e + expansion
            # print abs_e, files
            if negate(contains(files, abs_e)):
                continue
            else:
                print "Failed on ", e
                return False
        return True

    eulerian = io.find_datafolders(
        regex=io.FPNUMBER,
        path=base + test_dir
    )
    assert _all(base+test_dir, eulerian, folders)
    assert _all(base+test_dir, eulerian, ignored, negate=not_)

    lagrangian = io.find_datafolders(
        regex=io.FPNUMBER + "/lagrangian/[\w]*Cloud1",
        path=base + test_dir
    )
    assert _all(base+test_dir, eulerian, ignored, negate=not_)
    assert _all(base+test_dir, lagrangian, ignored, negate=not_,
                    expansion="/lagrangian/particleCloud1")

    sets = io.find_datafolders(
        regex= "sets/" + io.FPNUMBER,
        path=base + test_dir
    )
    assert _all(base+test_dir + "sets/", sets, folders)
    assert _all(base+test_dir + "sets/", sets, ignored, negate=not_)

def test_findDataFiles(create_directory_tree):
    """ test if all files in the times folder are found """
    base, folders, ignored, files = create_directory_tree
    test_dir = base + "/test_findDataFiles0/"

    def _test(testdir, folders, files, result, extra=""):
        for search_fold in folders:
            for file_ in files:
                target = testdir + "{}{}/{}".format(search_fold, extra, file_)
                assert target in result[testdir + search_fold + extra]

    eulerian = io.find_datafiles(path=test_dir)
    _test(test_dir, folders, files, eulerian)

    sets = io.find_datafiles(path=test_dir, search="sets/" + io.FPNUMBER)
    _test(test_dir + "sets/", folders, files, sets)

    lagrangian = io.find_datafiles(path=test_dir, search=io.FPNUMBER + "/lagrangian/[\w]*Cloud[0-9]?")
    _test(test_dir, folders, files, lagrangian, extra="/lagrangian/particleCloud1")