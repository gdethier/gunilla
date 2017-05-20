from setuptools import setup, find_packages
import sys


sys.path.append('src');

setup(
    name='wplab-theme-builder',

    version='0.1.0.dev1',

    description='WPLab theme builder',
    long_description='WPLab theme builder',

    url='https://github.com/gdethier',

    author='Gerard Dethier',
    author_email='g.dethier@gmail.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],

    keywords='wordpress themes',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[],

    extras_require={
        'dev': [],
        'test': [],
    },

    package_data={
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'wplab-builder=wplab.theme_builder:main',
        ],
    },
)
