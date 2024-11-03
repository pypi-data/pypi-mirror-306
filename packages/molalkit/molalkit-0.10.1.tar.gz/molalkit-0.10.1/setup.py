import io
import os
import re
import setuptools

with open('molalkit/__init__.py') as fd:
    __version__ = re.search("__version__ = '(.*)'", fd.read()).group(1)


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


long_description = read('README.md')

setuptools.setup(
    name='molalkit',
    version=__version__,
    python_requires='>=3.8',
    install_requires=[
        'typed-argument-parser',
        'rdkit',
        'mgktools'
    ],
    entry_points={
        'console_scripts': [
            'molalkit_run=molalkit.al.run:molalkit_run',
            'molalkit_run_from_cpt=molalkit.al.run:molalkit_run_from_cpt',
        ]
    },
    author='Yan Xiang',
    author_email='yan.xiang@duke.edu',
    description='MolALKit: A Toolkit for Active Learning in Molecular Data.',
    long_description=long_description,
    url='https://github.com/RekerLab/MolALKit',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
    package_data={'': ['data/datasets/*.csv', 'models/configs/*Config']}
)
