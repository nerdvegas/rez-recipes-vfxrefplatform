"""
Builds the VFX Reference Platform in rez.

Note that initial testing is on LINUX ONLY.
"""
from __future__ import print_function
import sys
import argparse
import subprocess

try:
    import yaml
    _yaml_imported = True
except ImportError:
    _yaml_imported = False


# conf.yaml contents
conf = {}


def validate_system():
    """Ensure system requirements to run this build script are met
    """
    try:
        subprocess.check_output(
            ["rez", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except OSError:
        print("Rez cli tools not found", file=sys.stderr)
        sys.exit(1)

    if not _yaml_imported:
        print("PyYAML not found", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Builds VFX Reference Platform in rez")

    validate_system()
