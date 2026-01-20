from hail.models.matrix import Matrix
from hail.models.matrix import mmin, mmax


def test_matrix_addition_mixed_dimensions_2d_plus_1d():
    """Test broadcasting 1D matrix across 2D matrix timesteps"""
    matrix_2d = Matrix([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    matrix_1d = Matrix([10.0, 20.0])
    result = matrix_2d + matrix_1d
    expected = [[11.0, 12.0, 13.0], [24.0, 25.0, 26.0]]
    assert list(result) == expected


def test_matrix_addition_mixed_dimensions_1d_plus_2d():
    """Test broadcasting 1D matrix across 2D matrix timesteps (reverse order)"""
    matrix_1d = Matrix([10.0, 20.0])
    matrix_2d = Matrix([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    result = matrix_1d + matrix_2d
    expected = [[11.0, 12.0, 13.0], [24.0, 25.0, 26.0]]
    assert list(result) == expected


def test_matrix_addition_3d():
    """Test 3D matrix addition"""
    matrix_3d_a = Matrix([
        [[1.0, 2.0], [3.0, 4.0]], 
        [[5.0, 6.0], [7.0, 8.0]]
    ])
    matrix_3d_b = Matrix([
        [[0.1, 0.2], [0.3, 0.4]], 
        [[0.5, 0.6], [0.7, 0.8]]
    ])
    result = matrix_3d_a + matrix_3d_b
    expected = [
        [[1.1, 2.2], [3.3, 4.4]], 
        [[5.5, 6.6], [7.7, 8.8]]
    ]
    assert list(result) == expected


def test_matrix_addition_4d():
    """Test 4D matrix addition"""
    matrix_4d_a = Matrix([
        [[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]],
        [[[9.0, 10.0], [11.0, 12.0]], [[13.0, 14.0], [15.0, 16.0]]]
    ])
    matrix_4d_b = Matrix([
        [[[0.1, 0.1], [0.1, 0.1]], [[0.1, 0.1], [0.1, 0.1]]],
        [[[0.2, 0.2], [0.2, 0.2]], [[0.2, 0.2], [0.2, 0.2]]]
    ])
    result = matrix_4d_a + matrix_4d_b
    expected = [
        [[[1.1, 2.1], [3.1, 4.1]], [[5.1, 6.1], [7.1, 8.1]]],
        [[[9.2, 10.2], [11.2, 12.2]], [[13.2, 14.2], [15.2, 16.2]]]
    ]
    assert list(result) == expected


def test_matrix_scalar_addition_3d():
    """Test scalar addition with 3D matrix"""
    matrix_3d = Matrix([
        [[1.0, 2.0], [3.0, 4.0]], 
        [[5.0, 6.0], [7.0, 8.0]]
    ])
    result = matrix_3d + 10
    expected = [
        [[11.0, 12.0], [13.0, 14.0]], 
        [[15.0, 16.0], [17.0, 18.0]]
    ]
    assert list(result) == expected


def test_matrix_dimension_validation_3d():
    """Test that 3D matrices have correct dimension attribute"""
    matrix_3d = Matrix([
        [[1.0, 2.0], [3.0, 4.0]], 
        [[5.0, 6.0], [7.0, 8.0]]
    ])
    assert matrix_3d.dimension == 3


def test_matrix_dimension_validation_4d():
    """Test that 4D matrices have correct dimension attribute"""
    matrix_4d = Matrix([
        [[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]],
        [[[9.0, 10.0], [11.0, 12.0]], [[13.0, 14.0], [15.0, 16.0]]]
    ])
    assert matrix_4d.dimension == 4


def test_matrix_broadcasting_3d_plus_2d():
    """Test broadcasting 2D matrix to 3D matrix"""
    matrix_3d = Matrix([
        [[1.0, 2.0], [3.0, 4.0]], 
        [[5.0, 6.0], [7.0, 8.0]]
    ])
    matrix_2d = Matrix([[100.0, 200.0], [300.0, 400.0]])
    result = matrix_3d + matrix_2d
    expected = [
        [[101.0, 102.0], [103.0, 104.0]], 
        [[305.0, 306.0], [307.0, 408.0]]
    ]
    assert list(result) == expected


def test_matrix_addition_dimension_mismatch_error():
    """Test that dimension mismatches raise appropriate errors"""
    matrix_1d = Matrix([1.0, 2.0, 3.0])  # 3 elements
    matrix_1d_different = Matrix([1.0, 2.0])  # 2 elements
    
    try:
        result = matrix_1d + matrix_1d_different
        assert False, "Should have raised ValueError for length mismatch"
    except ValueError:
        pass  # Expected behavior


def test_matrix_subtraction():
    m1 = Matrix([1, 2, 3])
    m2 = Matrix([4, 5, 6])
    result = m1 - m2
    assert list(result) == [-3, -3, -3]

def test_matrix_subtraction_2D():
    m1 = Matrix([[1, 2, 3], [4, 5, 6]])
    m2 = Matrix([[6, 5, 4], [3, 2, 1]])
    result = m1 - m2
    assert list(result) == [[-5, -3, -1], [1, 3, 5]]

def test_matrix_scalar_subtraction():
    m = Matrix([1, 2, 3])
    result = m - 5
    assert list(result) == [-4, -3, -2]

def test_matrix_scalar_subtraction_2D():
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    result = m - 5
    assert list(result) == [[-4, -3, -2], [-1, 0, 1]]

def test_matrix_reverse_scalar_subtraction():
    m = Matrix([1, 2, 3])
    result = 5 - m
    assert list(result) == [4, 3, 2]

def test_matrix_reverse_scalar_subtraction_2D():
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    result = 5 - m
    assert list(result) == [[4, 3, 2], [1, 0, -1]]

def test_matrix_multiplication():
    m1 = Matrix([1, 2, 3])
    m2 = Matrix([4, 5, 6])
    result = m1 * m2
    assert list(result) == [4, 10, 18]

def test_matrix_multiplication_2D():
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[5, 6], [7, 8]])
    result = m1 * m2
    assert list(result) == [[5, 12], [21, 32]]

def test_matrix_scalar_multiplication():
    m = Matrix([1, 2, 3])
    result = m * 5
    assert list(result) == [5, 10, 15]

def test_matrix_scalar_multiplication_2D():
    m = Matrix([[1, 2], [3, 4]])
    result = m * 5
    assert list(result) == [[5, 10], [15, 20]]

def test_matrix_reverse_scalar_multiplication():
    m = Matrix([1, 2, 3])
    result = 5 * m
    assert list(result) == [5, 10, 15]

def test_matrix_reverse_scalar_multiplication_2D():
    m = Matrix([[1, 2], [3, 4]])
    result = 5 * m
    assert list(result) == [[5, 10], [15, 20]]

def test_matrix_division():
    m1 = Matrix([4, 10, 18])
    m2 = Matrix([4, 5, 6])
    result = m1 / m2
    assert list(result) == [1, 2, 3]

def test_matrix_division_2D():
    m1 = Matrix([[10, 20], [30, 40]])
    m2 = Matrix([[2, 4], [5, 8]])
    result = m1 / m2
    assert list(result) == [[5, 5], [6, 5]]

def test_matrix_scalar_division():
    m = Matrix([5, 10, 15])
    result = m / 5
    assert list(result) == [1, 2, 3]

def test_matrix_scalar_division_2D():
    m = Matrix([[10, 20], [30, 40]])
    result = m / 10
    assert list(result) == [[1, 2], [3, 4]]

def test_matrix_reverse_scalar_division():
    m = Matrix([1, 2, 3])
    result = 9 / m
    assert list(result) == [9, 4.5, 3]

def test_matrix_reverse_scalar_division_2D():
    m = Matrix([[1, 2], [4, 5]])
    result = 20 / m
    assert list(result) == [[20, 10], [5, 4]]

def test_matrix_addition():
    m1 = Matrix([1, 2, 3])
    m2 = Matrix([4, 5, 6])
    result = m1 + m2
    assert list(result) == [5, 7, 9]

def test_matrix_addition_2D():
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[5, 6], [7, 8]])
    result = m1 + m2
    assert list(result) == [[6, 8], [10, 12]]

