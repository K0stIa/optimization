'''
Created on Feb 10, 2014

@author: kostia
'''

from distutils.core import setup, Extension
from Cython.Distutils import build_ext
import numpy.distutils.misc_util

include_dirs = numpy.distutils.misc_util.get_numpy_include_dirs() + ["."]

setup (name = "pyBMRM",
       version = "0.1",
       ext_modules = [Extension('cpp_bmrm',
                                ['c_bmrm_solver.pyx', 'bmrm_solver.cpp', 'libqp_splx.cpp'],
                                include_dirs=include_dirs,
                                language='c++'),
       		],
       cmdclass = {'build_ext': build_ext}
       )