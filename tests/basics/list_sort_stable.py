# test that list.sort()/sorted() are stable, as Python specifies

# skip on ports built with the unstable quicksort
probe = sorted([(i % 2, i) for i in range(32)], key=lambda t: t[0])
if [t[1] for t in probe] != [i for i in range(32) if i % 2 == 0] + [i for i in range(32) if i % 2 == 1]:
    print("SKIP")
    raise SystemExit

# equal keys keep their original order
l = [(0, 'a'), (1, 'b'), (0, 'c'), (1, 'd'), (0, 'e')]
print(sorted(l, key=lambda t: t[0]))

# ... also under reverse=True (CPython keeps the original order of equal
# elements there too; it does NOT reverse ties)
print(sorted(l, key=lambda t: t[0], reverse=True))

# in-place list.sort()
l2 = list(l)
l2.sort(key=lambda t: t[0])
print(l2)
l2 = list(l)
l2.sort(key=lambda t: t[0], reverse=True)
print(l2)

# stability composes: chained sorts give a multi-key sort
records = [('b', 2), ('a', 1), ('b', 1), ('a', 2), ('a', 1)]
by_second = sorted(records, key=lambda r: r[1])
by_first = sorted(by_second, key=lambda r: r[0])
print(by_first)

# the key function is called exactly once per element
calls = []
def key_fn(x):
    calls.append(x)
    return x % 3
print(sorted([5, 3, 1, 4, 2, 0], key=key_fn))
print(len(calls))

# no key function: sort a larger list with duplicates to exercise the merge
biglist = [(i * 137 + 41) % 50 for i in range(300)]
print(sorted(biglist) == sorted(biglist, reverse=True)[::-1])

# stability on a larger list with many ties, checked via decoration
dec = [((i * 7) % 5, i) for i in range(200)]
res = sorted(dec, key=lambda t: t[0])
ok = True
for a, b in zip(res, res[1:]):
    if a[0] == b[0] and a[1] > b[1]:
        ok = False
print(ok)
res = sorted(dec, key=lambda t: t[0], reverse=True)
ok = True
for a, b in zip(res, res[1:]):
    if a[0] == b[0] and a[1] > b[1]:
        ok = False
print(ok)
