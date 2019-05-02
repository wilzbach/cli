# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
from setuptools.command.install import install

from cli.version import version


classifiers = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Programming Language :: Python :: 3.7',
    'Topic :: Office/Business',
    'Topic :: Software Development :: Build Tools',
]

keywords = [
    'asyncy',
    'devops',
    'devtools',
    'microservices',
    'orchestration',
    'serverless',
    'storyscript',
]

requirements = [
    'asyncio==3.4.3',
    'click-help-colors==0.5',
    'click-spinner==0.1.8',
    'click==7.0',
    'emoji==0.5.0',
    'raven==6.9.0',
    'requests==2.20.0',
    'storyscript==0.18.1',
    'texttable==1.4.0',
    'pyyaml==3.13',
    'pytz==2018.5'
]


setup(name='asyncy',
      version=version,
      description='Asyncy CLI',
      long_description='',
      classifiers=classifiers,
      download_url='https://github.com/asyncy/cli/archive/master.zip',
      keywords=' '.join(keywords),
      author='Asyncy',
      author_email='hello@asyncy.com',
      url='http://docs.asyncy.com/cli',
      license='MIT',
      packages=find_packages(exclude=['scripts', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=requirements,
      extras_require={},
      entry_points={
          'console_scripts': ['asyncy=cli.main:cli']
      })
