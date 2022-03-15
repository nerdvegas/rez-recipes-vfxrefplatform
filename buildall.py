"""
Builds the VFX Reference Platform in rez.

Note that initial testing is on LINUX ONLY.
"""
from __future__ import print_function
import os
import os.path
import sys
import argparse
import subprocess

try:
    import yaml
    _yaml_imported = True
except ImportError:
    _yaml_imported = False


# consts
RECIPES_DIR = "recipes"

# globals
opts = None
conf = {}
pipe_if_not_verbose = None


def load_conf():
    global conf

    for filepath in ("conf.yaml", opts.conf):
        if filepath:
            with open(filepath) as f:
                conf.update(yaml.load(f.read()))


def run_cmd(args, **kwargs):
    environ = os.environ.copy()
    environ.update(conf.get("environ") or {})
    environ.update(kwargs.get("env") or {})

    # set REZ_CONFIG_FILE to pickup relevant rezconfig.py files
    rezconfigs = []
    for filepath in ("rezconfig.py", opts.rezconfig):
        if filepath:
            rezconfigs.append(os.path.abspath(filepath))

    environ["REZ_CONFIG_FILE"] = os.pathsep.join(rezconfigs)

    # disable user rezconfig, for reproducability
    environ["REZ_DISABLE_HOME_CONFIG"] = "1"

    kwargs["env"] = environ

    proc = subprocess.Popen(args, **kwargs)
    out, _ = proc.communicate()

    if proc.returncode:
        raise RuntimeError("Command failed with exitcode %d" % proc.returncode)

    return out


def check_system_requirements():
    """Ensure system requirements to run this build script are met
    """
    try:
        run_cmd(
            ["rez", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except RuntimeError:
        print("Rez cli tools not found", file=sys.stderr)
        sys.exit(1)

    if not _yaml_imported:
        print("PyYAML not found", file=sys.stderr)
        sys.exit(1)


def build_vfx_refs():
    """Build and install all the CY* platform ref versions

    Note that these are a kind of stub package that don't actually build anything,
    they just contain a list of weak requirements that match the ref platform
    spec for that year. We always build them because we need them to determine
    what versions of other packages to build.
    """
    path = os.path.join(RECIPES_DIR, "vfx_reference_platform")

    for name in os.listdir(path):
        print("Building vfx_reference_platform-%s..." % name)
        run_cmd(
            ["rez", "build", "-i"],
            cwd=os.path.join(path, name),
            stdout=pipe_if_not_verbose
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Builds VFX Reference Platform in rez")

    parser.add_argument(
        "--conf",
        help="conf.yaml settings"
    )
    parser.add_argument(
        "--rezconfig",
        help="rezconfig.py settings"
    )
    parser.add_argument(
        "-v", "--verbose", action='count', default=0,
        help="verbosity"
    )

    opts = parser.parse_args()

    if not opts.verbose:
        pipe_if_not_verbose = subprocess.PIPE

    load_conf()
    check_system_requirements()
    build_vfx_refs()
