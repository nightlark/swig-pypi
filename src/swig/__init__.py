import os
import platform
import subprocess
import sys

DATA = os.path.join(os.path.dirname(__file__), 'data')

BIN_DIR = os.path.join(DATA, 'bin')
SWIG_SHARE_DIR = os.path.join(DATA, 'share/swig')
SWIG_LIB_ENV = os.environ
SWIG_LIB_ENV["SWIG_LIB"] = "blah"

def _program(name, args):
    return subprocess.call([os.path.join(BIN_DIR, name)] + args, env=SWIG_LIB_ENV)

def swig():
    raise SystemExit(_program('swig', sys.argv[1:]))


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
