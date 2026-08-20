# test sys._getframe() (built on demand from the code-state chain; no trace
# function installed)
import sys

if not hasattr(sys, "_getframe"):
    print("SKIP")
    raise SystemExit

# depth 0 is the caller of _getframe
def g():
    f = sys._getframe(0)
    print(f.f_code.co_name)
    print(f.f_back.f_code.co_name)
    print(f.f_back.f_back.f_code.co_name)
    # depth walking agrees with f_back walking, by identity
    print(sys._getframe(1) is f.f_back)
    print(sys._getframe(2) is f.f_back.f_back)
    # frames are identity-stable per activation
    print(sys._getframe(0) is f)

def caller():
    g()

caller()

# default depth is 0
def default_depth():
    print(sys._getframe().f_code.co_name)

default_depth()

# the module frame is the outermost frame: its f_back is None
print(sys._getframe(0).f_code.co_name)
print(sys._getframe(0).f_back)

# f_lineno is live: it tracks the currently executing line of the frame
def live():
    fr = sys._getframe()
    a = fr.f_lineno
    b = fr.f_lineno
    return b - a

print(live())

# a caller's f_lineno reports the line the caller is currently executing
def caller_line():
    return sys._getframe(1).f_lineno

a = caller_line()
b = caller_line()
print(b - a)

# each activation of a function gets its own frame object
def activation(other):
    me = sys._getframe(0)
    if other is not None:
        return me is other
    return activation(me)

print(activation(None))

# generator frames stay live across resumes
def gen():
    fr = sys._getframe()
    yield fr.f_lineno
    yield fr.f_lineno

gi = gen()
a = next(gi)
b = next(gi)
print(b - a)

# asking beyond the stack depth raises ValueError
try:
    sys._getframe(99)
except ValueError:
    print("ValueError")
