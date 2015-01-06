#ifndef ITESTCLASS_H_
#define ITESTCLASS_H_

// Created by Cython when providing 'public api' keywords
#include "elps_api.h"

#include "TestClass.h"

namespace elps {

class ITestClass : public TestClass {
public:
    PyObject *m_obj;

    ITestClass(PyObject *obj);
    virtual ~ITestClass();
    virtual int override_me();
};

} /* namespace elps */
#endif /* ITESTCLASS_H_ */