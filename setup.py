#!/usr/bin/env python
import os
import sys
from setuptools import setup

if "testpublish" in sys.argv[-1]:
    os.system("python setup.py sdist upload -r pypitest")
    sys.exit()
elif "publish" in sys.argv[-1]:
    os.system("python setup.py sdist upload -r pypi")
    sys.exit()

# Load the __version__ variable without importing the package
exec(open('shark/version.py').read())

entry_points = {'console_scripts':
                ['shark = shark.ui:shark']}

setup(name='shark',
      version=__version__,
      description="Uses supervised machine learning on Kepler/K2 data. ",
      long_description=open('README.rst').read(),
      author='Christina Hedges',
      author_email='christina.l.hedges@nasa.gov',
      license='MIT',
      packages=['shark'],
      package_data={'shark': ['data/*']},
      install_requires=['astropy>=0.4',
                        'numpy',
                        'pandas',
                        'scikit-learn'],
      entry_points=entry_points,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Intended Audience :: Science/Research",
          "Topic :: Scientific/Engineering :: Astronomy",
          ],
      )
