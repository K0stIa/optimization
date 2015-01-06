%module py_libqp
%{
#define SWIG_FILE_WITH_INIT
    /* #define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION */
#include "py_libqp.h"
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

%apply (double* INPLACE_ARRAY2, int DIM1, int DIM2) {(double* Q, int mQ, int nQ)};
%apply (double* INPLACE_ARRAY1, int DIM1) {(double* F, int mF)};
/* %apply (double* INPLACE_ARRAY1, int DIM1) {(double* B, int mB)}; */
/* %apply (int* INPLACE_ARRAY1, int DIM1) {(int* I, int  mI)}; */
/* %apply (int* INPLACE_ARRAY1, int DIM1) {(int* S, int  mS)}; */
%apply (double* INPLACE_ARRAY1, int DIM1) {(double* x0, int  mX0)};

%include "py_libqp.h"
