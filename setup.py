from setuptools import setup, find_packages

setup(
    name="gannpy",  
    version="0.1.8",
    packages=find_packages(),
    install_requires=[
        "pandas",
    ],
    test_suite='tests',
    author="SAI JAYANTH GUJJALA",
    author_email="keshavaradha990@gmail.com",
    description="A package for Gann trading simulation",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
