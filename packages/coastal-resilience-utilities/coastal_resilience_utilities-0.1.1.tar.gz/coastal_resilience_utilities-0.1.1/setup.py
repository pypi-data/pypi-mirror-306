from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]


setup(
    name='coastal_resilience_utilities',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['**/*.csv', "**/*.txt"]},
    install_requires=parse_requirements('requirements-freeze.txt'),
    author='Chris Lowrie',
    author_email='chlowrie@ucsc.edu',
    description='Utilities for conducting coastal resilience assessments',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://git.ucsc.edu/chlowrie/coastal-resilience-utilities',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12.3',
)