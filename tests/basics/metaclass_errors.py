# test error cases of custom metaclasses
try:
    class _TestMeta(type):
        pass
    class _Test(metaclass=_TestMeta):
        pass
except TypeError:
    print("SKIP")
    raise SystemExit

class M(type):
    pass
class N(type):
    pass
class A(metaclass=M):
    pass
class B(metaclass=N):
    pass

# unrelated metaclasses in the bases conflict
try:
    class C(A, B):
        pass
except TypeError:
    print("TypeError")

# an explicit metaclass that is not compatible with a base's metaclass
try:
    class D(A, metaclass=N):
        pass
except TypeError:
    print("TypeError")

# a compatible explicit metaclass is allowed (the derived one wins)
class M2(M):
    pass
class E(A, metaclass=M2):
    pass
print(type(E) is M2)

# a non-class callable metaclass is used as-is
def factory(name, bases, ns):
    return (name, len(bases))
class F(A, metaclass=factory):
    pass
print(F)

# metatypes cannot be mixed with an incompatible native layout
try:
    class G(type, tuple):
        pass
except TypeError:
    print("TypeError")

# isinstance/issubclass reject non-classes properly
try:
    issubclass(A(), A)
except TypeError:
    print("TypeError")
print(isinstance(A(), (B, A)), issubclass(A, (B, A)))
