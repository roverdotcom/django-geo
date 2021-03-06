from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from setuptools import setup, find_packages

setup(
    name='django-geo',
    version='0.0.2',
    description='Zip codes and basic geographic support library',
    author='Philip Kimmey',
    author_email='philip@rover.com',
    url='https://github.com/philipkimmey/django-geo',
    packages=find_packages(exclude=('tests', 'docs'))
)
