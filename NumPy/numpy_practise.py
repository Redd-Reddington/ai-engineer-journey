import numpy as np
 
""" 
# NumPy array #
array = np.array([1 , 2, 3, 4])

array = array * 2  # Multiply each element by 2

print(array)

print(type(array)) # Print the type of the array
"""



"""
# MULTI-DIMENSIONAL ARRAYS #
array = np.array([[['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']],
                  [['J', 'K', 'L'], ['M', 'N', 'O'], ['P', 'Q', 'R']],
                  [['S', 'T', 'U'], ['V', 'W', 'X'], ['Y', 'Z', '_']]])

print(array.ndim) # Print the number of dimensions of the array 
print(array.shape) # Print the shape of the array
print(array[1, 1, 1]) # Print the element at index [1, 1, 1] of the array

word = array[0, 0, 0] + array[2, 0, 0] + array[2, 0, 0] # Concatenate elements at specified indices
print(word)
"""



"""
 # INDEXING AND SLICING #
array = np.array([[1, 2, 3, 4],
                 [5, 6, 7, 8],
                 [9, 10, 11, 12],
                 [13, 14, 15, 16]]) # Create a 2D array

# array[start:end:step]

print(array[1]) # Print the second row of the array
print(array[-2]) # Print the second last row of the array
print(array[0:3]) # Print the first three rows of the array
print(array[0:4:2]) # Print every second row of the array 
print(array[::2]) # Print every second row of the array
print(array[::-1])  # Print the array in reverse order

print(array[:, 0]) # Print the first column of the array  
print(array[:, 2]) # Print the third column of the array
print(array[:, -2]) # Print the second last column of the array
print(array[:, 0: 3]) # Print the first three columns of the array
print(array[:, 1: 4]) # Print the last three columns of the array
print(array[:, ::2]) # Print every second column of the array
print(array[:, 1::2]) # Print every second column of the array starting from the second column
print(array[:, ::-2]) # Print every second column of the array in reverse order

print(array[0:2, 0:2]) # Print the first two rows and first two columns of the array
print(array[0:2, 2:4]) # Print the first two rows and the last two columns of the array
print(array[0:2, 2:]) # Print the first two rows and every column from the third column to the end of the array 
print(array[2:, 2:4]) # Print every row from the third row to the end of the array and the last two columns of the array
print(array[2:, 2:]) # Print every row from the third row to the end of the array and every column from the third column to the end of the array
"""



"""
# BROADCASTING = allows NumPy to perform operations with different shapes by virtually expanding dimensions
#               so they match the larger array's shape.

#The dimensions have the same size.
#OR
#One of the dimensions has size 1.


array1 = np.array([[1, 2, 3, 4]])
array2 = np.array([[1], [2], [3], [4]])

print(array1.shape) # array1 has shape (1, 4) because it has 1 row and 4 columns
print(array2.shape) # array2 has shape (4, 1) because it has 4 rows and 1 column

print(array1 + array2) # Add the two arrays using broadcasting


array3 = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]])
array4 = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])

print(array3.shape) # array3 has shape (1, 10) because it has 1 row and 10 columns
print(array4.shape) # array4 has shape (10, 1) because it has 10 rows and 1 column

print(array3 + array4) # Add the two arrays using broadcasting
"""



"""
# VECTORIZE = A NumPy function that converts a scalar python functio into a
#             vectorized function that operates on arrays element by element.
"""

def square(x):
    return x ** 2

arr = np.array([1, 2, 3, 4, 5])

vectorized_square = np.vectorize(square) # Convert the square function into a vectorized function
result = vectorized_square(arr) # Apply the vectorized function to the array

print(result) # Print the result of squaring each element in the array



def is_even(x):
    return x % 2 == 0

arr = np.array([1, 2, 3, 4, 5])

vectorized_even = np.vectorize(is_even, otypes=[bool]) # Convert the is_even function into a vectorized function with output type bool
result = vectorized_even(arr)

print(result)



def power(base, exponent):
    return base ** exponent

bases = np.array([2, 3, 4])
exponents = np.array([3, 2, 2])

vectorized_power = np.vectorize(power)
result = vectorized_power(bases, exponents)

print(result)