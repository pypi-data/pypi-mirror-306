# setup.py

from setuptools import setup, find_packages

setup(
    name="math_toolkit",
    version="0.1.0",
    author="Prachi Kabra",
    author_email="kabraprachi9@gmail.com",
    description="A simple math toolkit package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/prachikabra121/mathToolkit",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
