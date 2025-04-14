"""
    This file is part of astrovedic - (C) FlatAngle
    Modified by Manan Ramnani (ramnani.manan@gmail.com)
    Original Author: João Ventura (flatangleweb@gmail.com)

"""

from setuptools import setup
from setuptools import find_packages

setup(
    # Project
    name='astrovedic',
    version='0.3.0',

    # Sources
    packages=find_packages(),
    package_data={
        'astrovedic': [
            'resources/README.md',
            'resources/swefiles/*'
        ],
    },

    # Dependencies
    install_requires=['pyswisseph==2.10.3.2'],

    # Metadata
    description='Python library for Vedic and Traditional Astrology',
    url='https://github.com/cryptekbits/astrovedic',
    keywords=['Astrology', 'Vedic Astrology', 'Traditional Astrology'],
    license='MIT',

    # Authoring
    author='Manan Ramnani',
    author_email='ramnani.manan@gmail.com',

    # Classifiers
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
