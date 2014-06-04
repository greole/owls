from setuptools import setup

config = {
    'author': 'Gregor Olenik',
    'author_email': 'itvgo@itv.uni-stuttgart.de',
    'description': 'A simple library for reading and processing OpenFOAM data',
    'license': 'BSD',
    'version': '0.2.0',
    'packages': ['FoamAna'],
    'install_requires': ['numpy',
                         'pandas',
                         'matplotlib',
                         'ipython',
                         'pyzmq',
                         'tornado',
                        ],
   'name': 'FoamAna' 
}


setup(**config)
