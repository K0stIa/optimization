#ifndef _BMRM_SOLVER
#define _BMRM_SOLVER

#include <vector>

struct _object;
typedef _object PyObject;


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
    const int dim;

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

    PyObject *oracle_obj;

 public:

    BMRM_Solver(const int, PyObject *);
    virtual ~BMRM_Solver();

    PyObject* learn(int algorithm);
    
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
