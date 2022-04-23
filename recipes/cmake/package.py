# -*- coding: utf-8 -*-

name = "cmake"

@early()
def version():
    import os
    version = os.path.basename(os.getcwd())
    return version

@early()
def uuid():
    import uuid
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, name))

description = \
    """
    Open-source and cross-platform family of tools designed to build, test, and package software.
    """

vendor_name = "Kitware"

vendor_type = "external"

opensource = True

source_author = vendor_name

source_license = "BSD 3-clause"

source_type = "c++"

gpl_compatible = True

has_plugins = False

vendor_version = version()

build_type = "python"

package_author = "maxnbk"
build_author = "maxnbk"

relocateable = False

build_requires_source = True
build_requires_internet = False
build_requires_sudo = False

@early()
def tools():
    major, minor = version().split('.')[:2]
    return [
        "2to3",
        "idle",
        "pydoc",
        "python",
        "python{major}".format(major=major),
        "python{major}.{minor}".format(major=major,minor=minor),
        "python{major}.{minor}-config".format(major=major,minor=minor),
        "python{major}-config".format(major=major),
        "python-config",
        "smtpd.py",
    ]

private_build_requires = [
    'gcc-4+',
    # 'cmake-3',
    # build will rely on the system-level cmake installation because we're being meta for now
    # 'python-2.7+<4',
    # build will rely on the system-level python interpreter because python package itself will be built using cmake
]

build_command = "python {root}/build.py {install}"

hashed_variants = True

@early()
def variants():
    from rez.package_py_utils import expand_requires
    requires = ["platform-linux", "arch-x86_64", "os-**"]
    return [expand_requires(*requires)]

def commands():
    env.PATH.prepend("{this.root}/bin")

tests = {
    "version_check": 'echo [[ \\"$(cmake --version | head -n 1)\\" -eq \\"cmake version {version}\\" ]]'.format(version=version())
}

with scope('config') as config:
    config.release_packages_path = '${SW_EXTERNAL_RELEASE_ROOT}'

