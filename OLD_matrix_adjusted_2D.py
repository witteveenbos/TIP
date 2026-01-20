# from typing import Iterable, Union


# class Matrix(Iterable):

#     def __init__(self, data: list):
#         self.data = data
#         self.dimension = self._calculate_dimensionality()

#     def _calculate_dimensionality(self):
#         """Calculate the dimensionality of the matrix data recursively"""
#         def get_depth(data):
#             if not data or not isinstance(data, list):
#                 return 0
#             if not isinstance(data[0], list):
#                 return 1
#             return 1 + get_depth(data[0])
        
#         def validate_structure(data, expected_depth, current_depth=1):
#             if current_depth == expected_depth:
#                 # At the deepest level, all should be scalars
#                 return all(not isinstance(item, list) for item in data)
#             elif current_depth < expected_depth:
#                 # At intermediate levels, all should be lists of same length
#                 if not all(isinstance(item, list) for item in data):
#                     return False
#                 expected_length = len(data[0]) if data else 0
#                 return (all(len(item) == expected_length for item in data) and
#                         all(validate_structure(item, expected_depth, current_depth + 1) for item in data))
#             else:
#                 return False
        
#         dimension = get_depth(self.data)
#         if not validate_structure(self.data, dimension):
#             raise ValueError(f"Irregular {dimension}D matrix structure - all dimensions must be consistent")
#         return dimension

#     def __iter__(self):
#         return iter(self.data)

#     def __repr__(self) -> str:
#         def get_shape(data, depth=0):
#             if not isinstance(data, list) or not data:
#                 return []
#             shape = [len(data)]
#             if isinstance(data[0], list):
#                 shape.extend(get_shape(data[0], depth + 1))
#             return shape
        
#         def get_sample_value(data, depth=0):
#             if not isinstance(data, list):
#                 return data
#             if depth < 2 and data:  # Show first few elements for shallow depths
#                 return get_sample_value(data[0], depth + 1)
#             return "..."
        
#         shape = get_shape(self.data)
#         sample = get_sample_value(self.data)
        
#         if self.dimension == 1:
#             return f"Matrix({[f'{d:.2f}' if d is not None else None for d in self.data]})"
#         elif self.dimension == 2:
#             if self.data and len(self.data) > 0:
#                 first_row = self.data[0]
#                 if len(first_row) > 3:
#                     preview = f"[{first_row[0]:.2f}, {first_row[1]:.2f}, ..., {first_row[-1]:.2f}]"
#                 else:
#                     preview = f"[{', '.join([f'{x:.2f}' if x is not None else 'None' for x in first_row])}]"
#                 return f"Matrix(2D: {len(self.data)} scenarios x {len(first_row)} timesteps, e.g. {preview})"
#             else:
#                 return "Matrix(2D: empty)"
#         else:
#             shape_str = " x ".join(map(str, shape))
#             return f"Matrix({self.dimension}D: {shape_str}, sample: {sample:.2f if isinstance(sample, (int, float)) else sample})"

#     def __setitem__(self, index, value):
#         if index < 0 or index >= len(self.data):
#             raise IndexError("list index out of range")

#         # Insert the new element at the specified index
#         self.data.insert(index, value)

#         # Remove the element that was originally at the specified index (now at index+1)
#         del self.data[index + 1]

#     def __getitem__(self, index):
#         return self.data[index]

#     def __add__(self, other):
#         if isinstance(other, Matrix):
#             return Matrix(self._recursive_add(self.data, other.data, self.dimension, other.dimension))
#         else:
#             # Matrix + scalar: add scalar to all elements recursively
#             return Matrix(self._recursive_scalar_add(self.data, other))
    
#     def _recursive_add(self, data_a, data_b, dim_a, dim_b):
#         """Recursively add two data structures with broadcasting for different dimensions"""
#         def add_elements(a, b):
#             if a is not None and b is not None:
#                 return a + b
#             return a if a is not None else b
        
#         if dim_a == dim_b:
#             # Same dimensions: element-wise addition
#             if dim_a == 1:
#                 # Base case: both are 1D lists of scalars
#                 return [add_elements(a, b) for a, b in zip(data_a, data_b)]
#             else:
#                 # Recursive case: both are multi-dimensional
#                 if len(data_a) != len(data_b):
#                     raise ValueError(f"Cannot add {dim_a}D matrices with different lengths at outermost dimension")
#                 return [self._recursive_add(sub_a, sub_b, dim_a - 1, dim_b - 1) 
#                        for sub_a, sub_b in zip(data_a, data_b)]
        
