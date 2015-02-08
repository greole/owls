#__all__ = ["case", "plot", "analysis"]
import os

owls_path = os.path.expanduser('~') + "/.owls"
if not os.path.exists(owls_path):
    os.makedirs(owls_path)

from .version import __version__
from io import *
from plot import *
from foam import *
from frames import *

print "Owls Version: " + __version__
