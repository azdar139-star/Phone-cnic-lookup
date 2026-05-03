"""
Setup Script for Phone & CNIC Lookup Tool
Install dependencies and initialize application
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="phone-cnic-lookup",
    version="1.0.0",
    author="azdar139-star",
    description="A command-line tool to find phone numbers and CNIC details with ownership information",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/azdar139-star/phone-cnic-lookup",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "colorama>=0.4.6",
        "tabulate>=0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "phone-cnic-lookup=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
