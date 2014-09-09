#!/usr/bin/env python

#from distutils.core import setup

from setuptools import setup, find_packages
import glob
import os

home = os.path.expanduser("~")

setup(
    name = 'cloudmesh',
    version = __import__('cloudmesh').version(),
    description = 'A tool to simplify managing multiple clouds including bare metal provisioning',
    #description-file =
    #    README.rst
    author = 'Cloudmesh Team',
    author_email = 'laszewski@gmail.com',
    url = 'http://github.org/cloudmesh/cloudmesh',
    classifiers = [
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Clustering',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Boot',
        'Topic :: System :: Systems Administration',
        'Framework :: Flask',
        'Environment :: OpenStack',
        ],
    packages = find_packages(),
    include_package_data = True,
    data_files = [
        (home + '/.cloudmesh', [
            'etc/FGLdapCacert.pem',
            'etc/sierra-cacert.pem',
            'etc/cloudmesh_flavor.yaml']),
        (home + '/.cloudmesh/etc', [
            'etc/cloudmesh.yaml',
            'etc/me-none.yaml',
            'etc/cloudmesh.yaml',
            'etc/cloudmesh_server.yaml',
            'etc/cloudmesh_rack.yaml',
            'etc/cloudmesh_celery.yaml',
            'etc/cloudmesh_mac.yaml',
            'etc/cloudmesh_flavor.yaml']),
        (home + '/.cloudmesh/etc/racks/diag', glob.glob('etc/racks/*'))            
    ],
#               'cloudmesh/etc/racks/diag = etc/racks/*
    entry_points={'console_scripts': [
        'cm-manage = cloudmesh.config.cm_manage:main',
        'cm-iu = cloudmesh_install:iu_credential_fetch_command',        
        'cm-init = cloudmesh.config.cm_init:main',
        'cm-image  = cloudmesh.image.cm_image:main',
        'cm-metric = cloudmesh.metric.cm_metric:main',
        'cm-rain = cloudmesh.rain.cobbler.cobbler_rain:main',
    ]},    

)

