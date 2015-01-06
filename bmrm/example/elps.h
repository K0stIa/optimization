#ifndef __PYX_HAVE__elps
#define __PYX_HAVE__elps


#ifndef __PYX_HAVE_API__elps

#ifndef __PYX_EXTERN_C
  #ifdef __cplusplus
    #define __PYX_EXTERN_C extern "C"
  #else
    #define __PYX_EXTERN_C extern
  #endif
#endif

__PYX_EXTERN_C DL_IMPORT(int) cy_call_func(PyObject *, char *, int *);

#endif /* !__PYX_HAVE_API__elps */

#if PY_MAJOR_VERSION < 3
PyMODINIT_FUNC initelps(void);
#else
PyMODINIT_FUNC PyInit_elps(void);
#endif

#endif /* !__PYX_HAVE__elps */
