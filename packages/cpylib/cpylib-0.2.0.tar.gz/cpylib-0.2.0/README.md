# My C Library

My C Library is a Python package that allows you to execute C code from within Python. It uses a C extension to provide fast execution of C code, making it suitable for performance-critical applications.
Url code: https://github.com/hqmdokkai/cpylib.git
## Features

- Execute arbitrary C code from Python.
- Lightweight and easy to use.
- Fast execution due to native C performance.

## Installation

You can install the package using pip:

```bash
pip install cpylib
```
Usage
Here's a quick example of how to use the library:
```bash
import cpylib

#Execute C code to print the sum of 5 and 1
cpylib.c("printf(\"%d\\n\", 5 + 1);")
