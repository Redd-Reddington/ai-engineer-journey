"""
20 exercises from the '100 NumPy exercises' set, worked and commented.

Each exercise is one small function that:
  1. does the task,
  2. checks the result with assert (so the file doubles as a mini test suite),
  3. returns the result so you can print and inspect it.

Run it:  python NumPy/numpy_100.py

Topics (matches Week 2):
  Indexing / slicing / masks : 8, 9, 10, 15, 16, 18, 19, 25, 45, 72
  Broadcasting               : 37, 58, 71
  Aggregation and axes       : 13, 22, 67
  Search / sort / products   : 24, 30, 50, 59

The numbers follow the rougier/numpy-100 list. If your copy numbers them
differently, match by the title in each docstring.
"""

import numpy as np

# One seeded random generator, so "random" results are the same every run
# and the asserts are reproducible.
rng = np.random.default_rng(42)


# =====================================================================
# Indexing, slicing and masks
# =====================================================================

def ex08_reverse_vector():
    """8. Reverse a vector (first element becomes last)."""
    z = np.arange(10)             # [0 1 2 ... 9]
    # Slice syntax is [start:stop:step]. Leaving start/stop empty means
    # "the whole thing", and step=-1 walks backwards. This returns a VIEW,
    # not a copy: no data is duplicated.
    result = z[::-1]
    assert list(result) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    return result


def ex09_matrix_0_to_8():
    """9. Create a 3x3 matrix with values ranging from 0 to 8."""
    # arange makes the 9 numbers, reshape arranges them into 3 rows x 3 cols.
    # The total count must match: 3 * 3 == 9, or reshape raises an error.
    result = np.arange(9).reshape(3, 3)
    assert result.shape == (3, 3)
    assert result[0, 0] == 0 and result[2, 2] == 8
    return result


def ex10_nonzero_indices():
    """10. Find the indices of the non-zero elements of [1,2,0,0,4,0]."""
    z = np.array([1, 2, 0, 0, 4, 0])
    # nonzero returns a TUPLE with one array per dimension. For a 1D input
    # that is a 1-item tuple, so we take [0] to get the index array.
    result = np.nonzero(z)[0]
    assert list(result) == [0, 1, 4]
    return result


def ex15_border_of_ones():
    """15. Create a 2D array with 1 on the border and 0 inside."""
    z = np.ones((5, 5))
    # 1:-1 means "from the second element up to (not including) the last",
    # so this selects everything EXCEPT the outer ring. Set that inside to 0.
    z[1:-1, 1:-1] = 0
    assert z.sum() == 16          # a 5x5 border has 5+5+3+3 = 16 cells
    assert z[2, 2] == 0 and z[0, 0] == 1
    return z


def ex16_pad_with_zeros():
    """16. Add a border of 0s around an existing array."""
    z = np.ones((5, 5))
    # pad_width=1 adds one layer on every side. mode="constant" fills the new
    # layer with constant_values (0 here). The array grows from 5x5 to 7x7.
    result = np.pad(z, pad_width=1, mode="constant", constant_values=0)
    assert result.shape == (7, 7)
    assert result.sum() == 25     # the original ones are untouched
    assert result[0].sum() == 0   # new border row is all zeros
    return result


def ex18_below_diagonal():
    """18. Create a 5x5 matrix with values 1,2,3,4 just below the diagonal."""
    # np.diag(values, k) puts `values` on the k-th diagonal.
    # k=0 is the main diagonal, k=-1 is the one just below it.
    # 4 values on the k=-1 diagonal make a 5x5 matrix.
    result = np.diag(1 + np.arange(4), k=-1)
    assert result.shape == (5, 5)
    assert list(np.diag(result, k=-1)) == [1, 2, 3, 4]
    return result


def ex19_checkerboard():
    """19. Create an 8x8 matrix and fill it with a checkerboard pattern."""
    z = np.zeros((8, 8), dtype=int)
    # Step slicing picks every other row/column.
    #   z[1::2, ::2] : odd rows (1,3,5,7),  even columns (0,2,4,6)
    #   z[::2, 1::2] : even rows (0,2,4,6), odd columns  (1,3,5,7)
    # Together those two groups are the "black squares".
    z[1::2, ::2] = 1
    z[::2, 1::2] = 1
    assert z.sum() == 32          # exactly half the squares
    assert z[0, 0] == 0 and z[0, 1] == 1 and z[1, 0] == 1
    # no two horizontal neighbours are equal
    assert (z[:, :-1] != z[:, 1:]).all()
    return z


