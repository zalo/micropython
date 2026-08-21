// Test passing integral JS numbers outside the int32 range to Python.
// These must convert as floats: the integer proxy kind carries an i32, so
// they would otherwise arrive silently wrapped (1e15 -> -1530494976).

const mp = await (await import(process.argv[2])).loadMicroPython();

globalThis.small_pos = 42;
globalThis.small_neg = -7;
globalThis.int32_min = -2147483648;
globalThis.int32_max = 2147483647;
globalThis.just_above = 2147483648;
globalThis.just_below = -2147483649;
globalThis.big = 1e15;
globalThis.huge = 1e100;
globalThis.huge_neg = -1e100;

mp.runPython(`
import js

# In-range integral numbers stay ints.
print(type(js.small_pos).__name__, js.small_pos)
print(type(js.small_neg).__name__, js.small_neg)
print(type(js.int32_min).__name__, js.int32_min)
print(type(js.int32_max).__name__, js.int32_max)

# Out-of-int32 integral numbers arrive as floats with the right VALUE.
print(type(js.just_above).__name__, js.just_above == 2147483648.0)
print(type(js.just_below).__name__, js.just_below == -2147483649.0)
print(type(js.big).__name__, js.big == 1e15)
print(type(js.huge).__name__, js.huge == 1e100)
print(type(js.huge_neg).__name__, js.huge_neg == -1e100)
`);

// Test passing them as function-call arguments too.
const mp_print = mp.pyimport("builtins").print;
mp_print(globalThis.big);
mp_print(globalThis.huge);
