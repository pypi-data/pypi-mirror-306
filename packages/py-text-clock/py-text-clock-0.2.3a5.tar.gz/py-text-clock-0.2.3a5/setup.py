from setuptools import setup, find_packages
import io
from os import path
requirements = [l.strip() for l in open('requirements.txt').readlines()]

# Get the long description from the README file

here = path.abspath(path.dirname(__file__))

with io.open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# This gets deployed when a new release is made by github actions
VERSION = '0.2.3a5'

setup(
    name='py-text-clock',
    url='https://github.com/manojmanivannan/py-clock',
    version=VERSION,
    author='Manoj Manivannan',
    author_email='manojm18@live.in',
    description='A verbose Clock',
    long_description=long_description,
    packages=find_packages(),
    entry_points={
    'console_scripts': ['py-clock=source.command_line:main'],
    },
    install_requires=requirements,
    setup_requires=['wheel','setuptools'],
    include_package_data=True,
)