def ex25_negate_between_3_and_8():
    """25. Given a 1D array, negate all elements between 3 and 8, in place."""
    z = np.arange(11)             # [0 1 2 ... 10]
    original_id = id(z)
    # (3 < z) & (z < 8) builds a BOOLEAN MASK: True where the value is
    # strictly between 3 and 8. Use & (not "and") and keep the parentheses,
    # because & binds tighter than comparison operators in Python.
    # Indexing with the mask picks those elements, and *= -1 changes them
    # in place. No loop needed: this is the vectorized way.
    z[(3 < z) & (z < 8)] *= -1
    assert id(z) == original_id   # same array object: truly in place
    assert list(z) == [0, 1, 2, 3, -4, -5, -6, -7, 8, 9, 10]
    return z


def ex45_zero_the_max():
    """45. Create a random vector of size 10 and replace the maximum with 0."""
    z = rng.random(10)
    biggest = z.max()
    # argmax returns the INDEX of the largest value (the first one if tied),
    # so we can assign straight to that position.
    z[z.argmax()] = 0
    assert z.max() < biggest      # the old maximum is gone
    assert (z == biggest).sum() == 0
    return z


def ex72_swap_rows():
    """72. Swap two rows of a matrix."""
    a = np.arange(25).reshape(5, 5)
    # a[[0, 1]] is FANCY indexing: a list of row numbers returns those rows
    # as a copy. The right-hand side a[[1, 0]] is evaluated first (a copy of
    # rows 1 then 0), and then assigned into rows 0 and 1. Result: swapped.
    a[[0, 1]] = a[[1, 0]]
    assert list(a[0]) == [5, 6, 7, 8, 9]
    assert list(a[1]) == [0, 1, 2, 3, 4]
    return a


# =====================================================================
# Broadcasting
# =====================================================================

def ex37_row_values_0_to_4():
    """37. Create a 5x5 matrix with row values ranging from 0 to 4."""
    z = np.zeros((5, 5))
    # Broadcasting: shapes are compared from the RIGHT. (5, 5) vs (5,):
    # the trailing 5s match, and the missing leading dimension is treated as
    # "repeat". So arange(5) is added to every row.
    z += np.arange(5)
    assert all(list(row) == [0, 1, 2, 3, 4] for row in z)
    return z


def ex58_subtract_row_mean():
    """58. Subtract the mean of each row of a matrix."""
    x = rng.random((5, 10))
    # mean(axis=1) averages ACROSS columns, giving one mean per row: shape (5,).
    # keepdims=True keeps it as (5, 1) instead of (5,). That matters:
    #   (5, 10) - (5, 1)  -> broadcasts: each row minus its own mean  (correct)
    #   (5, 10) - (5,)    -> aligns (5,) with the 10 columns -> shape error
    y = x - x.mean(axis=1, keepdims=True)
    assert y.shape == (5, 10)
    assert np.allclose(y.mean(axis=1), 0)   # every row now averages to 0
    return y


def ex71_broadcast_3d_by_2d():
    """71. Multiply an array of shape (5,5,3) by an array of shape (5,5)."""
    a = np.ones((5, 5, 3))
    b = 2 * np.ones((5, 5))
    # The naive a * b FAILS: broadcasting aligns from the right, so b's
    # trailing 5 is compared with a's trailing 3, and 5 != 3.
    try:
        _ = a * b                 # deliberately fails: (5,5,3) vs (5,5)
        raise AssertionError("expected a broadcasting error")
    except ValueError:
        pass                      # this error is what we expect
    # Fix: add a new axis to b so its shape is (5, 5, 1). A size-1 dimension
    # stretches to match the 3. b[:, :, None] and b[..., np.newaxis] are the same.
    result = a * b[:, :, None]
    assert result.shape == (5, 5, 3)
    assert (result == 2).all()
    return result


# =====================================================================
# Aggregation and axes
# =====================================================================

