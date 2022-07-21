SWIG Python Distributions
=========================

[![PyPI](https://img.shields.io/pypi/v/swig.svg)](https://pypi.org/project/swig)

A project that packages SWIG as a Python package, enabling `swig` to be installed from PyPI:

```sh
pip install swig
```

or used as part of `build-system.requires` in a pyproject.toml file:

```toml
[build-system]
requires = ["swig"]
```

PyPI package versions will follow the `major.minor.patch` version numbers of SWIG releases.

Binary wheels for Windows, macOS, and Linux for most CPU architectures supported on PyPI are provided. ARM wheels for Raspberry Pi available at https://www.piwheels.org/project/swig/.

[SWIG PyPI Package Homepage](https://github.com/nightlark/swig-pypi)

[SWIG Homepage](http://www.swig.org/)

[SWIG Source Code](https://github.com/swig/swig/)

[SWIG License](https://github.com/swig/swig/blob/master/LICENSE): GPL-3.0-or-later with portions under [LICENSE-UNIVERSITIES](https://github.com/nightlark/swig-pypi/blob/main/LICENSE-UNIVERSITIES) (see [LICENSE-SWIG](https://github.com/nightlark/swig-pypi/blob/main/LICENSE-SWIG) for details)

Installing SWIG
===============

SWIG can be installed by pip with:

```sh
pip install swig
```

or:

```sh
python -m pip install swig
```

Building from the source dist package requires internet access in order to download a copy of the SWIG source code.

Using with pipx
===============

Using `pipx run swig <args>` will run SWIG without any install step, as long as the machine has pipx installed (which includes GitHub Actions runners).

Using with pyproject.toml
=========================

SWIG can be added to the `build-system.requires` key in a pyproject.toml file for building Python extensions that use SWIG to generate bindings.

```toml
[build-system]
requires = ["swig"]
```

License
=======

The code for this project is covered by the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0). Source distributions do not include a copy of the SWIG source code or binaries. Binary wheels are covered by the SWIG license (GPLv3), due to their inclusion of a compiled SWIG binary and library files.

SWIG is distributed under the [GNU General Public License v3 or later](https://github.com/swig/swig/blob/master/LICENSE) with portions under the file [LICENSE-UNIVERSITIES](https://github.com/swig/swig/blob/master/LICENSE-UNIVERSITIES). For more information about SWIG, visit [http://www.swig.org](http://www.swig.org/)
