from setuptools import setup, find_packages

setup(
    name="aae",
    version="0.1.0",
    description="aae is a collection of libraries for building AI applications",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
