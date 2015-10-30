import numpy as np
from . import io


class Mesh():

    def __init__(self, path):
        self.path = path + "/constant/polyMesh/"
        print("reading mesh", end="")
        self.df = io.import_foam_mesh(path)
        print(" [done]\ncomputing face centres ", end="")
        self.faceCtr = self.compute_faceCentres()
        print("[done]\ncomputing cell centres ", end="")
        self.cellCtrs = self.compute_centres()
        print("[done]")

    def clean(self, name):
        return (self.df[self.path + name].reset_index(level=['Loc','Id'], drop=True))

    @property
    def owner(self):
        o = "owner"
        return self.clean(o)[o]

    @property
    def neighbour(self):
        n = "neighbour"
        return self.clean(n)[n]

    @property
    def faces(self):
        return self.clean("faces")

    @property
    def points(self):
        return self.clean("points")


    def compute_faceCentres(self):
        faceCtrsX = lambda x: self.points.ix[self.faces[x].values.astype(int)].reset_index(drop=True)
        faceCtrs = faceCtrsX("faces_0")
        for i, f in enumerate(self.faces):
            if i == 0:
                continue
            faceCtrs = faceCtrs.add(faceCtrsX(f), fill_value=0.0)
        return faceCtrs/4.0

    def compute_centres(self):
        """ compute cell centres for given mesh """
        # As in primitiveMesh.H we compute an approx.
        # cell centre first as the average of the face centres
        o = self.faceCtr.set_index(mesh.owner).sort_index()
        n = self.faceCtr[0:len(self.neighbour)].set_index(self.neighbour).sort_index()
        return o.append(n).groupby(level=0).mean()

    def line(self, start, end):
        pass
