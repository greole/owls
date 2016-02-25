#!/usr/bin/python
"""
    Usage:
        animSnapshots.py [options]

    Options:
        -h --help           Show this screen
        -d --decomposed     Case is decomposed
        -a --all            Process all times, otherwise last time step only
        -i --interpolate    Write images with interpolated fields
        --watch=<dir0,dir1> leave snappy alive and make snapshots continuosly
        --nlatest=num       Process only n latest time steps
        --slice=dir         Slice normal, default=y
        --config=file       Specify config file
        --json_config=str   Specify config file
        --vectors=fields    Explicit list of vector fields to read
        --scalars=fields    Explicit list of vector fields to read
        --gif               Create gifs
        --clean             Remove existing anim folder
        --update            Write till latest previously written snapshot
        --force             Force overwriting old snapshots #TODO
"""

import os, sys
pv_path = '/home/gregor/Downloads/paraview-build'
sys.path.append('%s/lib' % pv_path)
sys.path.append('%s/lib/site-packages' % pv_path)

import json
from paraview.simple import *
from paraview import servermanager
import numpy as np
from docopt import docopt
import subprocess
import shutil
from copy import deepcopy
import time
#os.environ['DISPLAY'] = ":0"

testlut="""<ColorMaps>
<ColorMap name="testlut" space="RGB" indexedLookup="false">
  <Point x="1.86486" o="0" r="0.0392157" g="0.0392157" b="0.94902"/>
  <Point x="70.1081" o="0.6954" r="0" g="1" b="0"/>
  <Point x="100" o="1" r="0.94902" g="0.94902" b="0.0392157"/>
  <NaN r="1" g="0" b="0"/>
</ColorMap>
</ColorMaps>"""
#'ColorAttributeType' is obsolete. Simply use 'ColorArrayName' instead.  Refer to ParaView Python API changes documentation online.

def make_color_map(servermanager):
    color_map = servermanager.rendering.ScalarBarWidgetRepresentation()
    color_map.LabelColor = [0, 0, 0]
    color_map.TitleColor = [0, 0, 0]
    color_map.LabelFontSize = 12
    color_map.TitleFontSize = 12
    color_map.TitleBold = 1
    color_map.AspectRatio = 15
    color_map.Position = [0.8, 0.25]
    #color_map.Orientation ='Horizontal'
    return color_map


def camera_offset(alpha, bds):
    delta_z = abs(bds[4] - bds[5])
    delta_y = abs(bds[3] - bds[2])
    delta_x = abs(bds[1] - bds[0])
    g = (lambda delta: np.arctan(alpha * 90/3.1415) * delta)
    offs = 1.5*max(g(delta_x), g(delta_z), g(delta_y))
    return offs


def center_camera(bds):
    h = (lambda x, y: 0.5*(x+y))
    x = h(bds[1], bds[0])
    y = h(bds[3], bds[2])
    z = h(bds[5], bds[4])
    return [x, y, z]


def set_up_time_annotator():
    #annTime = AnnotateTimeFilter(reader)           # Time annotator
    #annTimeRepr = GetDisplayProperties(annTime)
    #annTimeRepr.Color=[0,0,0]                      # make time color black
    pass


def attachToDict(dict_, str_):
    d = dict_.keys()
    for k in d:
        if k+str_ not in d: dict_.update({k + str_: dict_[k]})


def field_names(reader):
    "return cell data field names, does not include lagrangian names"
    fields = reader.CellData.items()
    return [f[0] for f in fields]

def convert_to_gif(slices, fields):
    for s in slices:
        for field in fields:
            try:
                path = "postProcessing/anim/{}{}".format(s, field)
                src = path + "_*.png"
                dst = path + ".mp4"
                com = "ffmpeg -y -r 7.5 -pattern_type glob -i '{}' -c:v libx264 -vf 'fps=25,format=yuv420p' {}".format(src, dst)
                out = subprocess.check_output(com, shell=True)
            except Exception as e:
                print e

