# Smart Numbers

A Python library to determine if a number is even, odd, or a multiple of a given number.

## Installation
```bash
pip install smart-numbers-YOUR_USERNAME

from numbers_properties_pkg.numbers_properties import NumberProperties

# Create an instance of the NumberProperties class
np = NumberProperties()

# Check if a number is even
print(np.is_even(4))  # Output: True

# Check if a number is odd
print(np.is_odd(3))   # Output: True

# Check if a number is a multiple of another number
print(np.is_multiple_of_n(15, 5))  # Output: True
print(np.is_multiple_of_n(15, 4))  # Output: False
