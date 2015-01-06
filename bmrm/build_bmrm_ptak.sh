rm  bmrm.pyc _bmrm.so
# bmrm.py

# swig -c++ -python  bmrm_solver.i

gcc -fPIC -c libqp_splx.cpp bmrm_solver.cpp bmrm_solver_wrap.cxx \
    -I/mnt/datagrid/personal/antonkos/usr/include/python2.7 \
    -I/mnt/datagrid/personal/antonkos/usr/lib/python2.7/site-packages/numpy/core/include \
    -I/mnt/datagrid/personal/antonkos/usr/lib/python2.7

g++ -shared  libqp_splx.o  bmrm_solver.o bmrm_solver_wrap.o -o _bmrm.so

rm *.o
#rm bmrm_solver_wrap.cxx bmrm_solver_wrap.h
