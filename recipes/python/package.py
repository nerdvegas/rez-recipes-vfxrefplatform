# -*- coding: utf-8 -*-

@early()
def name():
    import os
    name = os.path.basename(os.path.dirname(os.getcwd()))
    return name

@early()
def version():
    import os
    version = os.path.basename(os.getcwd())
    return version

@early()
def uuid():
    import uuid
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, name()))

description = \
    """
    An interpreted, interactive, object-oriented programming language
    """

vendor_name = "Python Software Foundation"

vendor_type = "external"

opensource = True

source_author = vendor_name

source_license = "PSF"

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
    'cmake-3'
    # build command requires a system-level python interpreter
    # expat-devel is installed at system-level
]

build_command = "python {root}/build.py {install}"
#build_command = "/bin/true" # temp while I work on the definition

variants = [
    ['platform-linux', 'arch-x86_64', 'os-rocky-8.5']
]

@early()
def variants():
    from rez.package_py_utils import expand_requires
    requires = ["platform-linux", "arch-x86_64", "os-**"]
    return [expand_requires(*requires)]

def pre_commands():
    env.PYTHONHOME.unset()

def commands():
    env.PATH.prepend("{this.root}/bin")

tests = {
    "python_runs": 'echo [[ "$(python -c \'import os; import sys; print(\".\".join(str(x) for x in sys.version_info[:3]))\')" -eq "{version}" ]]'.format(version=version())
}

has_plugins = True
plugin_for = ['rez']

with scope('config') as config:
    config.release_packages_path = '${SW_EXTERNAL_RELEASE_ROOT}'