class animator():
    """  wrapper class to handle python-paraview """

    def __init__(self,
             animate=False,
             decomposed=False,
             config=False,
             json_config=False,
             interpolate=False,
             update=False,
             cam_shift=1,
             cam_view_up=2,
             slice_normal=[0, -1, 0],
             ntimes=1,
             vectors=False,
             scalars=False,
            ):

        self.slice_normal = slice_normal
        self.cam_shift = cam_shift
        self.cam_view_up = cam_view_up
        self.anim = animate
        self.decomp = decomposed
        if config:
            self.conf = self.read_config(config)
        if json_config:
            self.conf = json.loads(json_config)
        self.path = os.getcwd()
        self.scalars = (self.conf['scalars'] if not scalars else {key: ('auto', 'Blues') for key in scalars.split(',')})
        self.vectors = (self.conf['vectors'] if not vectors else {key: ('auto', 'Blues') for key in vectors.split(',')})
        self.ntimes = ntimes
        self.interpolate = interpolate
        self.autoscaled = {}
        attachToDict(self.scalars, "Mean")
        #attachToDict(self.vectors, "Mean")
        # attachToDict(self.vectors, "Prime2Mean")
        Connect()
        self.create_reader()
        self.stop = False
        self.setup_view()
        self.color_map = self.create_colormap()
        self.setup_camera()
        self.set_times()

    def read_config(self, fn):
        """ read config file from script loc if no fn is given """
        fn = (fn if fn else os.path.dirname(os.path.realpath(__file__)) + '/readfiles.cfg')
        return json.load(open(fn))

    def create_reader(self):
        cdict = self.path + '/system/controlDict.foam'
        print "reading case data",
        self.reader = OpenDataFile(cdict)

        caseType = ('Decomposed Case' if self.decomp else 'Reconstructed Case')
        self.reader.CaseType = caseType
        self.has_changed()
        print "\t[done]"

    def has_changed(self):
        self.reader.FileNameChanged()

    def set_times(self):
        "read all or latest ts from reader"
        times = self.reader.TimestepValues
        self.total_times = len(times)

        self.times = (times[::-1][:self.ntimes] if not self.anim else times[::-1])

    def setup_view(self, image_size=[780, 780]):
       self.view = CreateRenderView()
       self.view.StillRender = 1
       self.view.Background = [1, 1, 1]       # make background white
       self.view.CenterAxesVisibility = 0     # hide the center axis
       self.view.ViewSize = image_size

    def create_colormap(self):
        color_map = make_color_map(servermanager)
        self.view.Representations.append(color_map)
        return color_map

    def slice_domain(self, slice_normal, slice_origin):
        if slice_normal==[0,1,0]:
            self.cam_shift = 1
            self.cam_view_up = 2
        elif slice_normal==[0,0,1]:
            self.cam_shift = 2
            self.cam_view_up = 1
        elif slice_normal==[1,0,0]:
            self.cam_shift = 0
            self.cam_view_up = 2
        self.setup_camera()
        slice = Slice(self.reader)              # make a slice
        slice.SliceType.Normal = slice_normal   # set the slice normal
        slice.SliceType.Origin = slice_origin   # set the slice normal
        reprSlice = servermanager.CreateRepresentation(slice, self.view)
        reprSlice.Representation = 'Surface'
        return reprSlice

    def setup_camera(self):
        self.cam = self.view.GetActiveCamera()
        self.view.ResetCamera()
        bound_box = self.reader.GetDataInformation().GetBounds()
        cam_pos = center_camera(bound_box)
        self.view.CameraFocalPoint = cam_pos
        cam_pos[self.cam_shift] += camera_offset(self.cam.GetViewAngle(), bound_box)
        self.view.CameraPosition = cam_pos
        self.view.CameraViewUp = [0, 0, 0]
        self.view.CameraViewUp[self.cam_view_up] = 1
        self.view.OrientationAxesVisibility = 0
        #camera_position=camera.GetPosition()
        #camera_focal_point=camera.GetFocalPoint()


    def write_all_fields(self):
        for time_nr, t in enumerate(self.times):
            self.reprSlice = self.slice_domain([0,0,1], [0,0,0])
            self.reprSlice.Visibility = False
            for slice_name, (slice_origin, slice_normal) in self.conf['slices'].iteritems():
                self.reprSlice = self.slice_domain(slice_normal, slice_origin)
                self.reprSlice.Visibility = True
                print self.reprSlice.Visibility
                self.view.ViewTime = t
                self.frame_nr = self.total_times - time_nr
                print t
                self.has_changed()
                vectors = deepcopy(self.vectors)
                link = True if time_nr == 0 else False
                for field, (limits, lut_name) in vectors.iteritems():
                    try:
                        self.display_vector_field(field, limits, str(lut_name), slice_dir=slice_name, link=link)
                    except Exception as e:
                        print e
                scalars = deepcopy(self.scalars)
                for field, (limits, lut_name) in scalars.iteritems():
                    try:
                        self.display_scalar(field, limits, str(lut_name), slice_dir=slice_name, link=link)
                    except Exception as e:
                        print e
                if self.stop:
                    print "STOP"
                    break
                self.reprSlice.Visibility = False

    def display_vector_field(self, name, lim, lut_name, slice_dir, link):
        if name not in self.reader.CellData.keys():
            return
        ncomps = (3 if lim =="auto" else len(lim))
        for j in range(ncomps):
            self.set_field(name)
            if lim == 'auto':
               idx = self.reader.CellData.keys().index(name)
               arr = self.reader.CellData[idx]
               lim = arr.GetRange()
               self.vectors[name][0] = [lim, lim, lim]
            elif self.vectors.get(name, False):
                lim = self.vectors[name][0][j]
            # print self.reader.CellData.keys().index(name)
            lt = AssignLookupTable(self.reader.CellData[j], lut_name, lim)
            lt.VectorMode = "Component" # Magnitude
            lt.VectorComponent = j
            self.reprSlice.LookupTable = lt
            self.color_map.LookupTable = lt
            self.write_image(name, j, slice_dir=slice_dir, link=link)

    def display_scalar(self, name, lim, lut_name, slice_dir, link):
        if name not in self.reader.CellData.keys():
            return
        self.set_field(name)
        if lim == 'auto':
           idx = self.reader.CellData.keys().index(name)
           arr = self.reader.CellData[idx]
           lim = arr.GetRange()
           self.scalars[name][0] = lim
        elif self.scalars.get(name, False):
            lim = self.scalars[name][0]
        lt = AssignLookupTable(self.reader.CellData[0], lut_name, lim)
        self.reprSlice.LookupTable = lt
        self.color_map.LookupTable = lt
        self.write_image(name, slice_dir=slice_dir, link=link)

    def set_field(self, name):
        #reprSlice.MeshVisibility = 1
        _ = ('POINTS' if self.interpolate else 'CELLS')
        self.reprSlice.ColorArrayName = (_, str(name))
        self.color_map.Title = str(name)

    def write_image(self, name, component=0, slice_dir='z', link=False):
        image_name = "{}/postProcessing/anim/{}{}_{}_{}.png".format(self.path,
                                         slice_dir,
                                         name,
                                         component,
                                         str(self.frame_nr).zfill(4),
                                         # self.view.ViewTime
                                         )

        if os.path.exists(image_name) and self.update:
            print 'STOP'
            self.stop = True
            return 0

        WriteImage(image_name)
        if link:
            image_name = "{}/postProcessing/anim/last_{}{}_{}.png".format(self.path,
                                             slice_dir,
                                             name,
                                             component,
                                             )
            WriteImage(image_name)

        print "written : " + image_name.split('/')[-1]

