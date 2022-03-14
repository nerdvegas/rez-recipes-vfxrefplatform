# rez-recipes-vfxrefplatform

Recipes for building the VFX Reference Platform in rez

## Usage

To locally build all packages required by VFX Reference Platform CY2022
(for example):

```
]$ python ./buildall.py CY2022
```

To run this build script, you first need to install:
* Rez cli tools (see [install notes](https://github.com/nerdvegas/rez/blob/master/INSTALL.md));
* PyYAML (https://pypi.org/project/PyYAML)

When you run this `buildall.py` script, it builds the latest version of each
package as required by the specified target CY. It determines this from the list
of package requirements in the `recipes/vfx_reference_platform/CY*` package
definition.

To rebuild and override existing variants (by default, existing variants are
not rebuilt):

```
]$ python ./buildall.py CY2022 --overwrite
```

To add more requirements to the build (often used to target a specific package
version, where the reference platform allows a range, as shown here):

```
]$ python ./buildall.py CY2022 --extra ~python-3.9.10
```

## Configuration

There are several files that control aspects of the build that you need to be
aware of.

### Preflight

So called "preflight" scripts are system-specific scripts found in the `preflight`
folder. You need to execute the preflight for your platform/os BEFORE running
`buildall.py`. These scripts install system-level requirements.

### rezconfig.py

This is the standard rez configuration file, which controls many aspects of rez
behaviour. For example, it's here where you set `local_packages_path`, which
determines where on disk your built packages are installed to. You can provide
your own config via the buildall `--rezconfig` arg, and note that the standard
rezconfig.py is still sourced (your own config will merge/override it).

### conf.yaml

This file controls aspects of the build not included in `rezconfig.py`. See this
file for docstrings explaining each setting. You can provide your own config
via the buildall `--conf` arg, and note that the standard conf.yaml is still
sourced (your own config will merge/override it).
