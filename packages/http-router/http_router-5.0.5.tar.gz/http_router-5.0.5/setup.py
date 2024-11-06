"""Setup the library."""

import os
import sys

from setuptools import setup

try:
    from Cython.Build import cythonize
except ImportError:
    cythonize = None


NO_EXTENSIONS = (
    sys.implementation.name != "cpython"
    or bool(os.environ.get("HTTP_ROUTER_NO_EXTENSIONS"))
    or cythonize is None
)

print("*********************")
print("* Pure Python build *" if NO_EXTENSIONS else "* Accelerated build *")
print("*********************")

setup(
    setup_requires=["wheel"],
    ext_modules=[]
    if NO_EXTENSIONS or cythonize is None
    else cythonize("http_router/*.pyx", language_level=3),
)
