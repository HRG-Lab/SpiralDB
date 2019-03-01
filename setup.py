from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='spiraldb',
    version='0.1.0',
    description='Provides an abstraction for interacting with the Spiral Database',
    license='MIT',
    long_description=long_description,
    author='Ryan Campbell',
    author_email='rdcampbell1990@gmail.com',
    packages=['spiraldb'],
    install_requires=['sqlalchemy', 'pandas']
)