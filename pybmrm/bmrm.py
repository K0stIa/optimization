'''
Created on Jul 15, 2013

@author: kostia
'''

import numpy as np


class BMRMOptionns(object):
    """
    BMRM Options class
    specify options here
    """

    def __init__(self,
                 dim_w,
                 max_iter = 1000,
                 epsilon = 1e-2,
                 max_cp = 500,
                 verbosity = 1):
                
        self.DIM_W = dim_w
        self.MAX_ITER = max_iter
        self.EPSILON = epsilon
        self.MAX_CP = max_cp                                                   # maxCP : maximum number of cutting plane in approx. problem    (default=  200) ! NRBM working memory = maxCP x dim
        # self.COMPUTE_GAP_QP = compute_gap_qp                                 # verify the solution of approximation
        self.VERBOSITY = verbosity                                             # level of verbosity from 0 to 2
        
        
class BMRMStatistic:

    def __init__(self):
        self.fbest = None                       # best observed value of f
        self.num_iter = None                    # number of iterations
        self.num_oracle_calls = None            # number of function evaluations
        self.time_report = None                 # time for reporting
        self.time_oracle_grad = None            # time for function evaluation / computing gradient
        self.time_NRBM = None                   # time of nrbm
        self.time_Total = None                  # total time


class BMRM:
    
    def __init__(self, oracle, options):
        self._options = options
        self._oracle = oracle
    
    def _evaluate_risk_subgradient(self, w, lmbda):
        return  self._oracle(w)
        
    def _evaluate_regulizer_subgradient(self, w, lmbda):
        return 0.5*lmbda*np.dot(w.flat, w.flat), lmbda*w
    
    def learn(self, lmbda):
        
        dim_w = self._options.DIM_W

        w = np.zeros((dim_w,1))
        subgradients_buffer = np.zeros((dim_w,self._options.MAX_CP))
        Q = np.zeros((self._options.MAX_CP,self._options.MAX_CP))
        bias = np.zeros(self._options.MAX_CP)
        
        inactive                             = np.ones(self._options.MAX_CP) * self._options.MAX_CP                # number of consecutive iterations in which the cutting plane is inactive (alpha=0);
        cp_ite                               = np.zeros(self._options.MAX_CP)                              # the iteration where cp is built
        alpha                                = np.zeros((self._options.MAX_CP,1))                          # lagrangian multipliers
        
        # call oracle at zero point
        cur_risk, cur_risk_subgradient  = self._evaluate_risk_subgradient(w, lmbda)
        
        w_best = w
        Fp_best = cur_risk

        for iteration in xrange(self._options.MAX_ITER):
            
            # Update working cutting plane set
            cp_old = np.nonzero(inactive<self._options.MAX_CP)[0]
            idx    = np.argsort(-1*inactive*self._options.MAX_ITER*10 + cp_ite, kind="mergesort")                     # sort old CPs by number of inactive then by iteration number
            cp_new = idx[:1]

            cp_old           = np.setdiff1d(cp_old, cp_new)
            inactive[cp_new] = 0
            cp_ite[cp_new]   = iteration

            cur_cp = np.nonzero(inactive<self._options.MAX_CP)[0]
            
            subgradients_buffer[:,cp_new] = cur_risk_subgradient #[:,0]
            
            Q[cp_new,:] = np.dot(subgradients_buffer[:,cp_new].T, subgradients_buffer)
            Q[:,cp_new] = Q[cp_new,:].T
            
            bias[cp_new] = cur_risk - np.dot(cur_risk_subgradient[:,0].flat, w[:,0].flat)
            
            #qp_solving_start_time_point = time.clock()
            
            Q1 = Q[cur_cp, :]; Q1 = Q1[:,cur_cp]
            # Solve QP problem           
            Fd, alpha[cur_cp,:] = self.solve_qp_with_libqp_splex(lmbda, Q1.copy(), bias[cur_cp], self._options.EPSILON)
            
            # get QP program solution
            # update w and counting inactive
            cur_active_cp_ids     = np.nonzero(alpha[cur_cp,0]>0)[0]
            cur_non_active_cp_ids = np.nonzero(alpha[cur_cp,0]==0)[0]

            # get solution from the dual problem
            w = - np.dot(subgradients_buffer[:,cur_cp[cur_active_cp_ids]], alpha[cur_cp[cur_active_cp_ids],:]) / lmbda
            # set up active cutting planes
            inactive[cur_cp[cur_active_cp_ids]]      = 0
            inactive[cur_cp[cur_non_active_cp_ids]] += 1
                       
            # get solution from the dual problem
            # w = - np.dot(subgradients_buffer[:,:iteration+1], alpha) / lmbda            
            # ask oracle
            cur_risk, cur_risk_subgradient  = self._evaluate_risk_subgradient(w, lmbda)
            
            Fp = 0.5 * lmbda * np.dot(w[:,0].flat, w[:,0].flat) + cur_risk
            
            if self._options.VERBOSITY >= 1:
                print "it = %d: Fp = %.3f, Fd = %.3f, (Fp-Fd) = %.3f, (Fp-Fd)/Fp = %.3f, R = %.3f" % (iteration, Fp, Fd, Fp - Fd, (Fp-Fd)/Fp, cur_risk)
            
            if Fp_best > Fp:
                Fp_best = Fp
                w_best = w 
            
            if iteration+1==self._options.MAX_ITER or (Fp-Fd)/np.abs(Fp) < self._options.EPSILON:
                if iteration+1==self._options.MAX_ITER:
                    print "Method did not converge in ", iteration+1, " iterations"
                return w_best, Fp_best
            
            
        assert('if this exception rise then you are screwed!') 


    def solve_qp_with_libqp_splex(self, lmbda, Q, b, EPSILON):

        # case when Q is one dimmension problem should be considered separatly ??
        #works well for cplex

