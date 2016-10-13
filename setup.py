#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='pyfreebilling',
      version='1.7.0',
      description='Softswitch billing app.',
      author='Mathias WOLFF',
      author_email='mathiaswolff@mac.com',
      url='https://bitbucket.org/mwolff/pyfreebilling/',
      packages=find_packages(),
      license='License :: AGPL v3',

      # Enable django-setuptest
      test_suite='setuptest.setuptest.SetupTestSuite',
      tests_require=(
        'django-setuptest',
        # Required by django-setuptools on Python 2.6
        'argparse'
      ),
)
