cmake_minimum_required(VERSION 3.6)

project(SwigPythonDistributions NONE)

set(default_build_type "Release")
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(
    STATUS
      "Setting build type to '${default_build_type}' as none was specified.")
  set(CMAKE_BUILD_TYPE
      "${default_build_type}"
      CACHE STRING "Choose the type of build." FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release"
                                               "MinSizeRel" "RelWithDebInfo")
endif()

enable_language(CXX)
include(ExternalProject)

set(_swig_cache_args)

function(tmp_ExternalProject_add_Empty prj deps)
  set(deps_args)
  if(NOT deps STREQUAL "")
    set(deps_args DEPENDS ${deps})
  endif()
  ExternalProject_Add(
    ${prj}
    SOURCE_DIR ${CMAKE_BINARY_DIR}/${prj}
    DOWNLOAD_COMMAND ""
    UPDATE_COMMAND ""
    CONFIGURE_COMMAND ""
    BUILD_COMMAND ""
    BUILD_IN_SOURCE 1
    INSTALL_COMMAND "" ${deps_args})
endfunction()

# PCRE
set(PCRE_SOURCE_DIR ${CMAKE_BINARY_DIR}/PCRE-src)
set(PCRE_BINARY_DIR ${CMAKE_BINARY_DIR}/PCRE-build)
set(PCRE_INSTALL_DIR ${CMAKE_BINARY_DIR}/PCRE-install)

ExternalProject_Add(
  PCRE
  SOURCE_DIR ${PCRE_SOURCE_DIR}
  BINARY_DIR ${PCRE_BINARY_DIR}
  URL "https://ftp.pcre.org/pub/pcre/pcre-8.45.tar.gz"
  URL_HASH
    "SHA256=4e6ce03e0336e8b4a3d6c2b70b1c5e18590a5673a98186da90d4f33c23defc09"
  CMAKE_CACHE_ARGS
    -DCMAKE_BUILD_TYPE:STRING=${default_build_type}
    -DCMAKE_INSTALL_PREFIX:PATH=${PCRE_INSTALL_DIR}
    -DCMAKE_INSTALL_LIBDIR:STRING=lib
  INSTALL_DIR ${PCRE_INSTALL_DIR})
list(
  APPEND
  _swig_cache_args
  -DPCRE_LIBRARY:FILEPATH=${PCRE_INSTALL_DIR}/lib/${CMAKE_STATIC_LIBRARY_PREFIX}pcre${CMAKE_STATIC_LIBRARY_SUFFIX}
  -DPCRE_INCLUDE_DIR:PATH=${PCRE_INSTALL_DIR}/include)

# Bison
find_package(BISON)
if(NOT BISON_FOUND)
  set(BISON_SOURCE_DIR ${CMAKE_BINARY_DIR}/BISON-bin-src)
  set(BISON_BINARY_DIR ${CMAKE_BINARY_DIR}/BISON-bin-build)
  set(BISON_INSTALL_DIR ${CMAKE_BINARY_DIR}/BISON-bin-install)
  set(BISON_BINARY_DIST_DIR ${CMAKE_BINARY_DIR}/BISON-bin-dist)
  set(BISON_BINARY_DIST_ARCH_DIR ${CMAKE_BINARY_DIR}/BISON-bin-dist-arch)
  if(WIN32)
    # Easiest to just download a precompiled binary
    # ExternalProject_add(BISON-bin SOURCE_DIR ${BISON_SOURCE_DIR} BINARY_DIR
    # ${BISON_BINARY_DIR} URL
    # "https://github.com/lexxmark/winflexbison/archive/v2.5.24.tar.gz" URL_HASH
    # "SHA256=a49d6e310636e3487e1e066e411d908cfeae2d5b5fde1f3cf74fe1d6d4301062"
    # CMAKE_CACHE_ARGS -DCMAKE_INSTALL_PREFIX:PATH=${BISON_INSTALL_DIR}
    # INSTALL_DIR ${BISON_INSTALL_DIR} )
    ExternalProject_Add(
      BISON-bin
      SOURCE_DIR ${BISON_BINARY_DIST_DIR}
      URL "https://github.com/lexxmark/winflexbison/releases/download/v2.5.24/win_flex_bison-2.5.24.zip"
      URL_HASH
        "SHA256=39c6086ce211d5415500acc5ed2d8939861ca1696aee48909c7f6daf5122b505"
      DOWNLOAD_DIR ${BISON_SOURCE_DIR}
      CONFIGURE_COMMAND ""
      BUILD_COMMAND ""
      BUILD_IN_SOURCE 1
      INSTALL_COMMAND "")
    list(
      APPEND
      _swig_cache_args
      -DBISON_EXECUTABLE:FILEPATH=${BISON_BINARY_DIST_DIR}/win_bison${CMAKE_EXECUTABLE_SUFFIX}
    )
  else()
    # Build from source on platforms that could reasonably already have
    # autotools installed
    ExternalProject_Add(
      BISON-bin
      SOURCE_DIR ${BISON_SOURCE_DIR}
      URL "https://ftp.gnu.org/gnu/bison/bison-3.7.tar.gz"
      URL_HASH
        "SHA256=492ad61202de893ca21a99b621d63fa5389da58804ad79d3f226b8d04b803998"
      CONFIGURE_COMMAND ${BISON_SOURCE_DIR}/configure
                        --prefix=${BISON_INSTALL_DIR}
      BUILD_COMMAND make
      BUILD_IN_SOURCE 1
      INSTALL_COMMAND make install
      INSTALL_DIR ${BISON_INSTALL_DIR})
    list(
      APPEND
      _swig_cache_args
      -DBISON_EXECUTABLE:FILEPATH=${BISON_INSTALL_DIR}/bin/bison${CMAKE_EXECUTABLE_SUFFIX}
    )
  endif()
else()
  tmp_externalproject_add_empty(BISON-bin "")
endif()

# SWIG
set(SWIG_SOURCE_DIR ${CMAKE_BINARY_DIR}/SWIG-src)
set(SWIG_BINARY_DIR ${CMAKE_BINARY_DIR}/SWIG-build)
ExternalProject_Add(
  SWIG
  SOURCE_DIR ${SWIG_SOURCE_DIR}
  BINARY_DIR ${SWIG_BINARY_DIR}
  URL "https://github.com/swig/swig/archive/master.tar.gz"
  CMAKE_CACHE_ARGS
    -DBUILD_TESTING:BOOL=OFF -DCMAKE_INSTALL_PREFIX:PATH=${CMAKE_INSTALL_PREFIX}
    -DCMAKE_C_FLAGS:STRING=-DPCRE_STATIC -DCMAKE_CXX_FLAGS:STRING=-DPCRE_STATIC
    ${_swig_cache_args}
  INSTALL_COMMAND ""
  DEPENDS PCRE BISON-bin)

install(SCRIPT ${SWIG_BINARY_DIR}/cmake_install.cmake)
