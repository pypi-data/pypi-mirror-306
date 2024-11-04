#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Pintaudi Giorgio

"""WAGASCI ANPAN for Python"""

import glob

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

extras = {
    'with_borg': ['borgbackup>=1.1.11']
}

setup(
    name='wagascianpy',
    version='0.3.9',
    author='Pintaudi Giorgio',
    author_email='giorgio.pimpa@gmail.com',
    include_package_data=True,
    zip_safe=True,
    keywords="WAGASCI ANPAN for Python",
    description='WAGASCI ANPAN for Python',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://git.t2k.org/wagasci_babymind/WagasciAnpy',
    packages=find_packages(),
    scripts=glob.glob('scripts/calibration/*.py') +
            glob.glob('scripts/data_quality/*.py') +
            glob.glob('scripts/mapping/*.py') +
            glob.glob('scripts/plotting/*.py') +
            glob.glob('scripts/viewer/*.py'),
    license='GPLv3',
    extras_require=extras,
    package_data={
        'wagascianpy': ['viewer/gui.ui', '*.rst', '**/*.rst'],
    },
    data_files=[
        ('wagasci/databases', glob.glob('../WagasciAnpy/databases/*')),
        ('wagasci/docs/images', glob.glob('../WagasciAnpy/docs/images/*'))
    ],
    install_requires=[
        'setuptools >= 72.1.0',
        'bitarray >= 0.8.1',
        'six >= 1.16.0',
        'paramiko >= 3.3.2',
        'scp >= 0.7.1',
        'pytz >= 2024.2',
        'tinydb >= 3.15.2',
        'recordclass >= 0.13.2',
        'pyfakefs >= 3.7.2',
        'numpy >= 1.26.4',
        'undecorated >= 0.3.0',
        'dependency_injector >= 3.15.6',
        'inflection >= 0.3.1',
        'pygubu >= 0.35.5',
        'typing >= 3.5.2.2',
        'mock >= 1.0.15.6'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: X11 Applications',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
    ],
)
