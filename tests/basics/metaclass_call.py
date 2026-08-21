# test metaclass __call__ interception (construction firewall)
try:
    class _TestMeta(type):
        pass
    class _Test(metaclass=_TestMeta):
        pass
except TypeError:
    print("SKIP")
    raise SystemExit

class CallMeta(type):
    def __call__(cls, *args, **kwargs):
        print("call", cls.__name__, args, sorted(kwargs.items()))
        obj = super().__call__(*args, **kwargs)
        obj.tagged = True
        return obj

class A(metaclass=CallMeta):
    def __init__(self, v, k=None):
        self.v = v
        self.k = k

a = A(5, k=7)
print(a.v, a.k, a.tagged, type(a) is A)

# subclass goes through the same firewall
class B(A):
    pass
b = B(1)
print(b.v, b.k, b.tagged, type(b) is B)

# a metaclass __call__ can veto construction entirely
class Veto(type):
    def __call__(cls, *args, **kwargs):
        return "vetoed"
class C(metaclass=Veto):
    def __init__(self):
        print("never runs")
print(C())

# classmethods and staticmethods on the metaclass are reachable via the class
class HelperMeta(type):
    @classmethod
    def which(mcs):
        return mcs.__name__
    @staticmethod
    def double(x):
        return 2 * x
    def tag(cls):
        return "tag:" + cls.__name__
class D(metaclass=HelperMeta):
    pass
print(D.which(), D.double(21), D.tag())
print(HelperMeta.which(), HelperMeta.double(1))

# metaclass inheriting a metaclass, both with __call__
class Outer(type):
    def __call__(cls, *args, **kwargs):
        print("outer", cls.__name__)
        return super().__call__(*args, **kwargs)
class Inner(Outer):
    def __call__(cls, *args, **kwargs):
        print("inner", cls.__name__)
        return super().__call__(*args, **kwargs)
class E(metaclass=Inner):
    def __init__(self):
        self.ok = True
print(E().ok)
