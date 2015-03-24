#!/usr/bin/env python

version = "2.2.0"


import os

try:
    from cloudmesh_base.util import banner
except:
    os.system("pip install cloudmesh_base")

from cloudmesh_base.util import banner
from cloudmesh_base.util import auto_create_version

banner ("Generate and Install Version")

auto_create_version("cloudmesh", version,"version.py")

from setuptools import setup, find_packages
from setuptools.command.install import install
import glob


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


class UploadToPypi(install):
    """Upload the package to pypi."""
    def run(self):
        auto_create_version("cloudmesh", version)
        os.system("python setup.py install")
        banner("Build Distribution")
        os.system("python setup.py sdist --format=bztar,zip upload")


class RegisterWithPypi(install):
    """Upload the package to pypi."""
    def run(self):
        banner("Register with Pypi")
        os.system("python setup.py register")


setup(
    name='cloudmesh',
    version=version,
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
        'pypi': UploadToPypi,
        'pypiregister': RegisterWithPypi,
        },
    # install_requires=requirements,
    # dependency_links=[
    #   'git+https://github.com/cloudmesh/timestring.git#egg=timestring-1.6.2.1',
    # ]
)
