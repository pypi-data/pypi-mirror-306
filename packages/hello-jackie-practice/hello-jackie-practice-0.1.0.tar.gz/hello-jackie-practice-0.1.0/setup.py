from setuptools import setup
from setuptools import find_packages

setup(
    name='hello-jackie-practice',  # package name
    version='0.1.0',  # package version
    description='my first package',  # package description
    packages=find_packages(),
    zip_safe=False,
)