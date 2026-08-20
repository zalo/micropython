# test that float hashing distributes non-integral values (i.e. that the
# hash uses the fractional bits, not just truncation to int)

# ports built with the simple truncation hash collide on all of (-1, 1);
# skip there (this test targets MICROPY_FLOAT_HIGH_QUALITY_HASH builds)
if len({hash(i / 1024) for i in range(16)}) == 1:
    print("SKIP")
    raise SystemExit

# integral floats must hash equal to the equal int (dict/set correctness:
# 1 == 1.0 so hash(1) == hash(1.0))
for i in (0, 1, 2, -1, -12, 12345):
    print(i, hash(float(i)) == hash(i))

# equal values hash equal
print(hash(0.5) == hash(2.0 / 4.0))

# fractional values sharing an integer part must (essentially all) hash
# differently - truncation would give 1 distinct hash for each group
frac = {hash(i / 1000.0) for i in range(512)}
print(len(frac) > 384)

coords = {hash((i / 10.0, (i * 13 % 511) / 10.0, (i * 7 % 511) / 10.0)) for i in range(512)}
print(len(coords) > 384)
