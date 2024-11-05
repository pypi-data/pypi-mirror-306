from setuptools import setup, find_packages

setup(
    name="fgv",
    version="0.1.0",
    description="fgv is a collection of libraries for building AI applications",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'fgv = name_register:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
