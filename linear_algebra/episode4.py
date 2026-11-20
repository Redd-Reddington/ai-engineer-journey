########## Matrix Multiplication as Composition ##########


##Main Idea

"""
A matrix represents a transformation.

If one matrix performs transformation A and another performs transformation B, then multiplying the matrices combines the transformations.

Vector
↓
Transformation A
↓
Transformation B
↓
Final Result

Instead of applying them separately:

B(A(v))

you can combine them into one matrix:

(BA)v

Example

First matrix:

[
[2, 0]
[0, 2]
]

Scales everything by 2.

Second matrix:

[
[1, 1]
[0, 1]
]

Shears space.

Combined:

BA

creates one transformation that does both.
"""



##Python Example
"""
import numpy as np

A = np.array([
[2, 0],
[0, 2]
])

B = np.array([
[1, 1],
[0, 1]
])

print(B @ A)
-----------------------------------------------------
Step 1: Set up the multiplication
[1 1] * [2 0]
[0 1] * [0 2]

The result will be another 2 * 2 matrix:
[? ?]
[? ?]
----------------------------------------------------
Step 2: Find the top-left value

Take:

Row 1 from B → [1, 1]
Column 1 from A → [2, 0]

Multiply and add:
(1 * 2)+(1 * 0)
2 + 0 = 2

So:
[2 ?]
[? ?]
----------------------------------------------------
Step 3: Find the top-right value

Take:

Row 1 from B → [1, 1]
Column 2 from A → [0, 2]

Multiply and add:
(1 * 0)+(1 * 2)
0 + 2 = 2

So:
[2 2]
[? ?]
----------------------------------------------------
Step 4: Find the bottom-left value

Take:

Row 2 from B → [0, 1]
Column 1 from A → [2, 0]

Multiply and add:

(0 * 2) + (1 * 0)
0 + 0 = 0

So:
[2 2]
[0 ?]
----------------------------------------------------
Step 5: Find the bottom-right value

Take:

Row 2 from B → [0, 1]
Column 2 from A → [0, 2]

Multiply and add:

(0 * 0) + (1 * 2)
0 + 2 = 2

So:
[2 2]
[0 2]
----------------------------------------------------
Final Result:
[[2 2]
[0 2]]
"""

##Important Rule
"""
Matrix multiplication is generally not commutative.

Plain Text
AB ≠ BA

Example:

1. Put on socks
2. Put on shoes

works.

1. Put on shoes
2. Put on socks

doesn't.

Order matters.
"""

##AI Connection
"""
Neural networks repeatedly perform:

Input Vector
↓
Matrix
↓
Matrix
↓
Matrix
↓
Prediction

The entire network is essentially a chain of matrix multiplications.
"""




"""      Matrix multiplication as composition Using Notebook
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()
df = pd.read_csv("netflix_titles.csv")

A = np.array([[0, -1],
              [1,  0]])      # rotate 90 degrees
B = np.array([[1, 1],
              [0, 1]])       # shear

print("A @ B =\n", A @ B)   # apply B first, then A
print("B @ A =\n", B @ A)   # apply A first, then B (different result)

v = np.array([1, 2])
print(A @ (B @ v))          # two steps
print((A @ B) @ v)          # one combined step, same answer
"""