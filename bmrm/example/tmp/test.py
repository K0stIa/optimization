import numpy as np
import sys
#sys.path.append('__build__')
import cyfwk

class PyAlg(cyfwk.AlgBase):
    def run(self):
        print '[py--]  PyAlg.run()'
    def oracle(self, w):
    	w[0] = 10

print "===> testing a py-alg"
s = PyAlg()
print "---> calling doRun()"
print s.doRun()
print "---> calling doJump()"
print s.doJump(3)

a = np.ones(4)
s = PyAlg()
print a
s.oracle(a)
print a