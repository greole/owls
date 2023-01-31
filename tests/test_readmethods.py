from __future__ import print_function
import pytest

from Owls import io
from test_findermethods import create_directory_tree


def test_readDataFiles(create_directory_tree):
    base, folders, ignored, files = create_directory_tree
    fn = base + "/test_readDataFiles0/sets/0/T"
    ret = io.read_data_file(fn, 1, 4)
    print(ret)
    # eulerian_decomp = io.import_foam_folder(
    #     path=test_dir,
    #     search="processor[0-9]\/" + io.FPNUMBER,
    #     files=['T'])
    # print(eulerian_decomp)
