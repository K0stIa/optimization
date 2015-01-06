rm py_libqp_wrap.py py_libqp_wrap.pyc _py_libqp_wrap.so

swig -c++ -python  py_libqp.i

gcc -fPIC -c libqp_splx.cpp py_libqp.cpp py_libqp_wrap.cxx \
  -I/usr/include/python2.7 \
  -I/usr/lib/pymodules/python2.7/numpy/core/include \
  -I/usr/lib/pymodules/python2.7

g++ -shared  libqp_splx.o  py_libqp.o py_libqp_wrap.o -o _py_libqp.so

rm *.o
rm py_libqp_wrap.cxx