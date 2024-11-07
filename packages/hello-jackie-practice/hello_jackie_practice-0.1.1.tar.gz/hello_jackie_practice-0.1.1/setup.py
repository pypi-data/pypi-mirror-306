from setuptools import setup
from setuptools import find_packages

setup(
    name='hello_jackie_practice',  # package name
    version='0.1.1',  # package version
    description='my first package',  # package description
    packages=find_packages(),
    zip_safe=False,
)