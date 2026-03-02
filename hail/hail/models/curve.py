from typing import Iterable, Union


class Curve(Iterable):

    def __init__(self, data: list[list]):
        self.data = data

    def __iter__(self):
        return iter(self.data)

    def __repr__(self) -> str:
        if self.data and len(self.data) > 0:
            first_row = self.data[0]
            if len(first_row) > 3:
                preview = f"[{first_row[0]:.2f}, {first_row[1]:.2f}, ..., {first_row[-1]:.2f}]"
            else:
                preview = f"[{', '.join([f'{x:.2f}' if x is not None else 'None' for x in first_row])}]"
            return f"Curve(2D: {len(self.data)} scenarios x {len(first_row)} timesteps, e.g. {preview})"
        else:
            return "Curve(2D: empty)"

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
        if isinstance(other, Curve):
            # Addition of two 2D Curve objects - element-wise addition
            return Curve(
                [
                    [
                        (
                            a_val + b_val
                            if a_val is not None and b_val is not None
                            else a_val if a_val is not None else b_val
                        )
                        for a_val, b_val in zip(a_row, b_row)
                    ]
                    for a_row, b_row in zip(self.data, other.data)
                ]
            )
        elif isinstance(other, (int, float)):
            # Addition of Curve with a scalar - add to each element
            return Curve(
                [
                    [a_val + other if a_val is not None else None for a_val in row]
                    for row in self.data
                ]
            )
        else:
            raise TypeError(f"Cannot add Curve with {type(other)}")

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Curve):
            # Subtraction of two 2D Curve objects - element-wise subtraction
            return Curve(
                [
                    [
                        (
                            a_val - b_val
                            if a_val is not None and b_val is not None
                            else a_val if a_val is not None else -b_val if b_val is not None else None
                        )
                        for a_val, b_val in zip(a_row, b_row)
                    ]
                    for a_row, b_row in zip(self.data, other.data)
                ]
            )
        elif isinstance(other, (int, float)):
            # Subtraction of scalar from Curve - subtract from each element
            return Curve(
                [
                    [a_val - other if a_val is not None else None for a_val in row]
                    for row in self.data
                ]
            )
        else:
            raise TypeError(f"Cannot subtract {type(other)} from Curve")

    def __rsub__(self, other):
        # For right subtraction (other - self), subtract self from other
        if isinstance(other, Curve):
            return Curve(
                [
                    [
                        b_val - a_val if a_val is not None and b_val is not None else None
                        for a_val, b_val in zip(a_row, b_row)
                    ]
                    for a_row, b_row in zip(self.data, other.data)
                ]
            )
        elif isinstance(other, (int, float)):
            return Curve(
                [
                    [other - a_val if a_val is not None else None for a_val in row]
                    for row in self.data
                ]
            )
        else:
            raise TypeError(f"Cannot subtract Curve from {type(other)}")

    def __mul__(self, other):
        if isinstance(other, Curve):
            # Multiplication of two 2D Curve objects - element-wise multiplication
            return Curve(
                [
                    [
                        a_val * b_val if a_val is not None and b_val is not None else None
                        for a_val, b_val in zip(a_row, b_row)
                    ]
                    for a_row, b_row in zip(self.data, other.data)
                ]
            )
        elif isinstance(other, (int, float)):
            # Multiplication of Curve with scalar - multiply each element
            return Curve(
                [
                    [a_val * other if a_val is not None else None for a_val in row]
                    for row in self.data
                ]
            )
        else:
            raise TypeError(f"Cannot multiply Curve with {type(other)}")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Curve):
            # Division of two 2D Curve objects - element-wise division
            return Curve(
                [
                    [
                        a_val / b_val if a_val is not None and b_val is not None and b_val != 0 else None
                        for a_val, b_val in zip(a_row, b_row)
                    ]
                    for a_row, b_row in zip(self.data, other.data)
                ]
            )
        elif isinstance(other, (int, float)):
            # Division of Curve by scalar - divide each element
            return Curve(
                [
                    [a_val / other if a_val is not None and other != 0 else None for a_val in row]
                    for row in self.data
                ]
            )
        else:
            raise TypeError(f"Cannot divide Curve by {type(other)}")

    def __rtruediv__(self, other):
        if isinstance(other, Curve):
            # Right division of two 2D Curve objects - element-wise division (other / self)
            return Curve(
                [
                    [
                        b_val / a_val if a_val is not None and b_val is not None and a_val != 0 else None
                        for a_val, b_val in zip(a_row, b_row)
                    ]
                    for a_row, b_row in zip(self.data, other.data)
                ]
            )
        elif isinstance(other, (int, float)):
            # Right division of scalar by Curve - divide scalar by each element
            return Curve(
                [
                    [other / a_val if a_val is not None and a_val != 0 else None for a_val in row]
                    for row in self.data
                ]
            )
        else:
            raise TypeError(f"Cannot divide {type(other)} by Curve")

    def __pow__(self, other):
        if isinstance(other, Curve):
            # Power of two 2D Curve objects - element-wise exponentiation
            return Curve(
                [
                    [
                        a_val**b_val if a_val is not None and b_val is not None else None
                        for a_val, b_val in zip(a_row, b_row)
                    ]
                    for a_row, b_row in zip(self.data, other.data)
                ]
            )
        elif isinstance(other, (int, float)):
            # Power of Curve with scalar - raise each element to the power
            return Curve(
                [
                    [a_val**other if a_val is not None else None for a_val in row]
                    for row in self.data
                ]
            )
        else:
            raise TypeError(f"Cannot raise Curve to power of {type(other)}")

    def __floor__(self):
        return Curve(
            [
                [int(a_val) if a_val is not None else None for a_val in row]
                for row in self.data
            ]
        )

    def __lt__(self, other):
        if isinstance(other, Curve):
            return Curve(
                [
                    [
                        a_val < b_val if a_val is not None and b_val is not None else None
                        for a_val, b_val in zip(a_row, b_row)
                    ]
                    for a_row, b_row in zip(self.data, other.data)
                ]
            )
        elif isinstance(other, (int, float)):
            return Curve(
                [
                    [a_val < other if a_val is not None else None for a_val in row]
                    for row in self.data
                ]
            )
        else:
            raise TypeError(f"Cannot compare Curve with {type(other)}")

    def __gt__(self, other):
        if isinstance(other, Curve):
            return Curve(
                [
                    [
                        a_val > b_val if a_val is not None and b_val is not None else None
                        for a_val, b_val in zip(a_row, b_row)
                    ]
                    for a_row, b_row in zip(self.data, other.data)
                ]
            )
        elif isinstance(other, (int, float)):
            return Curve(
                [
                    [a_val > other if a_val is not None else None for a_val in row]
                    for row in self.data
                ]
            )
        else:
            raise TypeError(f"Cannot compare Curve with {type(other)}")

    def __le__(self, other):
        if isinstance(other, Curve):
            return Curve(
                [
                    [
                        a_val <= b_val if a_val is not None and b_val is not None else None
                        for a_val, b_val in zip(a_row, b_row)
                    ]
                    for a_row, b_row in zip(self.data, other.data)
                ]
            )
        elif isinstance(other, (int, float)):
            return Curve(
                [
                    [a_val <= other if a_val is not None else None for a_val in row]
                    for row in self.data
                ]
            )
        else:
            raise TypeError(f"Cannot compare Curve with {type(other)}")

    def __ge__(self, other):
        if isinstance(other, Curve):
            return Curve(
                [
                    [
                        a_val >= b_val if a_val is not None and b_val is not None else None
                        for a_val, b_val in zip(a_row, b_row)
                    ]
                    for a_row, b_row in zip(self.data, other.data)
                ]
            )
        elif isinstance(other, (int, float)):
            return Curve(
                [
                    [a_val >= other if a_val is not None else None for a_val in row]
                    for row in self.data
                ]
            )
        else:
            raise TypeError(f"Cannot compare Curve with {type(other)}")

    def __eq__(self, other):
        if isinstance(other, Curve):
            return Curve(
                [
                    [
                        a_val == b_val if a_val is not None and b_val is not None else None
                        for a_val, b_val in zip(a_row, b_row)
                    ]
                    for a_row, b_row in zip(self.data, other.data)
                ]
            )
        elif isinstance(other, (int, float)):
            return Curve(
                [
                    [a_val == other if a_val is not None else None for a_val in row]
                    for row in self.data
                ]
            )
        else:
            raise TypeError(f"Cannot compare Curve with {type(other)}")

    def __ne__(self, other):
        if isinstance(other, Curve):
            return Curve(
                [
                    [
                        a_val != b_val if a_val is not None and b_val is not None else None
                        for a_val, b_val in zip(a_row, b_row)
                    ]
                    for a_row, b_row in zip(self.data, other.data)
                ]
            )
        elif isinstance(other, (int, float)):
            return Curve(
                [
                    [a_val != other if a_val is not None else None for a_val in row]
                    for row in self.data
                ]
            )
        else:
            raise TypeError(f"Cannot compare Curve with {type(other)}")

    def __abs__(self):
        return Curve(
            [
                [abs(a_val) if a_val is not None else None for a_val in row]
                for row in self.data
            ]
        )

    def __round__(self, n=None):
        return Curve(
            [
                [round(a_val, n) if a_val is not None else None for a_val in row]
                for row in self.data
            ]
        )

    def __or__(self, other):
        # Prefer left side if it is not None
        if isinstance(other, Curve):
            return Curve(
                [
                    [
                        a_val if a_val is not None else b_val
                        for a_val, b_val in zip(a_row, b_row)
                    ]
                    for a_row, b_row in zip(self.data, other.data)
                ]
            )
        elif isinstance(other, (int, float)):
            return Curve(
                [
                    [a_val if a_val is not None else other for a_val in row]
                    for row in self.data
                ]
            )
        else:
            raise TypeError(f"Cannot perform | operation with {type(other)}")

    def __ror__(self, other):
        # For right OR operation (other | self), prefer other when not None
        if isinstance(other, Curve):
            return Curve(
                [
                    [
                        b_val if b_val is not None else a_val
                        for a_val, b_val in zip(a_row, b_row)
                    ]
                    for a_row, b_row in zip(self.data, other.data)
                ]
            )
        elif isinstance(other, (int, float)):
            return Curve(
                [
                    [other if other is not None else a_val for a_val in row]
                    for row in self.data
                ]
            )
        else:
            raise TypeError(f"Cannot perform | operation with {type(other)}")

    def __len__(self):
        return len(self.data)
    
    def __shape__(self):
        if self.data and len(self.data) > 0:
            return (len(self.data), len(self.data[0]))
        else:
            return (0, 0)

    def sum_element_wise(self):
        """Return the sum across scenarios for each timestep, creating a timeseries"""
        if not self.data or not self.data[0]:
            return []
        
        # Get the number of timesteps from the first row
        num_timesteps = len(self.data[0])
        result = []
        
        # Sum across scenarios (rows) for each timestep (column)
        for col_idx in range(num_timesteps):
            column_sum = 0
            for row in self.data:
                if col_idx < len(row) and row[col_idx] is not None:
                    column_sum += row[col_idx]
            result.append(column_sum)
        
        return result

    @property
    def mask(self):
        return Curve(
            [
                [
                    1 if a_val is not None and a_val is not False else None
                    for a_val in row
                ]
                for row in self.data
            ]
        )

    def max_on(self, other):
        return mmax(self, other)

    def min_on(self, other):
        return mmin(self, other)


