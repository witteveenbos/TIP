from typing import Iterable, Union


class Matrix(Iterable):

    def __init__(self, data: list):
        self.data = data

    def __iter__(self):
        return iter(self.data)

    def __repr__(self) -> str:
        return f"Matrix({[round(d,2) if d is not None else None for d in self.data]})"

    def __setitem__(self, index, value):
        if index < 0 or index >= len(self.data):
            raise IndexError("list index out of range")

        # Insert the new element at the specified index
        self.data.insert(index, value)

        # Remove the element that was originally at the specified index (now at index+1)
        del self.data[index + 1]

    def __getitem__(self, index):
        return self.data[index]

    def __add__(self, other):
        if isinstance(other, Matrix):
            return Matrix(
                [
                    (
                        a + b
                        if a is not None and b is not None
                        else a if a is not None else b
                    )
                    for a, b in zip(self.data, other.data)
                ]
            )
        else:
            return Matrix([a + other if a is not None else None for a in self.data])

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Matrix):
            return Matrix(
                [
                    (
                        a - b
                        if a is not None and b is not None
                        else a if a is not None else -b if b is not None else None
                    )
                    for a, b in zip(self.data, other.data)
                ]
            )
        else:
            return Matrix([a - other if a is not None else None for a in self.data])

    def __rsub__(self, other):
        if isinstance(other, Matrix):
            return Matrix(
                [
                    b - a if a is not None and b is not None else None
                    for a, b in zip(self.data, other.data)
                ]
            )
        else:
            return Matrix([other - a if a is not None else None for a in self.data])

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return Matrix(
                [
                    a * b if a is not None and b is not None else None
                    for a, b in zip(self.data, other.data)
                ]
            )
        else:
            return Matrix([a * other if a is not None else None for a in self.data])

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Matrix):
            return Matrix(
                [
                    a / b if a is not None and b is not None and b != 0 else None
                    for a, b in zip(self.data, other.data)
                ]
            )
        else:
            return Matrix(
                [a / other if a is not None and other != 0 else None for a in self.data]
            )

    def __rtruediv__(self, other):
        if isinstance(other, Matrix):
            return Matrix(
                [
                    b / a if a is not None and b is not None and a != 0 else None
                    for a, b in zip(self.data, other.data)
                ]
            )
        else:
            return Matrix(
                [other / a if a is not None and a != 0 else None for a in self.data]
            )

    def __pow__(self, other):
        if isinstance(other, Matrix):
            return Matrix(
                [
                    a**b if a is not None and b is not None else None
                    for a, b in zip(self.data, other.data)
                ]
            )
        else:
            return Matrix([a**other if a is not None else None for a in self.data])

    def __floor__(self):
        return Matrix([int(a) if a is not None else None for a in self.data])

    def __lt__(self, other):
        if isinstance(other, Matrix):
            return Matrix(
                [
                    a < b if a is not None and b is not None else None
                    for a, b in zip(self.data, other.data)
                ]
            )
        else:
            return Matrix([a < other if a is not None else None for a in self.data])

    def __gt__(self, other):
        if isinstance(other, Matrix):
            return Matrix(
                [
                    a > b if a is not None and b is not None else None
                    for a, b in zip(self.data, other.data)
                ]
            )
        else:
            return Matrix([a > other if a is not None else None for a in self.data])

    def __le__(self, other):
        if isinstance(other, Matrix):
            return Matrix(
                [
                    a <= b if a is not None and b is not None else None
                    for a, b in zip(self.data, other.data)
                ]
            )
        else:
            return Matrix([a <= other if a is not None else None for a in self.data])

    def __ge__(self, other):
        if isinstance(other, Matrix):
            return Matrix(
                [
                    a >= b if a is not None and b is not None else None
                    for a, b in zip(self.data, other.data)
                ]
            )
        else:
            return Matrix([a >= other if a is not None else None for a in self.data])

    def __eq__(self, other):
        if isinstance(other, Matrix):
            return Matrix(
                [
                    a == b if a is not None and b is not None else None
                    for a, b in zip(self.data, other.data)
                ]
            )
        else:
            return Matrix([a == other if a is not None else None for a in self.data])

    def __ne__(self, other):
        if isinstance(other, Matrix):
            return Matrix(
                [
                    a != b if a is not None and b is not None else None
                    for a, b in zip(self.data, other.data)
                ]
            )
        else:
            return Matrix([a != other if a is not None else None for a in self.data])

    def __abs__(self):
        return Matrix([abs(a) if a is not None else None for a in self.data])

    def __round__(self, n=None):
        return Matrix([round(a, n) if a is not None else None for a in self.data])

    def __or__(self, other):
        # Prefer left side if it is not None
        if isinstance(other, Matrix):
            return Matrix(
                [a if a is not None else b for a, b in zip(self.data, other.data)]
            )
        else:
            return Matrix([a if a is not None else other for a in self.data])

    def __ror__(self, other):
        return self.__or__(other)

    def __len__(self):
        return len(self.data)

    def sum_element_wise(self):
        """Return the sum of all Not-None elements in the matrix"""
        return sum(a for a in self.data if a is not None)

    @property
    def mask(self):
        return Matrix(
            [1 if a is not None and a is not False else None for a in self.data]
        )

    def max_on(self, other):
        return mmax(self, other)

    def min_on(self, other):
        return mmin(self, other)


class AggregatedMatrix(Matrix):
    """A Matrix type that makes explicit that it is the result of an aggregation"""

    def __init__(self, data: list):
        super().__init__(data)

    def __repr__(self) -> str:
        return f"AggregatedMatrix({[round(d,2) if d is not None else None for d in self.data ]})"

    ## TODO: this is slow at runtime, consider doiung this with tests beforehand

    @staticmethod
    def _wrap_method(method_name):
        def method(self, other):
            if type(other) is Matrix:
                raise TypeError("Cannot operate on AggregatedMatrix with Matrix")
            return AggregatedMatrix(
                getattr(super(AggregatedMatrix, self), method_name)(other).data
            )

        return method

    __add__ = _wrap_method("__add__")
    __sub__ = _wrap_method("__sub__")
    __mul__ = _wrap_method("__mul__")
    __truediv__ = _wrap_method("__truediv__")
    __pow__ = _wrap_method("__pow__")
    __lt__ = _wrap_method("__lt__")
    __gt__ = _wrap_method("__gt__")
    __le__ = _wrap_method("__le__")
    __ge__ = _wrap_method("__ge__")
    __eq__ = _wrap_method("__eq__")
    __ne__ = _wrap_method("__ne__")
    __or__ = _wrap_method("__or__")
    min_on = _wrap_method("min_on")
    max_on = _wrap_method("max_on")


def mmin(one: Matrix | float | int, other: Matrix | float | int) -> Matrix:
    return clamp_el_wise(min, one, other)


def mmax(one: Matrix | float | int, other: Matrix | float | int) -> Matrix:
    return clamp_el_wise(max, one, other)


def clamp_el_wise(
    method: Union[min, max], one: Matrix | float | int, other: Matrix | float | int
) -> Matrix:
    if not isinstance(one, Matrix) and not isinstance(other, Matrix):
        raise ValueError(
            "At least one argument should be of type Matrix for matrix minimum"
        )
    elif not isinstance(one, Matrix):
        # make sure left side is Matrix
        one, other = other, one

    if isinstance(other, Matrix):
        return Matrix(
            [
                method(a, b) if a is not None and b is not None else None
                for a, b in zip(one.data, other.data)
            ]
        )
    else:
        return Matrix([min(a, other) if a is not None else None for a in one.data])
