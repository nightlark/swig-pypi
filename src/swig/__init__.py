import os
import platform
import subprocess
import sys

DATA = os.path.join(os.path.dirname(__file__), 'data')

BIN_DIR = os.path.join(DATA, 'bin')

def _program(name, args):
    return subprocess.call([os.path.join(BIN_DIR, name)] + args)

def swig():
    raise SystemExit(_program('swig', sys.argv[1:]))

