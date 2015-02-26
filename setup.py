from setuptools import setup

package_name = 'Owls'
# Get the version from FoamAna/version.py without importing the package
exec(compile(open(package_name + '/version.py').read(),
             package_name + '/version.py', 'exec'))

config = {
    'author': 'Gregor Olenik',
    'author_email': 'itvgo@itv.uni-stuttgart.de',
    'description': 'A simple library for reading and processing OpenFOAM data',
    'license': 'BSD',
    'version': __version__,
    'packages': [package_name],
    'install_requires': ['numpy',
                         'pandas',
                         'matplotlib',
                         'ipython',
                         'pyzmq',
                         'tornado',
                         'jinja2',
                         'bokeh==0.6.1',
                        ],
   'name': 'Owls' 
}


setup(**config)