class AggregatedCurve(Curve):
    """A Curve type that makes explicit that it is the result of an aggregation"""

    def __init__(self, data: list[list]):
        super().__init__(data)

    def __repr__(self) -> str:
        if self.data and len(self.data) > 0:
            first_row = self.data[0]
            if len(first_row) > 3:
                preview = f"[{first_row[0]:.2f}, {first_row[1]:.2f}, ..., {first_row[-1]:.2f}]"
            else:
                preview = f"[{', '.join([f'{x:.2f}' if x is not None else 'None' for x in first_row])}]"
            return f"AggregatedCurve(2D: {len(self.data)} scenarios x {len(first_row)} timesteps, e.g. {preview})"
        else:
            return "AggregatedCurve(2D: empty)"

    ## TODO: this is slow at runtime, consider doiung this with tests beforehand

    @staticmethod
    def _wrap_method(method_name):
        def method(self, other):
            if type(other) is Curve:
                raise TypeError("Cannot operate on AggregatedCurve with Curve")
            return AggregatedCurve(
                getattr(super(AggregatedCurve, self), method_name)(other).data
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


def mmin(one: Curve | float | int, other: Curve | float | int) -> Curve:
    return clamp_el_wise(min, one, other)


def mmax(one: Curve | float | int, other: Curve | float | int) -> Curve:
    return clamp_el_wise(max, one, other)


def clamp_el_wise(
    method: Union[min, max], one: Curve | float | int, other: Curve | float | int
) -> Curve:
    if not isinstance(one, Curve) and not isinstance(other, Curve):
        raise ValueError(
            "At least one argument should be of type Curve for Curve operations"
        )
    elif not isinstance(one, Curve):
        # make sure left side is Curve
        one, other = other, one

    if isinstance(other, Curve):
        # Element-wise operation between two 2D Curve objects
        return Curve(
            [
                [
                    method(a_val, b_val) if a_val is not None and b_val is not None else None
                    for a_val, b_val in zip(a_row, b_row)
                ]
                for a_row, b_row in zip(one.data, other.data)
            ]
        )
    elif isinstance(other, (int, float)):
        # Operation between Curve and scalar
        return Curve(
            [
                [method(a_val, other) if a_val is not None else None for a_val in row]
                for row in one.data
            ]
        )
    else:
        raise TypeError(f"Cannot perform operation between Curve and {type(other)}")
