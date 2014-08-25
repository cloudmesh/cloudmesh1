#!/usr/bin/env python

from distutils.core import setup

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
    packages = [
        'cloudmesh_cmd3',
        'cloudmesh',
        'cloudmesh_install',
        'cloudmesh_common'
    ],
  entry_points={'console_scripts': [
    'cm-manage = cloudmesh.config.cm_manage:main',
    'cm-init = cloudmesh.config.cm_init:main',
    'cm-image  = cloudmesh.image.cm_image:main',
    'cm-metric = cloudmesh.metric.cm_metric:main',
    'cm-rain = cloudmesh.rain.cobbler.cobbler_rain:main',
    ]},    

)

"""
[install]
install-data=$HOME


data_files =
    .cloudmesh = etc/FGLdapCacert.pem
    .cloudmesh = etc/sierra-cacert.pem
    .cloudmesh/etc/racks/diag = etc/racks/*
    .cloudmesh/etc = etc/cloudmesh.yaml
    .cloudmesh/etc = etc/me-none.yaml
    .cloudmesh/etc = etc/cloudmesh.yaml
    .cloudmesh/etc = etc/cloudmesh_server.yaml
    .cloudmesh/etc = etc/cloudmesh_rack.yaml
    .cloudmesh/etc = etc/cloudmesh_celery.yaml
    .cloudmesh/etc = etc/cloudmesh_mac.yaml
    .cloudmesh/etc = etc/cloudmesh_flavor.yaml
    .cloudmesh = etc/cloudmesh_flavor.yaml

"""
