########## Inverse Matrices, Column Space, and Null Space ##########
#This is one of the most important episodes for machine learning.


##Inverse Matrix
"""
An inverse matrix undoes a transformation.

Example:

1. A
2. ↓
3. A⁻¹
4. ↓
5. Original

Similar to:
1. *5
2  ↓
3. ÷5
"""


"""
Example

import numpy as np

A = np.array([
    [2, 0],
    [0, 2]
])

A_inv = np.linalg.inv(A)

print(A_inv)             #Output:[[0.5 0. ]
                         #       [0.  0.5]]
------------------------------------------------------------------------
"""


##Identity Matrix
"""
Equivalent of the number 1.

1. [
2. [1,0]
3. [0,1]
4. ]

Called:

1. I

Property:

Plain Text
1. AA⁻¹ = I
--------------------------------------------------------------------------
"""


##Column Space
"""
Column space means:

All outputs a matrix can produce.

Example matrix:
1. [
2. [1,0]
3. [0,1]
4. ]

can produce every point in 2D.

Its column space is the entire plane.
---------------------------------------------------------------------------
"""


##Restricted Column Space
"""
Matrix:

1. [
2. [1,0]
3. [2,0]
4. ]

Only gives outputs along one line.

Its column space is limited.
---------------------------------------------------------------------------
"""


##Null Space
"""
Null space means:

Inputs that become zero after transformation.

Example:

1. A(v) = 0

Some vectors disappear entirely.

They are in the null space.
--------------------------------------------------------------------------
"""


##Why Null Space Matters
"""
Suppose:

1. Data
2. ↓
3. Transformation
4. ↓
Some information vanishes

That lost information sits in the null space.

Machine learning often tries to avoid losing useful information.
-----------------------------------------------------------------------------
"""

## Python Example
"""
import numpy as np

A = np.array([
    [1, 1],
    [2, 2]
])

print(np.linalg.det(A))       #Output: 0.0

This matrix has:

1. No inverse

because one direction collapsed into another.
"""





"""    Inverse matrices, column space and null space Using Notebook
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()
df = pd.read_csv("netflix_titles.csv")

A = np.array([[2, 1],
              [1, 1]])
print("det A =", np.linalg.det(A))      # not 0, so A has an inverse

A_inv = np.linalg.inv(A)
print("A_inv =\n", A_inv)
print("A_inv @ A =\n", np.round(A_inv @ A, 10))   # identity: it undoes A

# solve A @ x = v
v = np.array([5, 3])
x = np.linalg.solve(A, v)
print("x =", x, " check A @ x =", A @ x)

# a matrix with no inverse: the columns point the same way
S = np.array([[1, 2],
              [2, 4]])
print("det S =", np.linalg.det(S))                  # 0.0
print("rank S =", np.linalg.matrix_rank(S))         # 1: column space is only a line
# np.linalg.inv(S) would raise LinAlgError: Singular matrix
"""