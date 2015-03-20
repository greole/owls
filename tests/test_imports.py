import os

exec_path = "/home/go/documents/code/Owls"

def test_imports():
    """ are the main modules importable """
    from Owls import io
    from Owls import FoamFrame
    from Owls import MultiFrame
    from Owls import foam
    from Owls import plotinterface


def test_importFoamFolder():
    from Owls import io
    path = exec_path + "/examples/buoyantCavity/"
    euls =  io.import_foam_folder(
        path=path,
        search=io.FPNUMBER,
        files=['T','U'],
    )
    sets =  io.import_foam_folder(
        path=path,
        search="sets/" + io.FPNUMBER,
        files=False,
    )
