/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * libbmrm.h: Implementation of the BMRM solver for SO training
 *
 * Copyright (C) 2012 Michal Uricar, uricamic@cmp.felk.cvut.cz
 *
 * Implementation of the BMRM solver
 *--------------------------------------------------------------------- */

#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "libbmrm.h"
#include "libqp.h"

namespace shogun
{
    static const int QPSolverMaxIter = 10000000;
    static const double epsilon = 0.0000000001;

    static double *H;
    static int BufSize;

    /*----------------------------------------------------------------------
      Returns pointer at i-th column of Hessian matrix.
      ----------------------------------------------------------------------*/
    static const double *get_col( int i)
    {
        return( &H[ BufSize*i ] );
    }

    bmrm_return_value_T svm_bmrm_solver(
                                        double*      W,
                                        double       TolRel,
                                        double       TolAbs,
                                        double       lambda,
                                        int        _BufSize,
                                        CRiskFunction*  risk_function)
    {
	bmrm_return_value_T bmrm = {0, 0, 0, 0, 0, 0, 0};
	libqp_state_T qp_exitflag;
	double *b, *beta, *diag_H, sq_norm_W;
	double R, *subgrad, *A, QPSolverTolRel, rsum, C = 1.0;
	int *I;
	uint8_t S = 1;
	int nDim=risk_function->get_dim();
	// CTime ttime;
	// double tstart, tstop;

	// tstart=ttime.cur_time_diff(false);

	BufSize = _BufSize;
	QPSolverTolRel = TolRel*0.5;

	H=NULL;
	b=NULL;
	beta=NULL;
	A=NULL;
	subgrad=NULL;
	diag_H = NULL;
	I = NULL;

	H = (double*)LIBBMRM_CALLOC(BufSize*BufSize, sizeof(double));
	if (H == NULL)
	{
            bmrm.exitflag = -2;
            goto cleanup;
	}

	A = (double*)LIBBMRM_CALLOC(nDim*BufSize, sizeof(double));
	if (A == NULL)
	{
            bmrm.exitflag = -2;
            goto cleanup;
	}

	b = (double*)LIBBMRM_CALLOC(BufSize, sizeof(double));
	if (b == NULL)
	{
            bmrm.exitflag = -2;
            goto cleanup;
	}

	beta = (double*)LIBBMRM_CALLOC(BufSize, sizeof(double));
	if (beta == NULL)
	{
            bmrm.exitflag = -2;
            goto cleanup;
	}

	subgrad = (double*)LIBBMRM_CALLOC(nDim, sizeof(double));
	if (subgrad == NULL)
	{
            bmrm.exitflag = -2;
            goto cleanup;
	}

	diag_H = (double*)LIBBMRM_CALLOC(BufSize, sizeof(double));
	if (diag_H == NULL)
	{
            bmrm.exitflag = -2;
            goto cleanup;
	}

	I = (int*)LIBBMRM_CALLOC(BufSize, sizeof(int));
	if (I == NULL)
	{
            bmrm.exitflag = -2;
            goto cleanup;
	}

	/* Iinitial solution */
	R = risk_function->risk(W, subgrad);

	bmrm.nCP = 0;
	bmrm.nIter = 0;
	bmrm.exitflag = 0;

	b[0] = -R;
	LIBBMRM_MEMCPY(A, subgrad, nDim*sizeof(double));

	/* Compute initial value of Fp, Fd, assuming that W is zero vector */
	sq_norm_W = 0;
	bmrm.Fp = R + 0.5*lambda*sq_norm_W;
	bmrm.Fd = -LIBBMRM_PLUS_INF;

	// tstop=ttime.cur_time_diff(false);

	/* Verbose output */
	// SG_SPRINT("%4d: tim=%.3f, Fp=%f, Fd=%f, R=%f\n",
        //           bmrm.nIter, tstop-tstart, bmrm.Fp, bmrm.Fd, R);

	/* main loop */
	while (bmrm.exitflag == 0)
	{
            // tstart=ttime.cur_time_diff(false);
            bmrm.nIter++;

            /* Update H */
            if (bmrm.nCP > 0)
            {
                for (int i = 0; i < bmrm.nCP; i++)
                {
                    rsum = 0.0;
                    for (int j = 0; j < nDim; j++)
                    {
                        rsum += A[LIBBMRM_INDEX(j, i, nDim)]*A[LIBBMRM_INDEX(j, bmrm.nCP, nDim)];
                    }
                    H[LIBBMRM_INDEX(i, bmrm.nCP, BufSize)] = rsum/lambda;
                }
                for (int i = 0; i < bmrm.nCP; i++)
                {
                    H[LIBBMRM_INDEX(bmrm.nCP, i, BufSize)] = H[LIBBMRM_INDEX(i, bmrm.nCP, BufSize)];
                }
            }
            //H[LIBBMRM_INDEX(bmrm.nCP, bmrm.nCP, BufSize)] = 0.0;

            for (int i = 0; i < nDim; i++)
                H[LIBBMRM_INDEX(bmrm.nCP, bmrm.nCP, BufSize)] += A[LIBBMRM_INDEX(i, bmrm.nCP, nDim)]*A[LIBBMRM_INDEX(i, bmrm.nCP, nDim)]/lambda;

            diag_H[bmrm.nCP] = H[LIBBMRM_INDEX(bmrm.nCP, bmrm.nCP, BufSize)];
            I[bmrm.nCP] = 1;

            bmrm.nCP++;

            /* call QP solver */
            qp_exitflag = libqp_splx_solver(&get_col, diag_H, b, &C, I, &S, beta,
                                            bmrm.nCP, QPSolverMaxIter, 0.0, QPSolverTolRel, -LIBBMRM_PLUS_INF, 0);

            bmrm.qp_exitflag = qp_exitflag.exitflag;

            /* W update */
            for (int i = 0; i < nDim; ++i)
            {
                rsum = 0.0;
                for (int j = 0; j < bmrm.nCP; ++j)
                {
                    rsum += A[LIBBMRM_INDEX(i, j, nDim)]*beta[j];
                }
                W[i] = -rsum/lambda;
            }

            /* compute number of active cutting planes */
            bmrm.nzA = 0;
            for (int aaa=0; aaa<bmrm.nCP; ++aaa)
                bmrm.nzA += (beta[aaa] > epsilon) ? 1 : 0;

            /* risk and subgradient computation */
            R = risk_function->risk(W, subgrad);
            LIBBMRM_MEMCPY(A+bmrm.nCP*nDim, subgrad, nDim*sizeof(double));
            b[bmrm.nCP] = -R;
            for (int j = 0; j < nDim; j++)
                b[bmrm.nCP] += subgrad[j]*W[j];

            sq_norm_W = 0;
            for (int j = 0; j < nDim; j++)
                sq_norm_W += W[j]*W[j];

            bmrm.Fp = R + 0.5*lambda*sq_norm_W;
            bmrm.Fd = -qp_exitflag.QP;

            /* Stopping conditions */
            if (bmrm.Fp - bmrm.Fd <= TolRel*LIBBMRM_ABS(bmrm.Fp)) bmrm.exitflag = 1;
            if (bmrm.Fp - bmrm.Fd <= TolAbs) bmrm.exitflag = 2;
            if (bmrm.nCP >= BufSize) bmrm.exitflag = -1;

            // tstop=ttime.cur_time_diff(false);

            // Verbose output
            printf("%4d: Fp=%f, Fd=%f, (Fp-Fd)=%f, (Fp-Fd)/Fp=%f, R=%f, nCP=%d, nzA=%d\n",
                      bmrm.nIter, bmrm.Fp, bmrm.Fd, bmrm.Fp-bmrm.Fd, (bmrm.Fp-bmrm.Fd)/bmrm.Fp, R, bmrm.nCP, bmrm.nzA);

	} /* end of main loop */

    cleanup:

	LIBBMRM_FREE(H);
	LIBBMRM_FREE(b);
	LIBBMRM_FREE(beta);
	LIBBMRM_FREE(A);
	LIBBMRM_FREE(diag_H);
        LIBBMRM_FREE(I);

	return(bmrm);
    }
}