#         if Q.size == 1: return -0.5 * Q[0,0] / lmbda + b[0], 1
        dim = Q.shape[0]
        P = Q/lmbda
        F = -b
        B = 1
        x0 = np.zeros(dim, dtype=np.double)

        max_iter = 1000000
        tol_abs = 0
        tol_rel = 1e-9
        qp_th = -np.inf
        is_equality_constrain = True

        import optimization.libqp.py_libqp as libqp
        
        x_opt, state = libqp.py_libqp_splx_solver(P, F, B, x0, is_equality_constrain,
                                        max_iter, tol_abs, tol_rel, qp_th)
        if state.nIter == max_iter:
            print "WARNING: splex did't find global optima in ", max_iter, " iterations"

#         val = -np.dot(np.dot(P,x0[:,np.newaxis])[:,0], x0)/2 + np.dot(x0, b)
        val = -1*state.QP
        return val, x_opt[:,np.newaxis]
    

# class CuttingPlaneManager:
#     
#     def __init__(self, cp_size, dim_w, max_iter):
#         self._cp_size = cp_size
#         self._dim_w = dim_w
#         self._max_iter = max_iter
#         self._subgradient_buff = np.zeros((self._dim_w, self._cp_size))
#         self._bias = np.zeros(cp_size,dtype=np.double)
#         self._cp_inactive = np.zeros(cp_size, dtype=np.int32)
#         self._cp_last_iter = np.zeros(cp_size, dtype=np.int32)
#         
#     def update_statistic(self, alpha, iteration):
#         idx = np.nonzero(alpha==0)[0]
#         self._cp_inactive[idx] += 1
#         
#     def remove_one_cp(self):        
#         
#     def add_cp(self, w, bias):
#         idx = np.array(range(self._cp_size), dtype=np.int32)
#         idx[self._active_cp] = -1
#         idx = idx[idx>=0]
#         #no free spots
#         if idx.size == 0: return False
#         
#         idx = idx[0]
#         self._subgradient_buff[:,idx] = w[:,0]
#         self._bias[idx] = bias
#         
#         return True        
#     
#     def extract_curent_Q_and_bias(self):
        