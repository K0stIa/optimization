rm  bmrm.pyc _bmrm.so
# bmrm.py

# swig -c++ -python  bmrm_solver.i

gcc -fPIC -c libqp_splx.cpp bmrm_solver.cpp bmrm_solver_wrap.cxx \
  -I/usr/include/python2.7 \
  -I/usr/lib/pymodules/python2.7/numpy/core/include \
  -I/usr/lib/pymodules/python2.7

g++ -shared  libqp_splx.o  bmrm_solver.o bmrm_solver_wrap.o -o _bmrm.so

rm *.o
#rm bmrm_solver_wrap.cxx bmrm_solver_wrap.h
