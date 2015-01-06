from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [
    Extension("elps", 
              sources=["elps.pyx", "src/ITestClass.cpp"],
              include_dirs=["."],
              language="c++"
              )
    ]
)