def test_matrix_add_through_sum():
    m1 = Matrix([1, 2, 3])
    m2 = Matrix([4, 5, 6])
    result = sum([m1, m2])
    assert result == Matrix([5, 7, 9])

def test_matrix_add_through_sum_2D():
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[5, 6], [7, 8]])
    result = sum([m1, m2])
    assert result == Matrix([[6, 8], [10, 12]])

def test_matrix_sum():
    m1 = Matrix([1, 2, 3])
    result = sum(m1)
    assert result == 6




def test_matrix_addition_with_none():
    m1 = Matrix([1, None, 3, None])
    m2 = Matrix([4, 5, None, None])
    result = m1 + m2
    assert list(result) == [5, 5, 3, None]


def test_matrix_scalar_addition():
    m = Matrix([1, 2, 3])
    result = m + 5
    assert list(result) == [6, 7, 8]


def test_matrix_reverse_scalar_addition():
    m = Matrix([1, 2, 3])
    result = 5 + m
    assert list(result) == [6, 7, 8]



def test_matrix_can_be_list():
    m = Matrix([1, 2, 3])
    assert list(m) == [1, 2, 3]
    assert len(list(m)) == 3


def test_matrix_does_elements_power():
    m = Matrix([1, 2, 3])
    result = pow(m, 2)
    assert list(result) == [1, 4, 9]


