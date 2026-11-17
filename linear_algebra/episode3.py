########## Episode 3: Linear Transformations and Matrices ##########

import numpy as np

## Transformation

"""
A transformation changes vectors.

Example:

Plain Text
(2,1)

becomes

(4,2)

Everything doubled.
This is a scaling transformation.
"""



## Matrix Example
"""
[
[2,0]
[0,2]
]

Applied to:

(3,1)

Produces:

(6,2)
"""

A = np.array([
    [2, 0],
    [0, 2]
])

v = np.array([3, 1])

print(A @ v)



## Rotation
"""
Matrices can rotate vectors.

Example:

→

becomes

↑

That's a transformation.
"""



## Shearing
"""Matrices can slant space.

Plain Text
□

becomes

▱

without changing area.
"""


## Big Insight
"""
A matrix describes what happens to the basis vectors.

If you know:

(1,0)

and

(0,1)

after transformation,
you know what happens to every vector.
That's why matrices work.
"""
#Python Example

A = np.array([
    [2, 1],
    [0, 1]
])

v = np.array([3, 2])

print(A @ v)


"""    Linear transformations and matrices Using Notebook
import numpy as np
import matplotlib.pyplot as plt

i = np.array([1, 0])
j = np.array([0, 1])
v = np.array([3, 2])

# The columns of A are where i and j land
A = np.array([[1, -1],
              [1,  1]])

new_i = A @ i
new_j = A @ j
new_v = A @ v

print("A i =", new_i)
print("A j =", new_j)
print("A v =", new_v)
print("same as 3*(A i) + 2*(A j)?", np.allclose(new_v, 3 * new_i + 2 * new_j))

fig, ax = plt.subplots(figsize=(5, 5))
ax.quiver(0, 0, i[0], i[1], angles="xy", scale_units="xy", scale=1, color="green", label="i")
ax.quiver(0, 0, j[0], j[1], angles="xy", scale_units="xy", scale=1, color="red", label="j")
ax.quiver(0, 0, new_i[0], new_i[1], angles="xy", scale_units="xy", scale=1, color="olive", label="A i")
ax.quiver(0, 0, new_j[0], new_j[1], angles="xy", scale_units="xy", scale=1, color="pink", label="A j")
ax.quiver(0, 0, new_v[0], new_v[1], angles="xy", scale_units="xy", scale=1, color="purple", label="A v")
ax.set_xlim(-4, 6)
ax.set_ylim(-4, 6)
ax.set_aspect("equal")
ax.grid(True)
ax.legend()
plt.show()
"""