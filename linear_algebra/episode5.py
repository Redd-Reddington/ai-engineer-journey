########## Three-Dimensional Linear Transformations ##########

##Main Idea
"""
Linear transformations work the same way in
three dimensions as they do in two dimensions.

Instead of transforming a flat plane,
we transform three-dimensional space.

A vector in 3D has three coordinates:

(x, y, z)

Example:

(2, 3, 1)

meaning:

2 units in the x-direction
3 units in the y-direction
1 unit in the z-direction.
"""


##Basis Vectors
"""In three dimensions there are three
standard basis vectors:

i = (1, 0, 0)

j = (0, 1, 0)

k = (0, 0, 1)

Every vector in 3D space can be built
using these basis vectors.


Example:
(2, 3, 1)

=

2(1,0,0)
+
3(0,1,0)
+
1(0,0,1)
"""


##Examples
"""
      ##Scaling

A transformation can stretch
or shrink space.

Example:

(1, 2, 3)

↓

(2, 4, 6)

Everything doubled in size.


      ##Rotation

A transformation can rotate vectors
around an axis.

Example:

A point moves around the z-axis
while keeping its distance
from the origin.


      ##Shearing

A transformation can slant space
without changing dimensions.

Example:

A cube becomes a skewed cube.
"""


##Key Insight
"""
A 3*3 matrix is determined by where
it sends the three basis vectors:

(1,0,0)

(0,1,0)

(0,0,1)

Once we know where these vectors go,
we know how every vector in space
will be transformed.
"""


##Python Example
"""
import numpy as np

A = np.array([
    [2, 0, 0],
    [0, 3, 0],
    [0, 0, 1]
])

v = np.array([1, 2, 3])

print(A @ v)      # Output: [2 6 3]


Meaning:
x-values are doubled
y-values are tripled
z-values remain unchanged
"""


##AI Connection
"""
Machine learning data is often represented
in higher-dimensional spaces.

Example:

Age
Salary
Years of Experience

can form a three-dimensional vector.

The same transformation ideas used in 3D
extend to spaces with hundreds or even
thousands of dimensions.

Neural networks continuously transform
data through these higher-dimensional spaces.
"""



"""   Three-dimensional transformations Using Notebook
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()
df = pd.read_csv("netflix_titles.csv")

M = np.array([[1, 0, 0],
              [0, 0, -1],
              [0, 1, 0]])    # rotate 90 degrees around the x axis

i = np.array([1, 0, 0])
j = np.array([0, 1, 0])
k = np.array([0, 0, 1])

print("M i =", M @ i)
print("M j =", M @ j)       # these three results are the columns of M
print("M k =", M @ k)

v = np.array([1, 2, 3])
print("M v =", M @ v)
"""