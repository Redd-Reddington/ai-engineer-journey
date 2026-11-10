"""
Vectorization benchmark: loop vs np.vectorize vs native NumPy
(1,000,000 random floats, computing x ** 2)

Results (one run on my machine):
    loop:      0.1140s
    vectorize: 0.1961s   <- slower than the plain loop
    native:    0.0023s   <- ~49x faster than the loop

Key takeaways:
- np.vectorize is a convenience wrapper, not real vectorization. It still
  calls the Python function once per element, so there is no speedup.
- Native array operations (v ** 2) run in compiled C over contiguous typed
  memory, with no per-element Python overhead.
- Use np.vectorize only when the logic can't be written with array
  operations, np.where, or other built-in NumPy functions.
- With very small arrays the gap shrinks, because NumPy has a fixed
  setup cost per operation.
"""

import time
import numpy as np

# Create 1 million random floats between 0 and 1.
# This is big enough that the differences in speed are easy to see.
x = np.random.rand(1_000_000)


def timeit(f, *args):
    """Run f(*args) once and return how many seconds it took."""
    # perf_counter() is a high-resolution clock meant for measuring short durations.
    start = time.perf_counter()
    f(*args)                          # the work we're timing (result is discarded)
    return time.perf_counter() - start   # end time minus start time = elapsed seconds


# 1) PURE PYTHON LOOP (list comprehension)
# Python walks through the array one element at a time. Each element is a NumPy
# float that gets converted to a Python object, squared, and stored in a list.
# Every step goes through the Python interpreter, so this is slow.
loop = timeit(lambda v: [i ** 2 for i in v], x)

# 2) np.vectorize
# Looks vectorized, but internally it still calls your Python function once per
# element. It only saves you from writing the loop yourself.
# Expect a time close to (or even worse than) the loop above.
vectorize = timeit(np.vectorize(lambda i: i ** 2), x)

# 3) NATIVE NUMPY OPERATION
# v ** 2 runs in compiled C code over the whole array at once, on data stored
# contiguously in memory. No Python-level loop and no per-element object
# creation, so this is the real vectorization.
native = timeit(lambda v: v ** 2, x)

print(f"loop:      {loop:.4f}s")
print(f"vectorize: {vectorize:.4f}s")
print(f"native:    {native:.4f}s")
print(f"native is ~{loop / native:.0f}x faster than the loop")