def test_matrix_floor():
    from math import floor

    m = Matrix([1.1, 2.2, 3.6])
    result = floor(m)
    assert list(result) == [1, 2, 3]


def test_matrix_lt():
    m1 = Matrix([4, 9, 3])
    m2 = Matrix([4, 5, 6])
    result = m1 < m2
    assert list(result) == [False, False, True]


def test_matrix_gt():
    m1 = Matrix([1, 9, 3])
    m2 = Matrix([4, 5, 6])
    result = m1 > m2
    assert list(result) == [False, True, False]


def test_matrix_le():
    m1 = Matrix([1, 5, 9])
    m2 = Matrix([4, 5, 6])
    result = m1 <= m2
    assert list(result) == [True, True, False]


def test_matrix_ge():
    m1 = Matrix([1, 5, 9])
    m2 = Matrix([4, 5, 6])
    result = m1 >= m2
    assert list(result) == [False, True, True]


def test_matrix_eq():
    m1 = Matrix([1, 2, 6])
    m2 = Matrix([4, 5, 6])
    result = m1 == m2
    assert list(result) == [False, False, True]


def test_matrix_ne():
    m1 = Matrix([1, 2, 6])
    m2 = Matrix([4, 5, 6])
    result = m1 != m2
    assert list(result) == [True, True, False]


def test_matrix_union():
    # prefer left side, if it is not None
    m1 = Matrix([None, 2, None])
    m2 = Matrix([1, 1, 1])
    result = m1 | m2
    assert list(result) == [1, 2, 1]


def test_matrix_max():
    m1 = Matrix([6, 2, 3])
    m2 = Matrix([4, 5, 6])
    result = mmax(m1, m2)
    assert list(result) == [6, 5, 6]


def test_matrix_max_with_negative():
    m1 = Matrix([-9, 2, 3])
    m2 = Matrix([4, -2, 6])
    result = mmax(m1, m2)
    assert list(result) == [4, 2, 6]


def test_matrix_inverse():
    m2 = Matrix([1, 2, 3])
    m1 = Matrix([4, 5, 6])
    assert max(m1, m2) == Matrix([4, 5, 6])


def test_matrix_min():
    m1 = Matrix([1, 2, 3])
    m2 = Matrix([4, 5, 6])
    result = mmin(m1, m2)
    assert list(result) == [1, 2, 3]


