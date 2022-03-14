
name = "vfx_reference_platform"

version = "CY2022"

description = (
    "Set of tool and library versions to be used as a common target platform "
    "for building software for the VFX industry"
)

help = "https://vfxplatform.com/"

uuid = "rez_vfx_reference_platform.vfx_reference_platform.CY2022"

requires = [
    "~python-3.9.1+<3.10",
    "~qt-5.15",
    "~pyqt-5.15",
    "~pyside-5.15",
    "~numpy-1.20",
    "~openexr-3.1",
    "~ptex-2.4",
    "~opensubdiv-3.4",
    "~openvdb-9",
    "~alembic-1.8",
    "~fbx-2020",
    "~ocio-2.1",
    "~aces-1.3",
    "~boost-1.76",
    "~tbb-2020.update3",
    "~mkl-2020",
    # TODO compiler support? We should allow for both cases, one where compiler
    # is system provided and one where it's a rez package
]

build_command = False
