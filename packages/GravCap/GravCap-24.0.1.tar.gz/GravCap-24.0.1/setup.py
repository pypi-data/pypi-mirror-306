from setuptools import setup, find_packages

setup(
    name="GravCap",
    version="24.0.1",
    author="Narender Kumar",
    author_email="bansalnarender25@gmail.com",
    description="GravCap is a Python tool designed to calculate the gravimetric storage capacity of hydrogen molecules adsorbed on the materials. This utility determines the theoretical weight-based storage capacity.",
    long_description="Calculate the weight percent (wt%) of H2 molecules adsorbed on the system. This library uses the mendeleev library for the molar mass contributions of user-defined atomic species.",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "mendeleev"  # dependencies
    ],
    entry_points={
        'console_scripts': [
            'GravCap=GravCap.GravCap:main'  # Entry point with capital letters
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
