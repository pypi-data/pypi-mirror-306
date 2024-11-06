# setup.py

from setuptools import setup, find_packages

setup(
    name='ayush_py',  # The name of your package
    version='0.1.0',   # Initial version of your package
    packages=find_packages(),  # Automatically find all the packages
    install_requires=[],  # List of dependencies (empty in this case)
    long_description=open('README.md').read(),  # Use the README as long description
    long_description_content_type='text/markdown',
    author='Ayush Mehrotra',
    author_email='ayush.mehrotra900@gmail.com',
    description='A simple Python package for greeting people.',
    url='https://github.com/yourusername/mypackage',  # Replace with your GitHub URL
    classifiers=[  # Optional metadata to help others find your package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
