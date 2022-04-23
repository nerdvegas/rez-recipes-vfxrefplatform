#!/usr/bin/env python

import multiprocessing
import os
import re
import shutil
import subprocess
import sys

SOURCE_TAR = "src/cmake-{version}.tar.gz"

CONFIGURE_ENV = {
    "linux_x86_64_rocky-8.5": {
        "CFLAGS": "-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions "
                  "-fstack-protector-strong --param=ssp-buffer-size=4 "
                  "-grecord-gcc-switches -m64 -mtune=generic ",
        "LDFLAGS": "-Wl,-z,relro,-rpath={config.package_path}/lib64"
    }
}

#CONFIGURE_OPTS = {
#    "linux_x86_64_rocky-8.5": #"--build=x86_64-unknown-linux-gnu "
#                              #"--host-x86_64-unknown-linux-gnu "
#                              "--prefix={config.package_path} --enable-ipv6 "
#                              "--enable-shared "
#                              "--with-dbmliborder=gdbm:ndbm:bdb "
#                              "--with-system-expat --with-system-ffi "
#                              # "--enable-optimizations "
#                              "--without-ensurepip "
#}



def build():

    if not build_config.is_installing:
        raise SystemExit("ERROR: This build must be run in a mode which would install or release it")

    source_tar = os.path.join(build_config.source_path, SOURCE_TAR.format(version=build_config.package_version))

    _build_and_install_payload(source_tar)
    
    if build_config.is_releasing:
        _lock_payload()

def _build_and_install_payload(source_tar):
    cmake_file = os.path.join(build_config.build_path, "CMakeLists.txt")
    with open(cmake_file, "w") as outstream:
        _generate_cmakelists(source_tar, stream=outstream)

    subprocess.check_call(["cmake", "."], cwd=build_config.build_path)
    subprocess.check_call(["make"], cwd=build_config.build_path)

def _generate_cmakelists(source_tar, stream=sys.stdout):
    """
    Args:
        source_tar (str): Path to source tarball
        stream (file): Output file stream
    """
    qt_gui_enable = "" # possibly hook this up to a qt variant in future
    if 'REZ_QT_ROOT' in os.environ:
        qt_gui_enable = "--qt-gui"

    configure_env = ""
    for name, value in CONFIGURE_ENV[build_config.build_variant_str].items():
        _str = ' "{var}={value}"'.format(var=name, value=value.format(config=build_config))
        configure_env += _str

    # configure_opts = CONFIGURE_OPTS[build_config.build_variant_str].format(config=build_config)

    stream.write("""
cmake_minimum_required(VERSION 3.0)

project(cmake CXX)

include(ExternalProject)

ExternalProject_Add(
    {config.package_name}
    URL {source_tarfile}
    PREFIX {config.package_name}
    SOURCE_DIR build
    CONFIGURE_COMMAND env {configure_env} ./bootstrap --prefix={config.package_path} {qt_gui_enable} --parallel={cpus} --system-curl
    BUILD_IN_SOURCE 1
    BUILD_COMMAND make -j{cpus}
    INSTALL_DIR {config.package_path}
)
""".format(
            config=build_config,
            source_tarfile=source_tar,
            configure_env=configure_env,
            # configure_opts=configure_opts,
            qt_gui_enable=qt_gui_enable,
            cpus=multiprocessing.cpu_count(),
        )
    )

def _lock_payload():
    path = os.path.dirname(build_config.package_path)
    subprocess.check_call(["/bin/chmod", "-R", "a-w", path])


class BuildConfig(object):
    def __init__(self):
        self.source_path = os.environ["REZ_BUILD_SOURCE_PATH"]
        self.build_path = os.environ["REZ_BUILD_PATH"]
        self.package_path = os.environ["REZ_BUILD_INSTALL_PATH"]
        self.package_name = os.environ["REZ_BUILD_PROJECT_NAME"]
        self.package_version = os.environ["REZ_BUILD_PROJECT_VERSION"]

    @property
    def is_installing(self):
        return os.environ["REZ_BUILD_INSTALL"] == '1'

    @property
    def is_releasing(self):
        return os.environ["REZ_BUILD_TYPE"] in ["central"]

    @property
    def build_variant_str(self):
        desc = "{platform}_{arch}_{os}".format(
            platform=os.environ["REZ_PLATFORM_VERSION"],
            arch=os.environ["REZ_ARCH_VERSION"],
            os=os.environ["REZ_OS_VERSION"],
        )
        return desc

build_config = BuildConfig()

if __name__ == "__main__":
    build()
