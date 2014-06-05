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

class AnalysisTest(unittest.TestCase):
	pass

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
