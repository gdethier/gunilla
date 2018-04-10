from setuptools import setup, find_packages
import sys

sys.path.append('src');

setup(
    name='gunilla',

    version='0.2.0.dev1',

    description='Gunilla',
    long_description='Gunilla',

    url='https://github.com/gdethier/gunilla',

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

    keywords='wordpress',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[
        'docker'
    ],

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
            'gnl=gunilla:main',
        ],
    },
)
