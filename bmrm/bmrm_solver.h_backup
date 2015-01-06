#ifndef _BMRM_SOLVER
#define _BMRM_SOLVER


#include <vector>

/* /\* #define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION *\/ */

#include "Python.h"

#define PY_ARRAY_UNIQUE_SYMBOL Py_Array_API_bmrm_solver
#ifndef SWIG_FILE_WITH_INIT
#define NO_IMPORT_ARRAY
#endif

#include "numpy/arrayobject.h"


typedef struct {
    int nIter;         /* number of iterations  */
    int nCP;           /* number of cutting planes */
    int nzA;           /* number of active cutting planes */
    double Fp;           /* primal objective value  */
    double Fd;           /* reduced (dual) objective value */
    int qp_exitflag;     /* exitflag from the last call of the inner QP solver  */
    int exitflag;        /* 1 .. ocas.Q_P - ocas.Q_D <= TolRel*ABS(ocas.Q_P)
                            2 .. ocas.Q_P - ocas.Q_D <= TolAbs
                            -1 .. ocas.nCutPlanes >= BufSize
                            -2 .. not enough memory for the solver */

    /** Track of Fp values in individual iterations */
    std::vector< double > hist_Fp;

    /** Track of Fd values in individual iterations */
    std::vector< double > hist_Fd;

    /** Track of w_dist values in individual iterations */
    std::vector< double > hist_wdist;

} bmrm_return_value_T;


class BMRM_Solver {

    static const int BMRM_USUAL = 1;
    static const int BMRM_PROXIMAL = 2;

    double _TolRel;
    double _TolAbs;
    double _lambda;
    int _BufSize;
    bool cleanICP;
    int cleanAfter;
    double K;
    int T_max;
    int cp_models;
    bool verbose;
    bmrm_return_value_T report;

    bmrm_return_value_T svm_bmrm_solver(
                                        double*       W,
                                        double        TolRel,
                                        double        TolAbs,
                                        double        _lambda,
                                        int         _BufSize,
                                        bool             cleanICP,
                                        int         cleanAfter,
                                        double        K,
                                        int         Tmax,
                                        bool             verbose);

    bmrm_return_value_T svm_ppbm_solver(
                                        double*      W,
                                        double       TolRel,
                                        double       TolAbs,
                                        double       _lambda,
                                        int        _BufSize,
                                        bool            cleanICP,
                                        int        cleanAfter,
                                        double       K,
                                        int        Tmax,
                                        bool            verbose);

    double risk(double *w, double *subgrad);
	
	PyObject* w_arr;
	PyObject* s_arr;

 public:

    BMRM_Solver();
    PyObject* learn(int algorithm = BMRM_Solver::BMRM_USUAL);

    virtual double eval_risk(PyObject *, PyObject *) = 0;
    virtual const int get_dim() = 0;

    virtual ~BMRM_Solver();

    void set_TolRel(double);
    void set_TolAbs(double);
    void set_BufSize(int);
    void set_lambda(double);
    void set_cleanICP(bool _cleanICP);
    void set_cleanAfter(int _cleanAfter);
    void set_K(double);
    void set_Tmax(int);
    void set_cp_models(int);
    void set_verbose(bool);

    bmrm_return_value_T get_report() { return report; }
};

#endif // _BMRM_SOLVER
