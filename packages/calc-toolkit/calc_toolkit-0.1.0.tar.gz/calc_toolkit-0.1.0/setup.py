# setup.py
from setuptools import setup, find_packages

setup(
    name="calc_toolkit",
    version="0.1.0",
    author="Pankaj Verma",
    author_email="pankajver@gmail.com",
    description="Calc toolkit package for basic geometric calculations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Pankaj01111/calc_tootkit",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # Specify dependencies here if needed, e.g., "numpy>=1.18.0",
    ],
)
