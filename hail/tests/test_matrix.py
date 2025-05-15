from hail.models.matrix import Matrix
from hail.models.matrix import mmin, mmax


def test_matrix_subtraction():
    m1 = Matrix([1, 2, 3])
    m2 = Matrix([4, 5, 6])
    result = m1 - m2
    assert list(result) == [-3, -3, -3]


def test_matrix_scalar_subtraction():
    m = Matrix([1, 2, 3])
    result = m - 5
    assert list(result) == [-4, -3, -2]


def test_matrix_reverse_scalar_subtraction():
    m = Matrix([1, 2, 3])
    result = 5 - m
    assert list(result) == [4, 3, 2]


def test_matrix_multiplication():
    m1 = Matrix([1, 2, 3])
    m2 = Matrix([4, 5, 6])
    result = m1 * m2
    assert list(result) == [4, 10, 18]


def test_matrix_scalar_multiplication():
    m = Matrix([1, 2, 3])
    result = m * 5
    assert list(result) == [5, 10, 15]


def test_matrix_reverse_scalar_multiplication():
    m = Matrix([1, 2, 3])
    result = 5 * m
    assert list(result) == [5, 10, 15]


def test_matrix_division():
    m1 = Matrix([4, 10, 18])
    m2 = Matrix([4, 5, 6])
    result = m1 / m2
    assert list(result) == [1, 2, 3]


def test_matrix_scalar_division():
    m = Matrix([5, 10, 15])
    result = m / 5
    assert list(result) == [1, 2, 3]


def test_matrix_reverse_scalar_division():
    m = Matrix([1, 2, 3])
    result = 9 / m
    assert list(result) == [9, 4.5, 3]


def test_matrix_addition():
    m1 = Matrix([1, 2, 3])
    m2 = Matrix([4, 5, 6])
    result = m1 + m2
    assert list(result) == [5, 7, 9]


def test_matrix_add_through_sum():
    m1 = Matrix([1, 2, 3])
    m2 = Matrix([4, 5, 6])
    result = sum([m1, m2])
    assert result == Matrix([5, 7, 9])


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