#         elif dim_a > dim_b:
#             # data_a has higher dimension: broadcast data_b
#             if len(data_a) != len(data_b):
#                 raise ValueError(f"Cannot broadcast: outermost dimensions don't match ({len(data_a)} vs {len(data_b)})")
#             if dim_b == 1:
#                 # data_b is 1D scalars, broadcast each scalar across data_a structure
#                 return [self._recursive_scalar_add(sub_a, scalar_b) for sub_a, scalar_b in zip(data_a, data_b)]
#             else:
#                 # data_b still multi-dimensional, recurse
#                 return [self._recursive_add(sub_a, scalar_b, dim_a - 1, dim_b) 
#                        for sub_a, scalar_b in zip(data_a, data_b)]
        
#         else:  # dim_a < dim_b
#             # data_b has higher dimension: broadcast data_a  
#             if len(data_a) != len(data_b):
#                 raise ValueError(f"Cannot broadcast: outermost dimensions don't match ({len(data_a)} vs {len(data_b)})")
#             if dim_a == 1:
#                 # data_a is 1D scalars, broadcast each scalar across data_b structure
#                 return [self._recursive_scalar_add(sub_b, scalar_a) for scalar_a, sub_b in zip(data_a, data_b)]
#             else:
#                 # data_a still multi-dimensional, recurse
#                 return [self._recursive_add(scalar_a, sub_b, dim_a, dim_b - 1) 
#                        for scalar_a, sub_b in zip(data_a, data_b)]
    
#     def _recursive_scalar_add(self, data, scalar):
#         """Recursively add a scalar to all elements in arbitrarily nested data"""
#         if isinstance(data, list):
#             return [self._recursive_scalar_add(item, scalar) for item in data]
#         else:
#             return data + scalar if data is not None else None


#     def __radd__(self, other):
#         return self.__add__(other)

#     def __sub__(self, other):
#         if isinstance(other, Matrix):
#             return Matrix(
#                 [
#                     (
#                         a - b
#                         if a is not None and b is not None
#                         else a if a is not None else -b if b is not None else None
#                     )
#                     for a, b in zip(self.data, other.data)
#                 ]
#             )
#         else:
#             return Matrix([a - other if a is not None else None for a in self.data])

#     def __rsub__(self, other):
#         if isinstance(other, Matrix):
#             return Matrix(
#                 [
#                     b - a if a is not None and b is not None else None
#                     for a, b in zip(self.data, other.data)
#                 ]
#             )
#         else:
#             return Matrix([other - a if a is not None else None for a in self.data])

#     def __mul__(self, other):
#         if isinstance(other, Matrix):
#             return Matrix(
#                 [
#                     a * b if a is not None and b is not None else None
#                     for a, b in zip(self.data, other.data)
#                 ]
#             )
#         else:
#             return Matrix([a * other if a is not None else None for a in self.data])

#     def __rmul__(self, other):
#         return self.__mul__(other)

#     def __truediv__(self, other):
#         if isinstance(other, Matrix):
#             return Matrix(
#                 [
#                     a / b if a is not None and b is not None and b != 0 else None
#                     for a, b in zip(self.data, other.data)
#                 ]
#             )
#         else:
#             return Matrix(
#                 [a / other if a is not None and other != 0 else None for a in self.data]
#             )

#     def __rtruediv__(self, other):
#         if isinstance(other, Matrix):
#             return Matrix(
#                 [
#                     b / a if a is not None and b is not None and a != 0 else None
#                     for a, b in zip(self.data, other.data)
#                 ]
#             )
#         else:
#             return Matrix(
#                 [other / a if a is not None and a != 0 else None for a in self.data]
#             )

#     def __pow__(self, other):
#         if isinstance(other, Matrix):
#             return Matrix(
#                 [
#                     a**b if a is not None and b is not None else None
#                     for a, b in zip(self.data, other.data)
#                 ]
#             )
#         else:
#             return Matrix([a**other if a is not None else None for a in self.data])

#     def __floor__(self):
#         return Matrix([int(a) if a is not None else None for a in self.data])

#     def __lt__(self, other):
#         if isinstance(other, Matrix):
#             return Matrix(
#                 [
#                     a < b if a is not None and b is not None else None
#                     for a, b in zip(self.data, other.data)
#                 ]
#             )
#         else:
#             return Matrix([a < other if a is not None else None for a in self.data])

#     def __gt__(self, other):
#         if isinstance(other, Matrix):
#             return Matrix(
#                 [
#                     a > b if a is not None and b is not None else None
#                     for a, b in zip(self.data, other.data)
#                 ]
#             )
#         else:
#             return Matrix([a > other if a is not None else None for a in self.data])

