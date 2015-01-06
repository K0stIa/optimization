import cpp_bmrm
import numpy as np

class Oracle:
    def __init__(self):
        pass

    def __call__(self, w):
        print w
        g = -2 * np.ones(w.shape)
        Fp = np.dot(g.flat, w.flat)  + 1
        return Fp, g

dim = 2
oracle = Oracle()
bmrm = cpp_bmrm.pyBMRM(dim, oracle)
bmrm.set_lambda(2.0)
weights = bmrm.learn()
report = bmrm.get_report()
print weights
print report.qp_exitflag