import os
import subprocess
import sys

from setuptools import setup

#from io import open

package_name = 'Owls'
# Fetch version from git tags, and write to version.py.
# Also, when git is not available (PyPi package), use stored version.py.
version_py = os.path.join(os.path.dirname(__file__), 'Owls/version.py')

#try:
#    version_git = subprocess.check_output(["git", "describe"], universal_newlines=True).rstrip()
#except:
#    with open(version_py, 'w') as fh:
#        version_git = open(version_py).read().strip().split('=')[-1].replace('"','')

#version_msg = "# Do not edit this file, pipeline versioning is governed by git tags"
#with open(version_py, 'w') as fh:
#    fh.write(version_msg + os.linesep + "__version__='{}'".format(version_git))

# Get the version from Owls/version.py without importing the package
# exec(compile(open(package_name + '/version.py').read(),
#              package_name + '/version.py', 'exec'))

packages = [
    'future',
    'numpy',
    'pandas',
    'functional',
    ]

if '--with-matplotlib' in sys.argv:
    packages.extend('matplotlib')

config = {
    'author': 'Gregor Olenik',
    'author_email': 'itvgo@itv.uni-stuttgart.de',
    'description': 'A simple library for reading and processing OpenFOAM data',
    'license': 'BSD',
    'version': version_git,
    'packages': [package_name],
    'install_requires': packages,
    'name': package_name,
    'zip_safe': False
}


setup(**config)