def ex13_min_and_max():
    """13. Create a 10x10 array with random values and find min and max."""
    z = rng.random((10, 10))
    # With no axis argument, min and max look at ALL 100 values.
    zmin, zmax = z.min(), z.max()
    assert 0 <= zmin <= zmax < 1  # random() is in [0, 1)
    assert zmin == z.flatten().min()
    return zmin, zmax


def ex22_normalize():
    """22. Normalize a 5x5 random matrix (rescale to the range 0..1)."""
    z = rng.random((5, 5))
    # Min-max scaling: subtract the minimum (smallest becomes 0), then divide
    # by the range (largest becomes 1). All vectorized, no loops.
    z = (z - z.min()) / (z.max() - z.min())
    assert np.isclose(z.min(), 0) and np.isclose(z.max(), 1)
    return z


def ex67_sum_last_two_axes():
    """67. Sum a 4D array over the last two axes at once."""
    a = rng.random((3, 4, 3, 4))
    # axis accepts a TUPLE: sum over axes -2 and -1 together.
    # The two summed axes disappear, leaving shape (3, 4).
    result = a.sum(axis=(-2, -1))
    assert result.shape == (3, 4)
    # Cross-check with another route: flatten the last two axes into one
    # (reshape with -1 = "work it out"), then sum that single axis.
    assert np.allclose(result, a.reshape(a.shape[:-2] + (-1,)).sum(axis=-1))
    return result


# =====================================================================
# Searching, sorting and products
# =====================================================================

def ex24_matrix_product():
    """24. Multiply a 5x3 matrix by a 3x2 matrix (real matrix product)."""
    # @ is matrix multiplication (same as np.dot for 2D). The inner
    # dimensions must match: (5, 3) @ (3, 2) -> (5, 2).
    # Plain * would be ELEMENT-WISE and would fail on these shapes.
    result = np.ones((5, 3)) @ np.ones((3, 2))
    assert result.shape == (5, 2)
    assert (result == 3).all()    # each cell sums 3 products of 1*1
    return result


def ex30_common_values():
    """30. Find the common values between two arrays."""
    a = np.array([1, 3, 5, 7, 9, 11])
    b = np.array([2, 3, 4, 7, 8, 11])
    # intersect1d returns the sorted, unique values present in both.
    result = np.intersect1d(a, b)
    assert list(result) == [3, 7, 11]
    return result


def ex50_closest_value():
    """50. Find the value closest to a given scalar in a vector."""
    z = np.array([1, 4, 9, 16, 25])
    v = 10
    # Distance from v to every element at once, then argmin gives the index
    # of the smallest distance. abs() matters: a value below v must count as
    # far as one the same distance above.
    index = np.abs(z - v).argmin()
    result = z[index]
    assert result == 9            # |9-10| = 1 beats |16-10| = 6
    return result


def ex59_sort_by_column():
    """59. Sort an array by the n-th column."""
    z = rng.integers(0, 10, size=(5, 4))
    n = 1
    # argsort returns the ORDER in which to take the elements to get them
    # sorted (not the sorted values). Applying that order to the rows with
    # z[order] reorders whole rows, so each row stays intact.
    order = z[:, n].argsort()
    result = z[order]
    assert (np.diff(result[:, n]) >= 0).all()   # column n is now ascending
    # rows were only reordered, never changed: same multiset of rows
    assert sorted(map(tuple, result)) == sorted(map(tuple, z))
    return result


# =====================================================================
# Runner
# =====================================================================

EXERCISES = [
    ex08_reverse_vector, ex09_matrix_0_to_8, ex10_nonzero_indices,
    ex13_min_and_max, ex15_border_of_ones, ex16_pad_with_zeros,
    ex18_below_diagonal, ex19_checkerboard, ex22_normalize,
    ex24_matrix_product, ex25_negate_between_3_and_8, ex30_common_values,
    ex37_row_values_0_to_4, ex45_zero_the_max, ex50_closest_value,
    ex58_subtract_row_mean, ex59_sort_by_column, ex67_sum_last_two_axes,
    ex71_broadcast_3d_by_2d, ex72_swap_rows,
]


def main():
    for exercise in EXERCISES:
        result = exercise()       # an AssertionError here means the solution is wrong
        title = exercise.__doc__.splitlines()[0]
        print(f"\n{title}")
        print(result)
    print(f"\nAll {len(EXERCISES)} exercises passed their checks.")


if __name__ == "__main__":
    main()
