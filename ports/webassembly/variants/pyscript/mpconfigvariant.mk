JSFLAGS += -s ALLOW_MEMORY_GROWTH

FROZEN_MANIFEST ?= variants/pyscript/manifest.py

# Collect garbage during execution, not only when control returns to
# JavaScript.  The SPLIT_HEAP_AUTO heap otherwise grows with EVERYTHING one
# top-level call allocates (a long-running script ratchets it to hundreds of
# MB that are never returned).  A collection at arbitrary depth needs every
# GC root a suspended C frame holds; wasm keeps those in locals and on the
# operand stack, invisible to a memory scan.  Binaryen fixes that at link time:
#   --flatten          every intermediate value becomes a local (nothing stays
#                      on the operand stack across a call)
#   --coalesce-locals  shrink those locals back down (the spill area below is
#                      one slot per pointer-sized local, so this keeps C frames
#                      -- and recursion depth -- close to an unflattened build)
#   --spill-pointers   store every pointer-sized local live across a call to
#                      the C stack before the call
#   -Os                re-optimize (spill stores are memory writes and stay)
# and main.c's gc_collect() then scans the C stack conservatively
# (MICROPY_GC_SCAN_SPILLED_STACK).  Costs ~+27% wasm and ~5% speed; Asyncify's
# emscripten_scan_registers (the standard variant's approach) costs +164%.
# GC_SPILL_POINTERS=0 restores upstream's deferred top-level-only collection.
GC_SPILL_POINTERS ?= 1
ifeq ($(GC_SPILL_POINTERS),1)
CFLAGS += -DMICROPY_GC_SCAN_SPILLED_STACK=1
JSFLAGS += -s BINARYEN_EXTRA_PASSES=--flatten,--coalesce-locals,--spill-pointers,-Os
JSFLAGS += -s STACK_SIZE=128KB
endif
