import os
import sys
from distutils.text_file import TextFile
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
from skbuild import setup

# may be needed in some cases for versioneer to get version correctly during builds
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import versioneer  # noqa: E402


class genericpy_bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        _bdist_wheel.finalize_options(self)
        self.root_is_pure = False

    def get_tag(self):
        python, abi, plat = _bdist_wheel.get_tag(self)
        python, abi = "py2.py3", "none"
        return python, abi, plat


with open("README.md", "r") as fp:
    readme = fp.read()

cmdclass = {"bdist_wheel": genericpy_bdist_wheel}
for k, v in versioneer.get_cmdclass().items():
    cmdclass[k] = v

setup(
    name="swig",
    version=versioneer.get_version(),
    cmdclass=cmdclass,
    package_dir={"": "src"},
    packages=["swig"],
    cmake_install_dir="src/swig/data",
    entry_points={"console_scripts": ["swig=swig:swig"]},
    url="http://www.swig.org/",
    download_url="http://www.swig.org/download.html",
    description="SWIG is a software development tool that connects "
    "programs written in C and C++ with a variety of "
    "high-level programming languages.",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "License :: Other/Proprietary License",
        "Programming Language :: C",
        "Programming Language :: C++",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
    ],
    license="pick a license",
    keywords="swig build c c++",
)
