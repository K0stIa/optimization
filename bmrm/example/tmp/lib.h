// -*- c++ -*-
#ifndef FWK_LIB_H
#define FWK_LIB_H 1

struct _object;
typedef _object PyObject;

class IAlg 
{
 public:
  IAlg();
  virtual ~IAlg();
  void doRun();
  virtual void run() =0;
  virtual double oracle(PyObject *, PyObject *) = 0;
  virtual double risk(double *, double *) = 0;
  virtual PyObject * get_parameters();
  virtual PyObject * get_subgradient();
  void doJump(int i);
  virtual void jump(int i);
};

IAlg *create_alg(int algid);

class CyAlgBase : public IAlg
{
public:
  PyObject *m_obj;

  CyAlgBase(PyObject *obj);
  virtual ~CyAlgBase();
  virtual void run();
  virtual void jump(int i);
  virtual double oracle(PyObject *, PyObject *);
  virtual PyObject * get_parameters();
  virtual PyObject * get_subgradient();
};

#endif // !FWK_LIB_H