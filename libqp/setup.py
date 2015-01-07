# -*- coding: utf-8 -*-
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

import numpy as np

setup(
    name="lib_qp",
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("py_libqp", ["py_libqp.pyx", "c_libqp.cpp", "libqp_splx.cpp"],
                             include_dirs = [np.get_include(),'.'],
                             language="c++",
                             extra_compile_args=['-O3'])],
    py_modules = ['py_libqp']
)

# setup(ext_modules = cythonize(
#            "py_libqp.pyx",                 # our Cython source
#            sources=["c_libqp.cpp", "libqp_splx.cpp"],  # additional source file(s)
#            language="c++",             # generate C++ code
#       ),
# include_dirs = [np.get_include(),'.'])