# test class-level attribute dispatch through the metaclass:
# properties, methods, __getitem__, __iter__, __contains__, __len__
try:
    class _TestMeta(type):
        pass
    class _Test(metaclass=_TestMeta):
        pass
except TypeError:
    print("SKIP")
    raise SystemExit

# class properties (AxisMeta-style)
class AxisMeta(type):
    @property
    def X(cls):
        return cls((0, 0, 0), (1, 0, 0))
    @property
    def Y(cls):
        return cls((0, 0, 0), (0, 1, 0))

class Axis(metaclass=AxisMeta):
    def __init__(self, origin, direction):
        self.position = origin
        self.direction = direction

print(Axis.X.direction, Axis.Y.direction)
print(Axis.X is not Axis.X)  # a fresh instance per access
print(isinstance(Axis.X, Axis))

# the class's own attributes win over the metaclass namespace
class ShadowMeta(type):
    color = "meta"
    def describe(cls):
        return "meta:" + cls.__name__
class S(metaclass=ShadowMeta):
    color = "cls"
print(S.color, S.describe())
class T(metaclass=ShadowMeta):
    pass
print(T.color)

# storing on the class stores in the class namespace, not the metaclass
T.color = "mine"
print(T.color, ShadowMeta.color)

# subscription, iteration, membership, len via the metaclass
class SeqMeta(type):
    def __getitem__(cls, item):
        return (cls.__name__, item)
    def __iter__(cls):
        return iter([10, 20, 30])
    def __contains__(cls, item):
        return item == 42
    def __len__(cls):
        return 5
class Q(metaclass=SeqMeta):
    pass
print(Q["k"], Q[0])
print(list(Q))
print(42 in Q, 43 in Q, 43 not in Q)
print(len(Q))

# Generic[T]-style class subscription usable in the bases of a class statement
class GenericMeta(type):
    def __getitem__(cls, item):
        return cls
class Generic(metaclass=GenericMeta):
    pass
class Builder(Generic):
    pass
class BuildPart(Builder[int]):
    pass
print(BuildPart.__bases__ == (Builder,), type(BuildPart) is GenericMeta)
print(issubclass(BuildPart, Builder), issubclass(BuildPart, Generic))

# metaclass methods bind the class they are called through
class BoundMeta(type):
    def whoami(cls):
        return cls.__name__
class P1(metaclass=BoundMeta):
    pass
class P2(P1):
    pass
print(P1.whoami(), P2.whoami())
