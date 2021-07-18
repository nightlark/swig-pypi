#!/usr/bin/env python

import os
import sys
from distutils.text_file import TextFile
from skbuild import setup

with open('README.md', 'r') as fp:
    readme = fp.read()

setup(
    name='swig',
    package_dir={'': 'src'},
    packages=['swig'],
    cmake_install_dir='src/swig/data',
    entry_points={
        'console_scripts': [
            'swig=swig:swig'
        ]
    },

    url='http://www.swig.org/',
    download_url='http://www.swig.org/download.html',
    description='SWIG is a software development tool that connects '
            'programs written in C and C++ with a variety of '
            'high-level programming languages.',
    long_description=readme,
    long_description_content_type='text/markdown',

    classifiers=[
        'OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Other/Proprietary License',
        'Programming Language :: C',
        'Programming Language :: C++',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools'
    ],
    license='pick a license',
    keywords='swig build c c++',
)