def test_matrix_min_negative_or_zero():
    m1 = Matrix([-1, -2, 3])
    m2 = Matrix([0, 0, 0])
    result = mmin(m1, m2)
    assert list(result) == [-1, -2, 0]


def test_addition_with_none():
    m1 = Matrix([1, None, 3])
    m2 = Matrix([4, 5, None])
    result = m1 + m2
    expected = [5, 5, 3]
    assert list(result) == expected, "Addition with None values failed"


def test_subtraction_with_none():
    m1 = Matrix([10, None, 30])
    m2 = Matrix([5, 15, None])
    result = m1 - m2
    expected = [5, -15, 30]
    assert list(result) == expected, "Subtraction with None values failed"


def test_multiplication_with_none():
    m1 = Matrix([2, None, 3])
    m2 = Matrix([4, 5, None])
    result = m1 * m2
    expected = [8, None, None]
    assert list(result) == expected, "Multiplication with None values failed"


def test_division_with_none():
    m1 = Matrix([20, None, 30])
    m2 = Matrix([4, 0, None])
    result = m1 / m2
    expected = [5.0, None, None]
    assert list(result) == expected, "Division with None values failed"


def test_division_by_zero():
    m1 = Matrix([10, 20, None])
    m2 = Matrix([0, 5, 2])
    result = m1 / m2
    expected = [None, 4.0, None]
    assert list(result) == expected, "Division by zero handling failed"


def test_power_with_none():
    m1 = Matrix([2, None, 3])
    m2 = Matrix([3, 4, None])
    result = m1**m2
    expected = [8, None, None]
    assert list(result) == expected, "Exponentiation with None values failed"


def test_floor_with_none():
    m = Matrix([1.9, None, 3.1])
    result = m.__floor__()
    expected = [1, None, 3]
    assert list(result) == expected, "Floor operation with None values failed"


def test_round_with_none():
    m = Matrix([1.2345, None, 3.6789])
    result = round(m, 2)
    expected = [1.23, None, 3.68]
    assert list(result) == expected, "Round operation with None values failed"


def test_comparison_lt_with_none():
    m1 = Matrix([1, None, 3])
    m2 = Matrix([2, 2, None])
    result = m1 < m2
    expected = [True, None, None]
    assert list(result) == expected, "Less than comparison with None values failed"


def test_comparison_eq_with_none():
    m1 = Matrix([1, None, 3])
    m2 = Matrix([1, 2, None])
    result = m1 == m2
    expected = [True, None, None]
    assert list(result) == expected, "Equality comparison with None values failed"


def test_or_operator_with_none():
    m1 = Matrix([None, 2, None])
    m2 = Matrix([1, None, 3])
    result = m1 | m2
    expected = [1, 2, 3]
    assert list(result) == expected, "Logical OR operation with None values failed"


def test_length():
    m = Matrix([1, None, 3, None])
    assert len(m) == 4, "Length calculation failed"


def test_bool_mask():
    m = Matrix([True, False, None, True])
    result = m.mask
    expected = [1, None, None, 1]
    assert list(result) == expected, "Masking failed"


def test_mixed_operations_with_none():
    m1 = Matrix([None, 2, 3])
    m2 = Matrix([1, None, 3])
    m3 = Matrix([1, 2, None])
    result = (m1 + m2) * m3
    expected = [1, 4, None]
    assert list(result) == expected, "Mixed operations with None values failed"


def test_setitem():
    m = Matrix([1, 2, 3])
    m[1] = 4
    assert m.data == [1, 4, 3], "Set item failed at index 1"

    m[0] = 5
    assert m.data == [5, 4, 3], "Set item failed at index 0"

    m[2] = 6
    assert m.data == [5, 4, 6], "Set item failed at index 2"


def test_setitem_out_of_range():
    m = Matrix([1, 2, 3])
    try:
        m[3] = 4
    except IndexError:
        pass
    else:
        assert False, "IndexError not raised for out of range index 3"

    try:
        m[-1] = 4
    except IndexError:
        pass
    else:
        assert False, "IndexError not raised for out of range index -1"
