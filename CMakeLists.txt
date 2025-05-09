cmake_minimum_required(VERSION 3.15)

project(SwigPythonDistributions NONE)

set(default_build_type "Release")
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(STATUS "Setting build type to '${default_build_type}' as none was specified.")
  set(CMAKE_BUILD_TYPE "${default_build_type}" CACHE
      STRING "Choose the type of build." FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS
    "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

enable_language(CXX)
include(ExternalProject)

include(swig_version.cmake)

set(_swig_cache_args)
set(_swig_build_flags)

if(WIN32)
  set(_swig_build_flags "${_swig_build_flags} -static -static-libgcc -static-libstdc++")
  if (SWIG VERSION_LESS 4.1.0)
    # Building with Makefiles on Windows using MSYS is a royal pain
    # Makefiles were trying to run using the git bash copy of sh.exe, but
    # of course, those failed to run due to a SPACE in the path name
    # because "Program Files"...
    set(WIN_USE_PREBUILT ON)
  endif()
endif()



function(tmp_ExternalProject_add_Empty prj deps)
  set(deps_args)
  if(NOT deps STREQUAL "")
    set(deps_args DEPENDS ${deps})
  endif()
  ExternalProject_add(${prj}
    SOURCE_DIR ${CMAKE_BINARY_DIR}/${prj}
    DOWNLOAD_COMMAND ""
    UPDATE_COMMAND ""
    CONFIGURE_COMMAND ""
    BUILD_COMMAND ""
    BUILD_IN_SOURCE 1
    INSTALL_COMMAND ""
    ${deps_args}
    )
endfunction()

# PCRE2
set(PCRE2_SOURCE_DIR ${CMAKE_BINARY_DIR}/PCRE2-src)
set(PCRE2_BINARY_DIR ${CMAKE_BINARY_DIR}/PCRE2-build)
set(PCRE2_INSTALL_DIR ${CMAKE_BINARY_DIR}/PCRE2-install)

# PCRE
set(PCRE_SOURCE_DIR ${CMAKE_BINARY_DIR}/PCRE-src)
set(PCRE_BINARY_DIR ${CMAKE_BINARY_DIR}/PCRE-build)
set(PCRE_INSTALL_DIR ${CMAKE_BINARY_DIR}/PCRE-install)

if(NOT WIN_USE_PREBUILT)
  if(NOT SWIG_VERSION VERSION_LESS 4.1.0)
    ExternalProject_add(PCRE2
      SOURCE_DIR ${PCRE2_SOURCE_DIR}
      BINARY_DIR ${PCRE2_BINARY_DIR}
      INSTALL_DIR ${PCRE2_INSTALL_DIR}
      URL "https://github.com/PCRE2Project/pcre2/releases/download/pcre2-10.40/pcre2-10.40.zip"
      URL_HASH "SHA256=b6ee01732f0e41296e60a00ce37fbed1c4955ae7e7625b1fd29a55605c9493b4"
      CMAKE_CACHE_ARGS
        -DCMAKE_BUILD_TYPE:STRING=${default_build_type}
        -DCMAKE_INSTALL_PREFIX:PATH=<INSTALL_DIR>
        -DCMAKE_INSTALL_LIBDIR:STRING=lib
	-DCMAKE_C_STANDARD:STRING=99
        "-DCMAKE_OSX_ARCHITECTURES:STRING=${CMAKE_OSX_ARCHITECTURES}"
      )
    list(APPEND _swig_cache_args
        -DPCRE2_LIBRARY:FILEPATH=${PCRE2_INSTALL_DIR}/lib/${CMAKE_STATIC_LIBRARY_PREFIX}pcre2-8${CMAKE_STATIC_LIBRARY_SUFFIX}
        -DPCRE2_INCLUDE_DIR:PATH=${PCRE2_INSTALL_DIR}/include
      )
  else()
    ExternalProject_add(PCRE
      SOURCE_DIR ${PCRE_SOURCE_DIR}
      BINARY_DIR ${PCRE_BINARY_DIR}
      INSTALL_DIR ${PCRE_INSTALL_DIR}
      URL "https://prdownloads.sourceforge.net/pcre/pcre-8.45.tar.gz"
      URL_HASH "SHA256=4e6ce03e0336e8b4a3d6c2b70b1c5e18590a5673a98186da90d4f33c23defc09"
      CMAKE_CACHE_ARGS
        -DCMAKE_BUILD_TYPE:STRING=${default_build_type}
        -DCMAKE_INSTALL_PREFIX:PATH=<INSTALL_DIR>
        -DCMAKE_INSTALL_LIBDIR:STRING=lib
        "-DCMAKE_OSX_ARCHITECTURES:STRING=${CMAKE_OSX_ARCHITECTURES}"
      )
    list(APPEND _swig_cache_args
        -DPCRE_LIBRARY:FILEPATH=${PCRE_INSTALL_DIR}/lib/${CMAKE_STATIC_LIBRARY_PREFIX}pcre${CMAKE_STATIC_LIBRARY_SUFFIX}
        -DPCRE_INCLUDE_DIR:PATH=${PCRE_INSTALL_DIR}/include
      )
  endif()
endif()

# Bison
find_package(BISON 3.5)
if(NOT BISON_FOUND AND NOT WIN_USE_PREBUILT)
  set(BISON_SOURCE_DIR ${CMAKE_BINARY_DIR}/BISON-bin-src)
  set(BISON_BINARY_DIR ${CMAKE_BINARY_DIR}/BISON-bin-build)
  set(BISON_INSTALL_DIR ${CMAKE_BINARY_DIR}/BISON-bin-install)
  set(BISON_BINARY_DIST_DIR ${CMAKE_BINARY_DIR}/BISON-bin-dist)
  set(BISON_BINARY_DIST_ARCH_DIR ${CMAKE_BINARY_DIR}/BISON-bin-dist-arch)
  if(WIN32)
    # Easiest to just download a precompiled binary
#    ExternalProject_add(BISON-bin
#      SOURCE_DIR ${BISON_SOURCE_DIR}
#      BINARY_DIR ${BISON_BINARY_DIR}
#      URL "https://github.com/lexxmark/winflexbison/archive/v2.5.24.tar.gz"
#      URL_HASH "SHA256=a49d6e310636e3487e1e066e411d908cfeae2d5b5fde1f3cf74fe1d6d4301062"
#      CMAKE_CACHE_ARGS
#        -DCMAKE_INSTALL_PREFIX:PATH=${BISON_INSTALL_DIR}
#      INSTALL_DIR ${BISON_INSTALL_DIR}
#      )
    ExternalProject_add(BISON-bin
      SOURCE_DIR ${BISON_BINARY_DIST_DIR}
      URL "https://github.com/lexxmark/winflexbison/releases/download/v2.5.24/win_flex_bison-2.5.24.zip"
      URL_HASH "SHA256=39c6086ce211d5415500acc5ed2d8939861ca1696aee48909c7f6daf5122b505"
      DOWNLOAD_DIR ${BISON_SOURCE_DIR}
      CONFIGURE_COMMAND ""
      BUILD_COMMAND ""
      BUILD_IN_SOURCE 1
      INSTALL_COMMAND ""
      )
    list(APPEND _swig_cache_args
      -DBISON_EXECUTABLE:FILEPATH=${BISON_BINARY_DIST_DIR}/win_bison${CMAKE_EXECUTABLE_SUFFIX}
      )
  else()
    # Build from source on platforms that could reasonably already have autotools installed
    ExternalProject_add(BISON-bin
      SOURCE_DIR ${BISON_SOURCE_DIR}
      INSTALL_DIR ${BISON_INSTALL_DIR}
      URL "https://ftp.gnu.org/gnu/bison/bison-3.8.2.tar.gz"
      URL_HASH "SHA256=06c9e13bdf7eb24d4ceb6b59205a4f67c2c7e7213119644430fe82fbd14a0abb"
      CONFIGURE_COMMAND <SOURCE_DIR>/configure --prefix=<INSTALL_DIR>
      BUILD_COMMAND make
      BUILD_IN_SOURCE 1
      INSTALL_COMMAND make install
      )
    list(APPEND _swig_cache_args
      -DBISON_EXECUTABLE:FILEPATH=${BISON_INSTALL_DIR}/bin/bison${CMAKE_EXECUTABLE_SUFFIX}
      )
  endif()
else()
  tmp_ExternalProject_add_Empty(BISON-bin "")
endif()

# SWIG
set(SWIG_SOURCE_DIR ${CMAKE_BINARY_DIR}/SWIG-src)
set(SWIG_BINARY_DIR ${CMAKE_BINARY_DIR}/SWIG-build)

if(NOT WIN_USE_PREBUILT)
  if(NOT SWIG_VERSION VERSION_LESS 4.1.0)
    ExternalProject_add(SWIG
      SOURCE_DIR ${SWIG_SOURCE_DIR}
      BINARY_DIR ${SWIG_BINARY_DIR}
      URL "https://github.com/swig/swig/archive/refs/tags/v${SWIG_VERSION}.tar.gz"
      #URL "https://github.com/swig/swig/archive/master.tar.gz"
      CMAKE_CACHE_ARGS
        -DBUILD_TESTING:BOOL=OFF
        -DCMAKE_CXX_STANDARD_REQUIRED:BOOL=ON
        -DCMAKE_CXX_STANDARD:STRING=11
        -DCMAKE_C_STANDARD_REQUIRED:BOOL=ON
        -DCMAKE_C_STANDARD:STRING=99
        -DCMAKE_INSTALL_PREFIX:PATH=${CMAKE_INSTALL_PREFIX}
        "-DCMAKE_C_FLAGS:STRING=${_swig_build_flags}"
        "-DCMAKE_CXX_FLAGS:STRING=${_swig_build_flags}"
        "-DCMAKE_OSX_ARCHITECTURES:STRING=${CMAKE_OSX_ARCHITECTURES}"
        ${_swig_cache_args}
      INSTALL_COMMAND ""
      DEPENDS
        PCRE2
        BISON-bin
      )
    install(SCRIPT ${SWIG_BINARY_DIR}/cmake_install.cmake)
  else()
    set(SWIG_INSTALL_DIR ${CMAKE_BINARY_DIR}/SWIG-install)
    ExternalProject_add(SWIG
      SOURCE_DIR ${SWIG_SOURCE_DIR}
      INSTALL_DIR ${SWIG_INSTALL_DIR}
      URL "https://prdownloads.sourceforge.net/swig/swig-${SWIG_VERSION}.tar.gz"
      CONFIGURE_COMMAND ${CMAKE_COMMAND} -E env PCRE_CONFIG=${PCRE_INSTALL_DIR}/bin/pcre-config ${MSYSTEM} ${MSYS_CMD} ${MSYS_SHELL} ${WIN_MSYS_HERE} <SOURCE_DIR>/configure --prefix=
      BUILD_COMMAND make -j
      BUILD_IN_SOURCE ON
      INSTALL_COMMAND make -j install DESTDIR=<INSTALL_DIR>
      DEPENDS
        PCRE
        BISON-bin
      )
    install(PROGRAMS ${SWIG_INSTALL_DIR}/bin/ DESTINATION bin)
    install(FILES ${SWIG_INSTALL_DIR}/share/ DESTINATION share)
  endif()
else(NOT WIN_USE_PREBUILT)
  # building on Windows with MinGW from Makefiles is a pain -- simply get precompiled Windows binaries instead
  set(SWIG_INSTALL_DIR ${CMAKE_BINARY_DIR}/SWIG-install)
  ExternalProject_add(SWIG
    SOURCE_DIR ${SWIG_INSTALL_DIR}
    URL "https://prdownloads.sourceforge.net/swig/swigwin-${SWIG_VERSION}.zip"
    CONFIGURE_COMMAND ""
    BUILD_COMMAND ""
    INSTALL_COMMAND ""
    )
  install(PROGRAMS ${SWIG_INSTALL_DIR}/swig.exe DESTINATION bin)
  install(FILES ${SWIG_INSTALL_DIR}/Lib/ DESTINATION share/swig/${SWIG_VERSION})
endif()
