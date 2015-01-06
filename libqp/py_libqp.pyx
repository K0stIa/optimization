cimport c_libqp

cimport numpy
import numpy


cdef class py_libqp:
	
	cdef public int nIter
	cdef public double QP
	cdef public double QD
	cdef public int exitflag

	def __init__(self, nIter, QP, QD, exitflag):
		self.nIter = nIter
		self.QP =QP
		self.QD =QD
		self.exitflag = exitflag


def  py_libqp_splx_solver(Q, F, B,  x0, isEqualityConstrain, MaxIter, TolAbs, TolRel, QP_TH):
	cdef int mQ = Q.shape[0]
	cdef int nQ = Q.shape[1]
	cdef int mF = F.shape[0]
	cdef int mX0 = x0.shape[0]

	if numpy.isfortran(Q): Q = Q.reshape(Q.shape, order='C')

	Q = numpy.ascontiguousarray(Q, dtype = Q.dtype)
	F = numpy.ascontiguousarray(F.flatten('F'), dtype = F.dtype)
	x0 = numpy.ascontiguousarray(x0.flatten('F'), dtype = x0.dtype)

	cdef c_libqp.libqp_state  lib_state = c_libqp.libqp_splx_solver(<double*>numpy.PyArray_DATA(Q), mQ, nQ,
		<double*>numpy.PyArray_DATA(F), mF, 
		B,
		<double*>numpy.PyArray_DATA(x0), mX0,
		isEqualityConstrain,
		MaxIter,
		TolAbs,
		TolRel,
		QP_TH)

	libqp = py_libqp(lib_state.nIter, lib_state.QP, lib_state.QD, lib_state.exitflag)
	#del lib_state
	return x0, libqp