import pytest
import os
import shutil

from Owls import io

@pytest.fixture
def create_directory_tree(tmpdir):
    def create_files(fold, files):
       mock_data = "\n".join(["1 2", "3 4", "5 6"])
       for f in files:
           handle = fold.join(f)
           handle.write(mock_data)

    def create_times(basedir, times):
        for time in times:
            time_fold = basedir.mkdir(str(time))
            yield time_fold

    files = ["U", "UMean", "U_0", "foo.xy", "T"]
    folders = list(range(10))
    folders.extend([str(float(_)) for _ in folders])
    folders.extend(["1.23e-09"])
    ignored = ["system", "constant", "0-bck", "0.old"]

    for prc_nr in range(4):
        proc_dir = tmpdir.mkdir("processor" + str(prc_nr))
        for folder in create_times(proc_dir, folders):
            create_files(folder, files)

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


    base, folders, ignored, _ = create_directory_tree
    def _all(base, files, exp, negate=truth, expansion=""):
        for e in exp:
            abs_e = base + e + expansion
            # print abs_e, files
            if negate(contains(files, abs_e)):
                continue
            else:
                print(("Failed on ", e))
                return False
        return True

    fold = os.path.join(base, "test_finddatafolders0") + "/"

    eulerian = io.find_datafolders(io.FPNUMBER, fold, slice="all")

    assert _all(fold, eulerian, folders)
    assert _all(fold, eulerian, ignored, negate=not_)

    lagrangian = io.find_datafolders(
        regex=io.FPNUMBER + "/lagrangian/[\w]*Cloud1",
        path=fold,
        slice="all"
    )

    assert _all(fold, eulerian, ignored, negate=not_)
    assert _all(fold, lagrangian, ignored, negate=not_,
                    expansion="/lagrangian/particleCloud1")

    sets = io.find_datafolders(
        regex= "sets/" + io.FPNUMBER,
        path=fold,
        slice="all"
    )

    assert _all(fold + "sets/", sets, folders)
    assert _all(fold + "sets/", sets, ignored, negate=not_)

    eulerian_decomp = io.find_datafolders(
        regex="processor[0-9]\/" + io.FPNUMBER,
        path=fold,
        slice="all"
    )

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
    els_eulerian = len(eulerian)
    _test(test_dir, folders, files, eulerian)

    sets = io.find_datafiles(path=test_dir, search="sets/" + io.FPNUMBER)
    _test(test_dir + "sets/", folders, files, sets)

    lagrangian = io.find_datafiles(path=test_dir, search=io.FPNUMBER + "/lagrangian/[\w]*Cloud[0-9]?")
    _test(test_dir, folders, files, lagrangian, extra="/lagrangian/particleCloud1")

    eulerian_decomp = io.find_datafiles(path=test_dir, search="processor[0-9]\/" + io.FPNUMBER)
    els_eulerian_decomp = len(eulerian_decomp)

    assert els_eulerian * 4 == els_eulerian_decomp
