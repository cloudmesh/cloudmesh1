"""Cloud Mesh: managing multiple virtual machines in Clouds

This project allows you to manage multiple virtual machines.
In future you will be able ta add multipl eclouds.
"""

from setuptools import setup, find_packages
import sys, os

filename = "VERSION.txt"
version = open(filename).read()


# due to a bug we are not including VERION.py yet
# execfile('VERSION.py)

classifiers = """\
Intended Audience :: Developers
Intended Audience :: Education
Intended Audience :: Science/Research
Development Status :: 4 - Beta
Intended Audience :: Developers
License :: OSI Approved :: Apache Software License
Programming Language :: Python
Topic :: Database
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: POSIX :: Linux
Programming Language :: Python :: 2.7
Operating System :: MacOS :: MacOS X
Topic :: Scientific/Engineering
Topic :: System :: Clustering
Topic :: System :: Distributed Computing
"""

if sys.version_info < (2, 7):
    _setup = setup
    def setup(**kwargs):
        if kwargs.has_key("classifiers"):
            del kwargs["classifiers"]
        _setup(**kwargs)

doclines = __doc__.split("\n")


setup(
    name='cloudmesh',
    version=version,
    description = doclines[0],
    classifiers = filter(None, classifiers.split("\n")),
    long_description = "\n".join(doclines[2:]),
    keywords='Cloud FutureGrid OpenStack',
    maintainer='Gregor von Laszewski',
    maintainer_email="laszewski@gmail.com",
    author='Gregor von Laszewski',
    author_email='laszewski@gmail.com',
    url='https://github.com/futuregrid/cm',
    license='Apache 2.0',
    package_dir = {'': '.'},
    packages = find_packages(exclude=['ez_setup', 'examples', 'tests']),
    
    #include_package_data=True,
    #zip_safe=True,
    #install_requires=[
    #    # -*- Extra requirements: -*-
    #],

    
#    entry_points={
#        'console_scripts': [
#                'cm = fgvirtualcluster.FGCluster:commandline_parser',
#                'fg-csh = fgvirtualcluster.FGShell:main',
#             ]},

    install_requires = [
             'setuptools',
             'pip',
             'paramiko',
             'blessings',
             'fabric',
             'progress',
             'sh',
             "console",
             ],

#    scripts=['bin/cm', 'bin/cm']

    )

    #http://pypi.python.org/pypi/progress/1.0.2
