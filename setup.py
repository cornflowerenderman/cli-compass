#!/bin/python3
# Incomplete but kinda working

import os
from setuptools import setup, find_packages

setup(
    include_package_data=True,
    name='cli-compass',
    version='0.1.0',
    description='A command line interface for Compass Education',
    packages=find_packages(),
    url='https://github.com/cornflowerenderman/cli-compass',
    license='MIT',
    author='cornflowerenderman',
    author_email='cornflowerenderman@duck.com',
    python_requires='>=3.8.0',
    install_requires=['pytz>=2023.3.post1', 'colorama>=0.4.6', 'browser-cookie3>=0.19.1', 'beautifulsoup4>=4.12.2']
)