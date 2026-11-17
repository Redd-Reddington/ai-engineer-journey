########## Episode 2: Span, Linear Combinations, and Basis ##########

"""
Linear Combination
    Adding scaled vectors.

Span
    All reachable points.

Basis
    Minimum vectors needed to describe a space.
"""


## Linear Combination

import numpy as np

"""
Take vectors and scale them.

Example:

2(1, 0) + 3(0, 1)

= (2, 3)
"""

# Python:

v1 = np.array([1, 0])
v2 = np.array([0, 1])

result = 2 * v1 + 3 * v2

print(result)


## Span

"""
Span means:

All locations you can reach using linear combinations.

Given:

1. (1,0)
2. (0,1)

You can reach any point in 2D space.

Example:

1. (4,5)
2. (-2,7)
3. (100,3)

all reachable.
"""


## Basis

"""
A basis is the minimum set of vectors needed to describe a space.

For 2D:

1. (1,0)
2. (0,1)

These are called the standard basis vectors.
"""


"""
Why AI Engineers Care

Imagine:

1. Age
2. Salary
3. Experience

Each feature can act like a direction.

Machine learning models combine these directions to make predictions.

That is basically a huge linear combination."""



"""    Linear combinations, span, basis Using Notebook
import numpy as np
import matplotlib.pyplot as plt

i = np.array([1, 0])
j = np.array([0, 1])
v = 3 * i + 2 * j      # 3 of i plus 2 of j

print("v =", v)

fig, ax = plt.subplots(figsize=(5, 5))
ax.quiver(0, 0, i[0], i[1], angles="xy", scale_units="xy", scale=1, color="green", label="i")
ax.quiver(0, 0, j[0], j[1], angles="xy", scale_units="xy", scale=1, color="red", label="j")
ax.quiver(0, 0, v[0], v[1], angles="xy", scale_units="xy", scale=1, color="blue", label="v = 3i + 2j")
ax.set_xlim(-1, 5)
ax.set_ylim(-1, 5)
ax.set_aspect("equal")
ax.grid(True)
ax.legend()
plt.show()

# Span: can two vectors reach the whole plane?
u = np.array([1, 2])
w = np.array([2, 4])   # w is just 2u, so it adds no new direction
print("rank of u, w:", np.linalg.matrix_rank(np.column_stack([u, w])))   # 1 = only a line
print("rank of i, j:", np.linalg.matrix_rank(np.column_stack([i, j])))   # 2 = the whole plane
"""