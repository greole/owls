from __future__  import print_function
import os

owls_path = os.path.expanduser('~') + "/.owls"
if not os.path.exists(owls_path):
    os.makedirs(owls_path)

from .version import __version__
# from . import io
from .plot import *
# from .foam import *
from .FoamFrame import *
from .MultiFrame import *

from future.builtins import *
print("Owls Version: " + __version__)

try:
  from mplinterface import *
except:
  print("Warning no matplotlib support")
