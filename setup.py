#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='tig',
      version='0.1',
      description='TiG: TiG isn\'t Git',
      author='Salvatore Caputi',
      author_email='salvatore@scaputi.net',
      #url='https://www.python.org/sigs/distutils-sig/',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      entry_points = {
        'console_scripts':
            ['tig = tig:main'],
      }
     )
