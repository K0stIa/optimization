rm bmrm.py bmrm.pyc _bmrm.so

gcc -fPIC -c libqp_splx.cpp bmrm_solver.cpp bmrm_solver_wrap.cxx \
    -I/System/Library/Frameworks/Python.framework/Versions/2.7/include/python2.7 \
    -I/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/numpy/core/include \
    -I/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7

g++ -shared  libqp_splx.o  bmrm_solver.o bmrm_solver_wrap.o -o _bmrm.so

rm *.o
# rm bmrm_solver_wrap.cxx bmrm_solver_wrap.h
