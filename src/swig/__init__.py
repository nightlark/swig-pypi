import os
import platform
import subprocess
import sys
import glob
from ._version import __version__, __version_tuple__

DATA = os.path.join(os.path.dirname(__file__), "data")

BIN_DIR = os.path.join(DATA, "bin")
SWIG_SHARE_DIR = os.path.join(DATA, "share" + os.path.sep + "swig")

# should only be one swig_lib version in the data subfolder
# make nicer if swig adds support for custom SWIG_LIB paths or relative swig_lib paths
SWIG_LIB_ENV = os.environ
SWIG_LIB_ENV["SWIG_LIB"] = glob.glob(SWIG_SHARE_DIR + os.path.sep + "*")[0]


def _program(name, args):
    return subprocess.call([os.path.join(BIN_DIR, name)] + args, env=SWIG_LIB_ENV)


def swig():
    raise SystemExit(_program("swig", sys.argv[1:]))
