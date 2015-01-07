#ifndef PY_LIBQP_H
#define PY_LIBQP_H

/** QP solver return value */
struct libqp_state{
    /** number of iterations */
    int nIter;
    /** primal objective value */
    double QP;
    /** dual objective value */
    double QD;
    /** exit flag */
    int exitflag;      /* -1 ... not enough memory
                          0 ... nIter >= MaxIter
                          1 ... QP - QD <= TolRel*ABS(QP)
                          2 ... QP - QD <= TolAbs
                          3 ... QP <= QP_TH
                          4 ... eps-KKT conditions satisfied */
    libqp_state(int nIter, double QP, double QD, int exitflag);
    libqp_state();
};


/** QP solver for tasks with simplex constraints */
struct libqp_state libqp_splx_solver(
                              double *Q, int mQ, int nQ,
                              double *F, int mF,
                              double B,
                              double *x0, int  mX0,
                              bool isEqualityConstrain,
                              int MaxIter,
                              double TolAbs,
                              double TolRel,
                              double QP_TH);

/* /\** Generalized SMO algorithm *\/ */
/* libqp_state_T libqp_gsmo_solver(const double* (*get_col)(int), */
/*                                 double *diag_H, */
/*                                 double *f, */
/*                                 double *a, */
/*                                 double b, */
/*                                 double *LB, */
/*                                 double *UB, */
/*                                 double *x, */
/*                                 int n, */
/*                                 int MaxIter, */
/*                                 double TolKKT, */
/*                                 void (*print_state)(libqp_state_T state)); */


#endif /* py_libqp_h */
