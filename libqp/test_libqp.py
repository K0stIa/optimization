import py_libqp as libqp
import numpy as np


dim = 2
Q = np.array([[1,0],[0,1]],dtype=np.double)
F = np.zeros(dim)
B = 1
x0 = np.array([0.3,0.7], dtype=np.double)

max_iter = 1000
tol_abs = 0
tol_rel = 1e-9
qp_th = -np.inf

state = libqp.libqp_splx_solver(Q, F, B, x0, True, max_iter, tol_abs, tol_rel, qp_th)
print state.nIter, state.QP, state.QD, state.exitflag
print x0
