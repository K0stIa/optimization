%module(directors="1") bmrm
%{
#define SWIG_FILE_WITH_INIT
    /* #define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION */
#include "bmrm_solver.h"
    %}

%include "numpy.i"
%init %{
    import_array();
    /* printf("called import_array\n"); */
    %}

%include "typemaps.i"
%include "std_vector.i"
%include "std_string.i"


namespace std {
    %template(vectori) vector<int>;
     %template(vectord) vector<double>;
 };

/*
example of typemap for vector<int> and numpy array
http://stackoverflow.com/questions/9270052/is-there-any-way-to-use-pythonappend-with-swigs-new-builtin-feature
 */

/* %apply (double* INPLACE_ARRAY1, int DIM1, double* INPLACE_ARRAY1, int DIM1) {(double* w, int  nW, double *subgrad, int nS)}; */
/* %feature("director") BMRM_Solver::get_dim; */
/* %feature("director") BMRM_Solver::eval_risk; */

%feature("director") BMRM_Solver;

%include "bmrm_solver.h"
