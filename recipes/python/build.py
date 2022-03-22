#!/usr/bin/env python

import multiprocessing
import os
import re
import subprocess
import sys

SOURCE_TAR = "src/Python-{version}.tgz"

CONFIGURE_ENV = {
    "linux_x86_64_rocky-8.5": {
        "CFLAGS": "-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions "
                  "-fstack-protector-strong --param=ssp-buffer-size=4 "
                  "-grecord-gcc-switches -m64 -mtune=generic -D_GNU_SOURCE "
                  "-fPIC -fwrapv",
        "LDFLAGS": "-Wl,-z,relro,-rpath={config.package_path}/lib"
    }
}

CONFIGURE_OPTS = {
    "linux_x86_64_rocky-8.5": #"--build=x86_64-unknown-linux-gnu "
                              #"--host-x86_64-unknown-linux-gnu "
                              "--prefix={config.package_path} --enable-ipv6 "
                              "--enable-shared "
                              "--with-dbmliborder=gdbm:ndbm:bdb "
                              "--with-system-expat --with-system-ffi "
                              # "--enable-optimizations "
                              "--without-ensurepip "
}

def build():
    build_config = BuildConfig()

    if not build_config.is_installing:
        raise SystemExit("ERROR: This build must be run in a mode which would install or release it")

    source_tar = os.path.join(build_config.source_path, SOURCE_TAR.format(version=build_config.package_version))

    _build_and_install_payload(build_config, source_tar)
    _create_unversioned_python_symlink(build_config)

    if build_config.is_releasing:
        _lock_payload(build_config)

def _build_and_install_payload(config, source_tar):
    cmake_file = os.path.join(config.build_path, "CMakeLists.txt")
    with open(cmake_file, "w") as outstream:
        _generate_cmakelists(config, source_tar, stream=outstream)

    subprocess.check_call(["cmake", "."], cwd=config.build_path)
    subprocess.check_call(["make"], cwd=config.build_path)

def _generate_cmakelists(build_config, source_tar, stream=sys.stdout):
    """
    Args:
        build_config (`BuildConfig`): Build configuration
        source_tar (str): Path to source tarball
        stream (file): Output file stream
    """
    configure_env = ""
    for name, value in CONFIGURE_ENV[build_config.build_variant_str].items():
        _str = ' "{var}={value}"'.format(var=name, value=value.format(config=build_config))
        configure_env += _str

    configure_opts = CONFIGURE_OPTS[build_config.build_variant_str].format(config=build_config)

    stream.write("""
cmake_minimum_required(VERSION 3.0)

project(python CXX)

include(ExternalProject)

ExternalProject_Add(
    {config.package_name}
    URL {source_tar}
    PREFIX {config.package_name}
    SOURCE_DIR build
    CONFIGURE_COMMAND env {configure_env} ./configure {configure_opts}
    BUILD_IN_SOURCE 1
    BUILD_COMMAND make -j{cpus}
    INSTALL_DIR {config.package_path}
)
""".format(
            config=build_config,
            source_tar=source_tar,
            configure_env=configure_env,
            configure_opts=configure_opts,
            cpus=multiprocessing.cpu_count(),
        )
    )

def _create_unversioned_python_symlink(build_config):
    python_link = os.path.join(build_config.package_path, "bin", "python")
    if not os.path.lexists(python_link):
        os.symlink("python{major}".format(major=self.package_version.split('.')[0]), python_link)

def _lock_payload(build_config):
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

if __name__ == "__main__":
    build()
