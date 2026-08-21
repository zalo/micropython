# test metaclass __new__/__init__ customization (enum-style member synthesis)
try:
    class _TestMeta(type):
        pass
    class _Test(metaclass=_TestMeta):
        pass
except TypeError:
    print("SKIP")
    raise SystemExit

class TraceMeta(type):
    def __new__(mcs, name, bases, ns):
        print("new", mcs.__name__, name, len(bases))
        return super().__new__(mcs, name, bases, ns)
    def __init__(cls, name, bases, ns):
        print("init", name)
        super().__init__(name, bases, ns)

class A(metaclass=TraceMeta):
    pass
print(type(A) is TraceMeta, A.__name__)

# __new__ can rewrite the namespace before the class is made
class UpperMeta(type):
    def __new__(mcs, name, bases, ns):
        ns2 = {}
        for k, v in ns.items():
            ns2[k.lower() if not k.startswith("_") else k] = v
        return super().__new__(mcs, name, bases, ns2)
class B(metaclass=UpperMeta):
    VALUE = 42
print(B.value, hasattr(B, "VALUE"))

# enum-style: synthesize bound member objects out of the class attributes
class EnumMeta(type):
    def __new__(mcs, name, bases, ns):
        cls = super().__new__(mcs, name, bases, ns)
        members = []
        for k in sorted(ns):
            v = ns[k]
            if not k.startswith("_") and isinstance(v, int):
                obj = object.__new__(cls)
                obj._name_ = k
                obj._value_ = v
                setattr(cls, k, obj)
                members.append(obj)
        cls._members_ = members
        return cls
    def __call__(cls, value):
        for m in cls._members_:
            if m._value_ == value:
                return m
        raise ValueError("not a valid " + cls.__name__)

class Color(metaclass=EnumMeta):
    RED = 1
    GREEN = 2

print(Color.RED._name_, Color.RED._value_)
print(Color.RED is Color.RED, isinstance(Color.RED, Color))
print(Color(2) is Color.GREEN)
try:
    Color(3)
except ValueError:
    print("ValueError")

# extra class keywords are passed through to the metaclass
class KwMeta(type):
    def __new__(mcs, name, bases, ns, **kwargs):
        print("kwargs", sorted(kwargs.items()))
        return super().__new__(mcs, name, bases, ns)
    def __init__(cls, name, bases, ns, **kwargs):
        super().__init__(name, bases, ns)
class C(metaclass=KwMeta, flavor="sweet", size=3):
    pass
print(C.__name__)

# type() 1-arg and 3-arg still work
print(type(1) is int)
D = type("D", (), {"x": 9})
print(type(D) is type, D.x)
