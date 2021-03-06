rm bmrm.py bmrm.pyc _bmrm.so

swig -c++ -python  bmrm_solver.i

#CFLAGS=$(shell python-config --cflags)
#LDFLAGS=$(shell python-config --ldflags)

gcc -fPIC -c libqp_splx.cpp bmrm_solver.cpp bmrm_solver_wrap.cxx \
  -I/usr/local/Cellar/python/2.7.9/Frameworks/Python.framework/Versions/2.7/include/python2.7 \
  -I/usr/local/lib/python2.7/site-packages/numpy/core/include \
  -I/usr/local/Cellar/python/2.7.9/Frameworks/Python.framework/Versions/2.7/lib/python2.7

# -I/usr/include/python2.7 
#  -I/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/numpy/core/include \
#  -I/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python

# -lpython2.7
g++ -shared -L/usr/local/Cellar/python/2.7.9/Frameworks/Python.framework/Versions/2.7/lib -lpython2.7  libqp_splx.o  bmrm_solver.o bmrm_solver_wrap.o -o _bmrm.so

rm *.o
rm bmrm_solver_wrap.*
