cdef extern from "c_libqp.h":
	cdef struct libqp_state:             
		libqp_state(int, double, double, int)
		double QP
		double QD
		int nIter
		int exitflag

	libqp_state libqp_splx_solver(
		double *, int, int,
		double *, int,
		double,
		double *, int,
		bool,
		int,
		double,
		double,
		double)