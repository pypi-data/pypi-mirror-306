# setup.py
from setuptools import setup, find_packages

setup(
    name='Textrix',  # Unique project name
    version='0.1.0',  # Starting version
    description='A text processing utility package',
    author='Priyanshi Mehta',  # Your name
    author_email='dhwani2003@gmail.com',  # Your email address
    url='https://github.com/priyanshi58/Textrix',  # Link to your repository
    packages=find_packages(),  # Automatically find and include all packages
    install_requires=[],  # List dependencies here if any, e.g., ['numpy', 'pandas']
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify Python version compatibility
)
 
