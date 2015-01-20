import os

basepath = os.getcwd() + "/examples/buoyantCavity"
setspath = basepath + "/sets"


setsfiles = ['y0.1_T.xy', 'y0.1_U.xy', 'y0.2_T.xy', 'y0.2_U.xy', 'y0.3_T.xy', 'y0.3_U.xy', 'y0.4_T.xy', 'y0.4_U.xy', 'y0.5_T.xy', 'y0.5_U.xy', 'y0.6_T.xy', 'y0.6_U.xy', 'y0.7_T.xy', 'y0.7_U.xy', 'y0.8_T.xy', 'y0.8_U.xy', 'y0.9_T.xy', 'y0.9_U.xy']

basefiles = ['T', 'U', 'alphat', 'k', 'mut', 'omega', 'p', 'p_rgh', 'phi']

def test_imports():
    """ are the main modules importable """
    from Owls import io
    from Owls import frames

# def test_find_times():
#     import Owls as ow
#     ow.read_sets(folder=basepath)
    
def test_findtimes():
    """ are all times and times in sets found """
    from Owls import io
    def contains_all(res):
        times = [str(_*50) for _ in range(21)]
        return all([time in res for time in times])

    assert contains_all(io.find_times(fold=basepath))
    assert contains_all(io.find_times(fold=setspath))

def test_findDataFiles():
    """ are all files in the the sets and times folder are found """
    from Owls import io
    read_folder = lambda x=False,filt=False: [path.replace(x,'') for path in io._get_datafiles_from_dir(x, filt)]
    setsfolder = setspath + "/1000/"
    basefolder = basepath + "/1000/"
    datafilessets = read_folder(setsfolder)
    datafilesbase = read_folder(basefolder)
    assert setsfiles == datafilessets
    assert basefiles == datafilesbase
    for fn in basefiles:
        # print read_folder(basefolder,fn)
        assert [fn] == read_folder(basefolder,[fn])
