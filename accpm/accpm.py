import numpy as np
import time

#import ipdb; ipdb.set_trace()

def pos(x):
    if(np.any(~np.isreal(x))): raise Exception('Argument must be real.')
    x[x < 0] = 0
    return x

def acent(A, b, x_0):

    MAXITERS = 1000
    ALPHA = 0.1
    BETA = 0.5
    TOL = 1e-6

    m = b.size

    # starting point
    e = 0.01

    y = pos(np.dot(A,x_0) - b + e)
    y[y == 0] = 1
    x = x_0
    #dual variables
    w = np.zeros((m,1))

    niter = MAXITERS
    AT = A.transpose()

    #lacond = -np.inf

    for iters in range(MAXITERS):
        g = -1.0 / y
        H = np.diag((1./y**2).transpose()[0])
        rd = g + w
        rp = np.dot(A,x) + y - b
        res = np.r_[np.dot(A.transpose(),w), rd, rp]

        if(np.sqrt(np.dot(res.transpose(),res)[0,0]) < np.sqrt(TOL)):
            niter = iters + 1
            break

        AHA = np.dot(np.dot(AT,H), A)
        #lacond = max(lacond, np.linalg.cond(AHA))
        dx = np.linalg.solve(AHA, np.dot(AT, g - np.dot(H,rp)))
        dy = - np.dot(A,dx)- rp
        dw = - np.dot(H,dy) - rd

        t = 1
        while((y+t*dy).min() <= 0):
            t = BETA*t

        newres = np.r_[np.dot(AT,w+t*dw), \
                       w + t*dw - 1./(y+t*dy), \
                       np.dot(A,x+t*dx) + y + t*dy - b]

        while (np.dot(newres.transpose(),newres)[0,0] > \
               ((1-ALPHA*t)**2)*np.dot(res.transpose(),res)[0,0]):
            t = BETA*t
            newres = np.r_[np.dot(AT,w+t*dw), \
                           w + t*dw - 1./(y+t*dy), \
                           np.dot(A,x+t*dx) + y + t*dy - b]

        x = x + t*dx
        y = y + t*dy
        w = w + t*dw

    t = (np.diag(((b-np.dot(A,x))**(-2)).transpose()[0]))
    H = np.dot(np.dot(AT, t), A)
    return (x,H,niter, niter == MAXITERS)

def  accpm(oracle, C, d, thresh=1.0e-2, Lambda=0.0, MaxIters=50000, is_log = True):

    n = oracle.dimm
    # initial localization polyhedron {x | Cx <= d}

    # C = np.r_[np.eye(n), -np.eye(n)]
    # d = R*np.ones((2*n,1),dtype=np.double)
    # if not(A is None) and not(b is None):
    #     C = np.r_[A,C]
    #     d = np.r_[b,d]

    m = C.shape[0]
    N = 3*n

    #initial point
    x = np.zeros((n,1),dtype=np.double)
    x_best = np.array([],dtype=np.double)

    f_save = np.array([], dtype=np.double)
    f_best = np.array([], dtype=np.double)
    l_save = np.array([], dtype=np.double)
    l_best = np.array([], dtype=np.double)

    nt_steps = []

    for iter in xrange(MaxIters):

        itertic = time.time()
        f, g = oracle(x)
        #print 'oracle call took %f sec.\n' % (time.time() - itertic)
        f = f + Lambda * np.sqrt(np.dot(x.flat,x.flat))/2
        g = g.reshape((g.size,1))
        g = g + Lambda * x

        f_save = np.append(f_save, f)
        if len(f_best)>0:
            f_best = np.append(f_best, min(f_best.min(),f))
        else:
            f_best = np.append(f_best, f)

        if f_best[-1] == f:
            x_best = x.copy

        # deep cut
        C = np.r_[C,[g.reshape(g.size)]]
        d = np.r_[d, [[np.dot(g.flat,x.flat) + f_best[-1] - f]]]

        # find analytical center of polyhedron
        tic = time.time()
        (x, H, nt, max_number_of_iters) = acent(C, d, x)
        #print 'looking for analytical center of polyhedron took %f sec.\n' % (time.time() - tic)
        # compute lower bound

        df = d - np.dot(C, x)
        df[df <= np.finfo(np.float).eps] = np.finfo(np.float).eps

        duals = 1. / df
        mu = duals[:m]
        lmdba = duals[m:]
        lmdba = lmdba / np.sum(duals[m:])
        mu = mu / np.sum(duals[m:])
        lb = np.dot((f_best[:,np.newaxis] - d[m:]).flat,lmdba.flat) - \
             np.dot(d[:m].flat,mu.flat)

        l_save = np.append(l_save, lb)
        if l_best.size > 0:
            l_best = np.append(l_best, max(lb, l_best.max()))
        else:
            l_best = np.append(l_best, lb)

        if is_log:
            print '%4d: nt%4d Fs=%.3f, Fb=%.3f, Ls=%.3f, Lb =%.3f, Fb-Lb=%.3f, 1-Lb/Fb=%.3f' % \
                (iter, nt, f_save[-1], f_best[-1], l_save[-1], l_best[-1], \
                f_best[-1] - l_best[-1], \
                (f_best[-1] - l_best[-1]) / np.abs(f_best[-1]))

        if (f_best[-1] - l_best[-1]) < thresh * np.abs(f_best[-1]) or \
          np.abs(f_best[-1]) < thresh or np.abs(f_best[-1] - l_best[-1])<thresh or \
          max_number_of_iters:
            break

        # ranking and dropping constraints

        if d.size > m + N -1:

            temp1 = np.dot(C,x) - d
            temp1 = np.squeeze(temp1)

            HC = np.linalg.solve(H,C.transpose())
            CHC = np.dot(C,HC)
            temp2 = m*np.sqrt(np.diag(CHC))

            #print np.diag(CHC)

            temp1 = temp1[m:]
            temp2 = temp2[m:]

            r = temp1 / temp2

            idx = np.argsort(r)[::-1]
            idx = idx[:N-1]
            idx = np.sort(idx)

            f_save = f_save[idx]
            f_best = f_best[idx]
            l_save = l_save[idx]
            l_best = l_best[idx]

            idx = m + idx;
            idx = np.append(np.arange(m), idx)

            C = C[idx,:]
            d = d[idx,:]

        #print 'accpm iteration took %f sec.\n' % (time.time() - itertic)
    return x,f_best.min()


#class Oracle:
#    def __init__(self):
#        self.dimm = 20
#        self.m = 200
#        np.random.seed(3)
#        self.AA = np.random.rand(self.m, self.dimm)
#        self.bb = np.random.rand(self.m, 1)
#        #self.A = np.array([[1,0], [-1,0], [0,1], [0,-1]], dtype=np.double)
#        #self.b = np.array([[1],[1],[1],[1]], dtype=np.double)
#        #self.AA = np.array([[1,11], [1,100]], dtype=np.double)
#        #self.bb = np.zeros((self.dimm,1), dtype=np.double)
#
#    def __call__(self, x):
#        f = np.dot(self.AA,x) + self.bb
#        fobj = f.max()
#        idx = f.argmax()
#        g = self.AA[idx,:]
#
#        return fobj, g
#
#
#
#if __name__ == '__main__':
#    import time
#    #import profile
#    tic = time.clock()
#    #profile.run('accpm()')
#    accpm()
#    toc = time.clock()
#    print toc - tic

#oracle = Oracle()

#x, fobj = accpm2(oracle)

#print x

#import scipy.io as sio
#sio.savemat('func.mat', {'A':oracle.AA, 'b':oracle.bb})
