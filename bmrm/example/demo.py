from elps import PyTestClass as TC;

a = TC(); 
print a.calculate(1);

class B(TC):
#   pass
    def override_me(self):
        return 5

b = B()
print b.calculate(1)