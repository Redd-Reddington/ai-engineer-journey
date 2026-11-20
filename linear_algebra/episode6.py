#episode 5

########## The Determinant ##########

##Main Idea
"""
The determinant measures how much a transformation changes space.

Think of a square:

□

After transformation it may become:

▱

or

▭

The determinant tells you how the area changed.
"""

##Examples
"""
      ##Determinant = 2

Area doubles.

1 square unit
↓
2 square units



      ##Determinant = 0.5

Area shrinks by half.

1 square unit
↓
0.5 square units



     ##Determinant = 0

Space collapses.

Example:

□
↓
—

Everything flattened into a line.
Information is lost.

This means:

1. No inverse exists.


     ##Negative Determinants

A negative determinant means space flips.

1. Mirror reflection

occurred somewhere in the transformation.
"""


##Python Example
"""
import numpy as np

A = np.array([
[2, 0],
[0, 3]
])

print(np.linalg.det(A))       #Output: 6.0
                              #Meaning area became:
                              #6 times larger
"""



##AI Connection
"""
When data gets transformed many times:

Input
↓
Matrix
↓
Matrix
↓
Matrix

determinants help describe whether information is preserved or crushed.
"""




"""   The determinant Using Notebook
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()
df = pd.read_csv("netflix_titles.csv")

A = np.array([[2, 0],
              [0, 3]])      # stretch x by 2 and y by 3

print("det A =", np.linalg.det(A))                               # 6.0
print("rotation:", np.linalg.det(np.array([[0, -1], [1, 0]])))   # 1.0
print("flip:", np.linalg.det(np.array([[-1, 0], [0, 1]])))       # -1.0
print("squash:", np.linalg.det(np.array([[1, 2], [2, 4]])))      # 0.0

# the unit square before and after A
square = np.array([[0, 1, 1, 0, 0],
                   [0, 0, 1, 1, 0]])
new_square = A @ square

fig, ax = plt.subplots(figsize=(5, 5))
ax.plot(square[0], square[1], label="unit square (area 1)")
ax.plot(new_square[0], new_square[1], label="after A (area 6)")
ax.set_aspect("equal")
ax.grid(True)
ax.legend()
plt.show()
"""