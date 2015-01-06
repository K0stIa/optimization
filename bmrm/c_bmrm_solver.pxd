cdef extern from "bmrm_solver.h":
    ctypedef struct bmrm_return_value_T:
         int nIter
         int nCP
         int nzA
         double Fp
         double Fd
         int qp_exitflag
         int exitflag