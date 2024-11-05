

from setuptools import setup, find_packages

setup(
    name="iranian_validators",
    version="0.1.0",
    description="A package for validating Iranian national code, mobile number, and more.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="MrVafaei",
    author_email="mvmsoft7@gmail.com",
    url="https://mrvafaei.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
