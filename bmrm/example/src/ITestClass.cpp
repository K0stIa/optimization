#include "ITestClass.h"

namespace elps {

ITestClass::ITestClass(PyObject *obj): m_obj(obj) {
    // Provided by "elps_api.h"
    if (import_elps()) {
    } else {
        Py_XINCREF(this->m_obj);
    }
}

ITestClass::~ITestClass() {
    Py_XDECREF(this->m_obj);
}

int ITestClass::override_me()
{
    if (this->m_obj) {
        int error;
        // Call a virtual overload, if it exists
        int result = cy_call_func(this->m_obj, (char*)"override_me", &error);
        if (error)
            // Call parent method
            result = TestClass::override_me();
        return result;
    }
    // Throw error ?
    return 0;
}

} /* namespace elps */