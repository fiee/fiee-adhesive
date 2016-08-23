# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from setuptools import setup, find_packages
import os

setup(name='fiee-adhesive',
      version='0.0.10',
      description='Sticky notes for your (dorsale based) django models',
      keywords='sticky notes generic attachment',
      author='Henning Hraban Ramm',
      author_email='hraban@fiee.net',
      license='BSD',
      url='https://github.com/fiee/fiee-adhesive',
      download_url='https://github.com/fiee/fiee-adhesive/tarball/master',
      package_dir={'adhesive': 'adhesive',},
      packages=find_packages(),
      include_package_data = True,
      package_data = {'': ['*.rst', 'locale/*/LC_MESSAGES/*.*', 'templates/*/*.*', 'templates/*/*/*.*', 'static/*/*/*.*']},
      # see http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Utilities',
                   'Natural Language :: English',
                   'Natural Language :: German',],
      install_requires=['Django>=1.8', 'django-registration>=2', 'fiee-dorsale>=0.1.2',],
      zip_safe=False,
      )
