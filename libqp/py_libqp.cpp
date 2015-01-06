#include <stdio.h>
#include "libqp.h"

#include "py_libqp.h"

static double *QQ;
static int nQQ;

const double* get_col(int idx) {
    return &QQ[idx*nQQ];
}

libqp_state libqp_splx_solver(
                              double *Q, int mQ, int nQ,
                              double *F, int mF,
                              double B,
                              double *x0, int  mX0,
                              bool isEqualityConstrain,
                              int MaxIter,
                              double TolAbs,
                              double TolRel,
                              double QP_TH) {

    if(B<=0) {
        printf("parameter B must be positive");
    }

    QQ = Q; nQQ = nQ;

    const int dim = nQ;
    int *I = new int[dim];
    int *S = new int[dim];
    double *b = new double[dim];
    double *diag = new double[dim];

    for (int i = 0; i < dim; ++i) {
        I[i] = 1;
        S[i] = int(isEqualityConstrain==0);
        b[i] = i==0 ? B : 0;
        diag[i] = Q[i*nQ+i];
        x0[i] = 0;
    }
    x0[0] = B;

    shogun::libqp_state_T state = shogun::libqp_splx_solver(get_col, diag, F, b, I, S, x0, dim,
                                                            MaxIter, TolAbs, TolRel, QP_TH, NULL);

    delete [] I;
    delete [] S;
    delete [] b;
    delete [] diag;
    QQ = NULL;
    //TODO: add return res tuple: (vector, stat)
    return libqp_state(state.nIter, state.QP, state.QD, state.exitflag);
}
