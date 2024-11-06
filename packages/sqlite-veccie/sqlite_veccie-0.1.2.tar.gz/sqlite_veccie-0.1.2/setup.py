# NB: Most package information resides in pyproject.toml!

from setuptools import Extension, setup

# Build the veccie sqlite extension and include it with the package.
#
# This is a bit cheeky: here we pretend to setuptools that our sqlite extension
# is in fact a Python extension module. Like Python extensions, sqlite
# extensions just need compiling as a shared library and installing somewhere
# accessible. Since setuptools (nor Python) will never actually attempt to load
# the module, they'll never know!
setup(
    ext_modules=[
        Extension(
            name="sqlite_veccie.veccie",
            sources=["veccie.c"],
        ),
    ]
)
