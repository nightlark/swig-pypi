import os
import sys
from distutils.text_file import TextFile
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
from skbuild import setup


class genericpy_bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        _bdist_wheel.finalize_options(self)
        self.root_is_pure = False

    def get_tag(self):
        python, abi, plat = _bdist_wheel.get_tag(self)
        python, abi = "py2.py3", "none"
        return python, abi, plat


cmdclass = {"bdist_wheel": genericpy_bdist_wheel}

setup(
    cmdclass=cmdclass,
    package_dir={"": "src"},
    packages=["swig"],
    cmake_install_dir="src/swig/data",
    url="http://www.swig.org/",
    download_url="http://www.swig.org/download.html",
    project_urls={
        "Source Code": "https://github.com/nightlark/swig-pypi",
        "Bug Tracker": "https://github.com/nightlark/swig-pypi/issues",
    },
    license="https://github.com/swig/swig/blob/master/LICENSE",
)
