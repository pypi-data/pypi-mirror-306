# setup.py

from setuptools import setup, find_packages

setup(
    name='masterdef',
    version='0.1',
    packages=find_packages(),
    description='Library for Excel validation and formatting',
    author='Prajwal Bhagwat',
    author_email='app.architecturer@gmail.com',
    install_requires=[
        'openpyxl>=3.0.0',
    ],
)