def main(arguments):

    if arguments['--clean']: shutil.rmtree('anim')
    if not os.path.exists('postProcessing/anim'): os.makedirs('postProcessing/anim')
    #fetch_fields = (False if arguments['--all-fields'] else True)
    cam_shift = cam_view_up = slice_normal = False

    if arguments['--nlatest'] and arguments['--all']:
        print "cannot use --nlatest and --all at the same time"
        sys.exit()

    if not arguments['--slice']:
        cam_shift = 1
        cam_view_up = 2
        slice_normal = [0, 1, 0]
    elif arguments['--slice'] == 'z':
        cam_shift = 2
        cam_view_up = 1
        slice_normal = [0, 0, 1]
    elif arguments['--slice'] == 'x':
        cam_shift = 2
        cam_view_up = 1
        slice_normal = [1, 0, 0]

    anim = animator(
        animate=arguments['--all'],
        decomposed=arguments['--decomposed'],
        config=arguments.get('--config', False),
        json_config=arguments.get('--json_config', False),
        interpolate=arguments['--interpolate'],
        update=arguments['--update'],
        cam_shift=cam_shift,
        cam_view_up=cam_view_up,
        slice_normal=slice_normal,
        ntimes=(int(arguments['--nlatest']) if arguments['--nlatest'] else 1),
        vectors=arguments['--vectors'],
        scalars=arguments['--scalars'],
        )

    anim.write_all_fields()

    if arguments['--gif']:
        convert_to_gif(anim.conf['slices'].keys(), anim.scalars)
        convert_to_gif(anim.conf['slices'].keys(), anim.vectors)

def latestTime(arguments):
    p = "./processor0/"
    return max([p + _ for _ in os.listdir(p)], key = os.path.getctime)

if __name__ == '__main__':
    arguments = docopt(__doc__)
    if arguments['--watch']:
        from collections import defaultdict
        old_latest_time = defaultdict(int)
        cases  = arguments['--watch'].split(',')
        while True:
            for case in cases:
                old_pwd = os.getcwd()
                os.chdir(case)
                print "waiting"
                latestTime_ = latestTime(arguments)
                if latestTime_ != old_latest_time[case]:
                    try:
                        old_latest_time[case] = latestTime_
                        main(arguments)
                    except Exception as e:
                        print e
                os.chdir(old_pwd)
                time.sleep(60)
    else:
        main(arguments)
