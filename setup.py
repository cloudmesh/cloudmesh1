#!/usr/bin/env python
requirements = """
    # ######################################################################
    # Basic environment
    # ######################################################################
    #
    future
    pip
    #
    # ######################################################################
    # Sphinx
    # ######################################################################
    #
    sphinx
    sphinx_bootstrap_theme
    sphinxcontrib-autorun
    sphinxcontrib-blockdiag
    sphinxcontrib-exceltable
    sphinxcontrib-webmocks
    actdiag
    blockdiag
    blockdiagcontrib-square
    blockdiagcontrib-qb
    blockdiagcontrib-class
    blockdiagcontrib-cisco
    nwdiag
    seqdiag
    sphinxcontrib-httpdomain 
    #
    # ######################################################################
    # Packages which must be installed first
    # ######################################################################
    #
    paramiko
    pycrypto
    fabric
    #
    # ######################################################################
    # Console and commandline Related
    # ######################################################################
    #
    blessings
    progress
    sh
    console
    python-hostlist
    docopt
    cmd3>=1.1.0
    #
    # ######################################################################
    # Databases and directories
    # ######################################################################
    #
    python-ldap
    pyaml
    pyyaml
    pymongo
    mongoengine
    #
    # ######################################################################
    # Rabbitmq
    # ######################################################################
    #
    librabbitmq
    #
    # ######################################################################
    # Flask
    # ######################################################################
    #
    WTForms
    Flask>=0.10.1
    Flask-WTF>=0.9.3
    Flask-AutoIndex
    Flask-Silk
    flask_login
    Flask-OpenID
    flask-principal
    Flask-RSTPages
    flask-restful
    flask-restful-swagger
    #
    # ######################################################################
    # Testing and formatting
    # ######################################################################
    #
    nose
    autopep8
    #
    # ######################################################################
    # OpenStack and cloud
    # ######################################################################
    #
    apache-libcloud==0.14.1
    python-novaclient
    python-keystoneclient
    azure
    #
    # ######################################################################
    # Parallel tools
    # ######################################################################
    #
    celery
    flower
    psutil
    #
    # ######################################################################
    # General Libraries
    # ######################################################################
    #
    simple-json
    pytimeparse
    timestring
    prettytable
    tabulate
    passlib
    # ######################################################################
    # ipython
    # ######################################################################
    #
    ipython
    pyzmq
    tornado
    # ######################################################################
    # General Libraries
    # ######################################################################
    #
    fake-factory
    ecdsa
    #
"""

def auto_install_requirements_from_string(requirements):
    lines = requirements.split("\n")

    r = []
    for line in lines:
        line = line.strip()
        if not line.startswith("#") and line != '':
            r.append(line)
    return r

requirements = auto_install_requirements_from_string(requirements)

#from distutils.core import setup


from setuptools import setup, find_packages
from setuptools.command.install import install
import glob
import os

# try:
#     from fabric.api import local
# except:
#     os.system("pip install fabric")
#     from fabric.api import local

home = os.path.expanduser("~")

class InstallTest(install):
    """Test of a custom install."""
    def run(self):
        print "Install Test"
        #install.run(self)


setup(
    name='cloudmesh',
    version=__import__('cloudmesh').version(),
    description='A tool to enable federated management of multiple clouds including Azure, AWS, Eucalyptus, OpenStack',
    # description-file =
    #    README.rst
    author='Cloudmesh Team',
    author_email='laszewski@gmail.com',
    url='http://github.org/cloudmesh/cloudmesh',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
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
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        (home + '/.cloudmesh', [
            'etc/FGLdapCacert.pem',
            'etc/india-havana-cacert.pem',
            'etc/cloudmesh_flavor.yaml']),
        (home + '/.cloudmesh/etc', [
            'etc/cloudmesh.yaml',
            'etc/me-none.yaml',
            'etc/cloudmesh.yaml',
            'etc/cloudmesh_server.yaml',
            'etc/cloudmesh_rack.yaml',
            'etc/cloudmesh_celery.yaml',
            'etc/cloudmesh_mac.yaml',
            'etc/cloudmesh_flavor.yaml',
            'etc/ipython_notebook_config.py']),
        (home + '/.cloudmesh/etc/racks/diag', glob.glob('etc/racks/*'))
    ],
    #               'cloudmesh/etc/racks/diag = etc/racks/*
    entry_points={'console_scripts': [
        'cm-manage = cloudmesh.config.cm_manage:main',
        'cm-iu = cloudmesh_install.futuregrid:main',
        'cm-init = cloudmesh.config.cm_init:main',
        'cm-image  = cloudmesh.image.cm_image:main',
        'cm-metric = cloudmesh.metric.cm_metric:main',
        'cm-rain = cloudmesh.rain.cobbler.cobbler_rain:main',
        'cm-admin = cloudmesh_admin.admin:main',        
    ]},
    cmdclass={
        'custom': InstallTest,
        },
    install_requires=requirements,
)
