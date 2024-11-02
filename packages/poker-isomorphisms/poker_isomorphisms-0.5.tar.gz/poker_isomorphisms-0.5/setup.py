from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name='poker_isomorphisms',
    version='0.5',
    packages=find_packages(),
    install_requires=[],
    long_description=description,
    long_description_content_type='text/markdown',
)