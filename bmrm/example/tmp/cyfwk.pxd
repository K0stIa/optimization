from cpython.ref cimport PyObject

cdef extern from "lib.h":
    cdef cppclass IAlg:
        void doRun()
        void run()
        void doJump()
        void jump()
        double oracle(PyObject *, PyObject *)
        double risk(double *, double *)
        PyObject * get_parameters()
        PyObject * get_subgradient()

    cdef IAlg* create_cy_alg()

    cdef cppclass CyAlgBase:
        #PyObject *obj
        #RunFct fct
        
        CyAlgBase(PyObject *obj)
        void doRun()
        void run()
        void doJump(int i)
        void jump(int i)
        double oracle(PyObject*, PyObject*)
        double risk(double *, double *)
        PyObject * get_parameters()
        PyObject * get_subgradient()
    
cdef public api IAlg* cy_create_alg()