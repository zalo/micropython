# test isinstance/issubclass with nested classinfo tuples (CPython accepts
# arbitrarily nested tuples of classes)

class A:
    pass

class B(A):
    pass

# isinstance, one level of nesting
print(isinstance(1.5, (int, (float, str))))
print(isinstance("x", (int, (float, str))))
print(isinstance(1, (int, (float, str))))
print(isinstance([], (int, (float, str))))

# deeper nesting
print(isinstance(1.5, (int, (str, (bytes, (float,))))))
print(isinstance(1.5, (int, (str, (bytes, (bytearray,))))))

# nested tuple containing a user class
print(isinstance(B(), (int, (str, A))))
print(isinstance(A(), (int, (str, B))))

# empty nested tuple is allowed and matches nothing
print(isinstance(1, (str, ())))

# issubclass with nested tuples
print(issubclass(B, (int, (str, A))))
print(issubclass(A, (int, (str, B))))
print(issubclass(B, ((A,),)))
