#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='conjugaison',
      version='0.2.0',
      description='Practice Conjugaison',
      author='Luyao Zou',
      packages=find_packages('.'),
      entry_points={
          'gui_scripts': [
              'conjugaison = app:launch',
          ]},
      install_requires=[
          'PyQt5>=5.10',
      ],
      license='MIT',
      )
