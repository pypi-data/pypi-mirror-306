# maxbits

`maxbits` is a Python module that provides functions to calculate the maximum and minimum values for signed and unsigned integers, as well as floating-point numbers of specified bit widths. This module helps in understanding the range of values that can be represented with different bit sizes.

## Installation

To use the `maxbits` module, simply download the module using pip and import it into your Python script. No additional dependencies are required.

## Functions

### signed_max(x: int) -> int

Calculates the maximum value for a signed integer of the given bit width.

- **Args**: 
  - `x`: Bit width of the signed integer.
- **Returns**: 
  - Maximum value for the signed integer.

### signed_min(x: int) -> int

Calculates the minimum value for a signed integer of the given bit width.

- **Args**: 
  - `x`: Bit width of the signed integer.
- **Returns**: 
  - Minimum value for the signed integer.

### unsigned_max(x: int) -> int

Calculates the maximum value for an unsigned integer of the given bit width.

- **Args**: 
  - `x`: Bit width of the unsigned integer.
- **Returns**: 
  - Maximum value for the unsigned integer.

### unsigned_min(x: int = 0) -> int

Calculates the minimum value for an unsigned integer.

- **Args**: 
  - `x`: Bit width of the unsigned integer (default is 0).
- **Returns**: 
  - Minimum value for the unsigned integer (always 0).

### float_max(x: int) -> float

Calculates the maximum value for a floating-point number of the specified bit width (32 or 64).

- **Args**: 
  - `x`: Bit width of the floating-point number.
- **Returns**: 
  - Maximum value for the floating-point number, or `None` if unsupported.

### float_min(x: int, n: bool = True) -> float

Calculates the minimum positive normalized or denormalized value for a floating-point number of the given bit width.

- **Args**: 
  - `x`: Bit width of the floating-point number (32 or 64).
  - `n`: If `True`, returns the minimum normalized value; if `False`, returns the minimum denormalized value (default is `True`).
- **Returns**: 
  - Minimum value for the floating-point number, or `None` if unsupported.

## Usage Example

```python
from maxbits import signed_max, unsigned_max, float_max

print(signed_max(8))  # Output: 127
print(unsigned_max(8))  # Output: 255
print(float_max(32))  # Output: 3.4028234663852886e+38
```

## License

This module is licensed under the Mozilla Public License 2.0. For more details, please refer to the LICENSE file.