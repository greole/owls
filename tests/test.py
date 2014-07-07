import pandas as pd
import unittest
from mock import Mock
from FoamAna import *

input_filenames = ["0/U",
	  "0/lagrangian/coalCloud1/U",
	  "0/lagrangian/coalCloud1/positions",
	  "0/sets/X0_U_UMean_UPrime2Mean_T.xy",
	  "0/sets/X+85_T.xy",
	 ]

expected_fieldnames = [["u","v","w"],
	  ["u","v","w"],
	  ["positions_0","positions_1","positions_2","positions_3"],
	  ["X0","X0_u","X0_v","X0_w","X0_uMean","X0_vMean","X0_wMean",
	   "X0_uu","X0_uv","X0_uw","X0_vv","X0_vw","X0_ww","X0_T"],
	  ["X+85","X+85_T"],
	 ]

file_entries = [3, 3, 4, 14, 2,]

filename_to_fieldnames = zip(input_filenames,
                         expected_fieldnames,
                         file_entries,
                         )

expected_times = ['1000','900', '950' , '0']
expected_times_in_sets = ['1000']

u_set = pd.Series([0, 0.00217143, 0.00434286, 0.00651429, 0.00868571, 0.0108571,
    0.0130286, 0.0152, 0.0173714, 0.0195429, 0.0217143, 0.0238857, 0.0260571,
    0.0282286, 0.0304, 0.0325714, 0.0347429, 0.0369143, 0.0390857, 0.0412571,
    0.0434286, 0.0456, 0.0477714, 0.0499429, 0.0521143, 0.0542857, 0.0564571,
    0.0586286, 0.0608, 0.0629714, 0.0651429, 0.0673143, 0.0694857, 0.0716571,
    0.0738286, 0.076])

class AnalysisTest(unittest.TestCase):

    def test_Foam_to_DataFrame_eul(self):
        input_file = "examples/buoyantCavity/1000/U"
        test, data = read_data_file(input_file)
        self.assertEqual(data['u'][78749], 0.00447051)
        self.assertEqual(len(data),78750)

    def test_Foam_to_DataFrame_sets(self):
        input_file = "examples/buoyantCavity/sets/1000/y0.1_U.xy"
        test, data = read_data_file(input_file)
        isEqual = (u_set == data['y0.1'])
        self.assertTrue(isEqual.all())

    def test_find_times(self):
        input_folder = "examples/buoyantCavity/"
        times = sorted(find_times(input_folder))
        self.assertEqual(times,sorted(expected_times))

    def test_find_times_sets(self):
        input_folder = "examples/buoyantCavity/sets/"
        times = sorted(find_times(input_folder))
        self.assertEqual(times,sorted(expected_times_in_sets))

    def test_get_datafiles_from_dir_with_filelist(self):
        import FoamAna as FA
        found = FA.analysis._get_datafiles_from_dir("examples/buoyantCavity/950",['U'])
        self.assertEqual(['examples/buoyantCavity/950/U'],found)

def test_names_generator(filename, expect, entries):
    def test_evaluate_field_names(self):
        names = evaluate_names(filename, entries)
        self.assertEqual(names, expect)
    return test_evaluate_field_names

if __name__ == '__main__':
    for filename, fieldnames, entries in filename_to_fieldnames:
        base = "/home/go/"
        test_name = 'test_%s' % filename
        test = test_names_generator(filename, fieldnames, entries)
        setattr(AnalysisTest, test_name, test)
    unittest.main()
