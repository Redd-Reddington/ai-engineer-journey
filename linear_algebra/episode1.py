###### Vectors | Chapter 1, Essence of linear algebra #####

"""
Vector
    An object with magnitude and direction.

Vector Addition
    Combines movement.

Scalar Multiplication
    Stretches or shrinks a vector.
"""

## Python Connection

import numpy as np

v = np.array([3, 2])

print(v)


## AI Connection

# Features in machine learning are often represented as vectors.
"""
person = [25, 180, 75]

Could mean:
Age = 25
Height = 180 cm
Weight = 75 kg
"""


### Vector Addition
"""
(1, 2) + (3, 1)

= (4, 3)

Graphically:

Move 1 right, 2 up
Then 3 right, 1 up

Result:
4 right, 3 up
"""
# Python:

v1 = np.array([1, 2])
v2 = np.array([3, 1])

print(v1 + v2)



## Scalar Multiplication
"""
Multiply a vector by a number.

2 * (3, 2)

= (6, 4)
"""
# Python:
v = np.array([3, 2])

print(2 * v)



"""       Vectors Using Notebook
import numpy as np
import matplotlib.pyplot as plt

a = np.array([2, 1])
b = np.array([1, 3])
total = a + b          # vector addition
double_a = 2 * a       # scalar multiplication

print("a + b =", total)
print("2a =", double_a)

fig, ax = plt.subplots(figsize=(5, 5))
ax.quiver(0, 0, a[0], a[1], angles="xy", scale_units="xy", scale=1, color="green", label="a")
ax.quiver(0, 0, b[0], b[1], angles="xy", scale_units="xy", scale=1, color="red", label="b")
ax.quiver(0, 0, total[0], total[1], angles="xy", scale_units="xy", scale=1, color="blue", label="a + b")
ax.quiver(0, 0, double_a[0], double_a[1], angles="xy", scale_units="xy", scale=1, color="orange", label="2a")
ax.set_xlim(-1, 6)
ax.set_ylim(-1, 6)
ax.set_aspect("equal")
ax.grid(True)
ax.legend()
plt.show()
"""