from __future__ import unicode_literals

import re
from setuptools import setup


def get_version(filename):
    content = open(filename).read()
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", content))
    return metadata['version']


setup(
    name='Mopidy-Scrobbler',
    version=get_version('mopidy_scrobbler/__init__.py'),
    url='https://github.com/mopidy/mopidy-scrobbler',
    license='Apache License, Version 2.0',
    author='Stein Magnus Jodal',
    author_email='stein.magnus@jodal.no',
    description='Mopidy extension for scrobbling played tracks to Last.fm',
    long_description=open('README.rst').read(),
    packages=['mopidy_scrobbler'],
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'Mopidy',
        'Pykka >= 1.1',
        'pylast >= 0.5.7',
    ],
    entry_points={
        'mopidy.ext': [
            'scrobbler = mopidy_scrobbler:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)