#     def __le__(self, other):
#         if isinstance(other, Matrix):
#             return Matrix(
#                 [
#                     a <= b if a is not None and b is not None else None
#                     for a, b in zip(self.data, other.data)
#                 ]
#             )
#         else:
#             return Matrix([a <= other if a is not None else None for a in self.data])

#     def __ge__(self, other):
#         if isinstance(other, Matrix):
#             return Matrix(
#                 [
#                     a >= b if a is not None and b is not None else None
#                     for a, b in zip(self.data, other.data)
#                 ]
#             )
#         else:
#             return Matrix([a >= other if a is not None else None for a in self.data])

#     def __eq__(self, other):
#         if isinstance(other, Matrix):
#             return Matrix(
#                 [
#                     a == b if a is not None and b is not None else None
#                     for a, b in zip(self.data, other.data)
#                 ]
#             )
#         else:
#             return Matrix([a == other if a is not None else None for a in self.data])

#     def __ne__(self, other):
#         if isinstance(other, Matrix):
#             return Matrix(
#                 [
#                     a != b if a is not None and b is not None else None
#                     for a, b in zip(self.data, other.data)
#                 ]
#             )
#         else:
#             return Matrix([a != other if a is not None else None for a in self.data])

#     def __abs__(self):
#         return Matrix([abs(a) if a is not None else None for a in self.data])

#     def __round__(self, n=None):
#         return Matrix([round(a, n) if a is not None else None for a in self.data])

#     def __or__(self, other):
#         # Prefer left side if it is not None
#         if isinstance(other, Matrix):
#             return Matrix(
#                 [a if a is not None else b for a, b in zip(self.data, other.data)]
#             )
#         else:
#             return Matrix([a if a is not None else other for a in self.data])

#     def __ror__(self, other):
#         return self.__or__(other)

#     def __len__(self):
#         return len(self.data)

#     def sum_element_wise(self):
#         """Return the sum of all Not-None elements in the matrix"""
#         return sum(a for a in self.data if a is not None)

#     @property
#     def mask(self):
#         return Matrix(
#             [1 if a is not None and a is not False else None for a in self.data]
#         )

#     def max_on(self, other):
#         return mmax(self, other)

#     def min_on(self, other):
#         return mmin(self, other)


# class AggregatedMatrix(Matrix):
#     """A Matrix type that makes explicit that it is the result of an aggregation"""

#     def __init__(self, data: list):
#         super().__init__(data)

#     def __repr__(self) -> str:
#         return f"AggregatedMatrix({[round(d,2) if d is not None else None for d in self.data ]})"

#     ## TODO: this is slow at runtime, consider doiung this with tests beforehand

#     @staticmethod
#     def _wrap_method(method_name):
#         def method(self, other):
#             if type(other) is Matrix:
#                 raise TypeError("Cannot operate on AggregatedMatrix with Matrix")
#             return AggregatedMatrix(
#                 getattr(super(AggregatedMatrix, self), method_name)(other).data
#             )

#         return method

#     __add__ = _wrap_method("__add__")
#     __sub__ = _wrap_method("__sub__")
#     __mul__ = _wrap_method("__mul__")
#     __truediv__ = _wrap_method("__truediv__")
#     __pow__ = _wrap_method("__pow__")
#     __lt__ = _wrap_method("__lt__")
#     __gt__ = _wrap_method("__gt__")
#     __le__ = _wrap_method("__le__")
#     __ge__ = _wrap_method("__ge__")
#     __eq__ = _wrap_method("__eq__")
#     __ne__ = _wrap_method("__ne__")
#     __or__ = _wrap_method("__or__")
#     min_on = _wrap_method("min_on")
#     max_on = _wrap_method("max_on")


# def mmin(one: Matrix | float | int, other: Matrix | float | int) -> Matrix:
#     return clamp_el_wise(min, one, other)


# def mmax(one: Matrix | float | int, other: Matrix | float | int) -> Matrix:
#     return clamp_el_wise(max, one, other)


# def clamp_el_wise(
#     method: Union[min, max], one: Matrix | float | int, other: Matrix | float | int
# ) -> Matrix:
#     if not isinstance(one, Matrix) and not isinstance(other, Matrix):
#         raise ValueError(
#             "At least one argument should be of type Matrix for matrix minimum"
#         )
#     elif not isinstance(one, Matrix):
#         # make sure left side is Matrix
#         one, other = other, one

#     if isinstance(other, Matrix):
#         return Matrix(
#             [
#                 method(a, b) if a is not None and b is not None else None
#                 for a, b in zip(one.data, other.data)
#             ]
#         )
#     else:
#         return Matrix([min(a, other) if a is not None else None for a in one.data])
