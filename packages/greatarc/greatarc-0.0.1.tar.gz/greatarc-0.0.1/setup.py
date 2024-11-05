# setup.py
from setuptools import setup, find_packages

setup(
    name="greatarc",
    version="0.0.1",
    description="A sample Python package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ziqi Li",
    author_email="liziqi1992@gmail.com",
    url="https://github.com/Ziqi-Li/greatarc",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
