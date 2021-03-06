rm py_libqp_wrap.py py_libqp_wrap.pyc _py_libqp_wrap.so

swig -c++ -python  py_libqp.i

gcc -fPIC -c libqp_splx.cpp py_libqp.cpp py_libqp_wrap.cxx \
    -I/mnt/datagrid/personal/antonkos/usr/include/python2.7 \
    -I/mnt/datagrid/personal/antonkos/usr/lib/python2.7/site-packages/numpy/core/include \
    -I/mnt/datagrid/personal/antonkos/usr/lib/python2.7

g++ -shared  libqp_splx.o  py_libqp.o py_libqp_wrap.o -o _py_libqp.so

rm *.o
rm py_libqp_wrap.cxx
