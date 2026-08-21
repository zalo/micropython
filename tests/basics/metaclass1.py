# test basic custom metaclass creation and identity semantics
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

# subclassing type produces a metaclass
print(issubclass(M, type))
print(isinstance(M, type))

# explicit call of the metaclass creates a class
X = M("X", (), {"a": 1})
print(type(X) is M)
print(isinstance(X, M), isinstance(X, type))
print(X.__name__, X.a)

# instances of the class behave normally
x = X()
print(type(x) is X, isinstance(x, X), x.a)
x.a = 2
print(x.a, X.a)

# class statement with metaclass= keyword
class Y(metaclass=M):
    b = 3
print(type(Y) is M, Y.b)

# the metaclass is inherited from the bases
class Z(Y):
    pass
print(type(Z) is M, issubclass(Z, Y))

# most-derived metaclass rule
class M2(M):
    pass
class W(Z, metaclass=M2):
    pass
print(type(W) is M2)
class V(W):
    pass
print(type(V) is M2)

# classes remain usable as dict keys and compare by identity
d = {X: 1, Y: 2}
print(d[X], d[Y], X == X, X == Y, X != Y)
