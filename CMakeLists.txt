cmake_minimum_required(VERSION 3.20)
project(FindWord 
    VERSION 1.0.0 
    DESCRIPTION "High-performance word permutation generator with C++20 coroutines"
    HOMEPAGE_URL "https://github.com/pooriayousefi/findword"
    LANGUAGES CXX)

# Set C++23 standard for modern features
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Enable modern CMake policies
cmake_policy(SET CMP0077 NEW)
cmake_policy(SET CMP0091 NEW)

# Use modern build configurations
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

# Set default build type to Release if not specified
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    message(STATUS "Setting build type to 'Release' as none was specified.")
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

# Enable IPO/LTO for Release builds if supported
include(CheckIPOSupported)
check_ipo_supported(RESULT ipo_supported OUTPUT ipo_error)
if(ipo_supported AND CMAKE_BUILD_TYPE STREQUAL "Release")
    message(STATUS "IPO/LTO enabled for Release build")
    set(CMAKE_INTERPROCEDURAL_OPTIMIZATION TRUE)
endif()

# Compiler-specific options with modern standards
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(findword PRIVATE
        $<$<CONFIG:Debug>:-g -O0 -Wall -Wextra -Wpedantic -Wshadow -Wnon-virtual-dtor -Woverloaded-virtual>
        $<$<CONFIG:Release>:-O3 -DNDEBUG -march=native>
    )
    # Enable sanitizers for debug builds
    if(CMAKE_BUILD_TYPE STREQUAL "Debug")
        target_compile_options(findword PRIVATE -fsanitize=address,undefined)
        target_link_options(findword PRIVATE -fsanitize=address,undefined)
    endif()
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    target_compile_options(findword PRIVATE
        $<$<CONFIG:Debug>:/Zi /Od /W4 /permissive->
        $<$<CONFIG:Release>:/O2 /DNDEBUG /GL>
    )
    if(CMAKE_BUILD_TYPE STREQUAL "Release")
        target_link_options(findword PRIVATE /LTCG)
    endif()
endif()

# Modern dependency management with vcpkg support
find_package(Python3 REQUIRED COMPONENTS Interpreter)

# Create modern executable target
add_executable(findword)
target_sources(findword PRIVATE findword.cpp)

# Use modern target properties
set_target_properties(findword PROPERTIES
    CXX_STANDARD 23
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
    DEBUG_POSTFIX "_debug"
)

# Modern packaging and installation
install(TARGETS findword
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    COMPONENT Runtime
)

install(FILES findword.py
    DESTINATION ${CMAKE_INSTALL_BINDIR}
    PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE
                GROUP_READ GROUP_EXECUTE
                WORLD_READ WORLD_EXECUTE
    COMPONENT Runtime
)

install(FILES README.md LICENSE
    DESTINATION ${CMAKE_INSTALL_DOCDIR}
    COMPONENT Documentation
)

# Create requirements.txt for modern Python package management
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/requirements.txt.in" 
               "${CMAKE_CURRENT_BINARY_DIR}/requirements.txt" @ONLY)

install(FILES "${CMAKE_CURRENT_BINARY_DIR}/requirements.txt"
    DESTINATION ${CMAKE_INSTALL_DOCDIR}
    COMPONENT Documentation
)

# Modern CPack configuration for cross-platform packaging
set(CPACK_PACKAGE_NAME "FindWord")
set(CPACK_PACKAGE_VENDOR "Pooria Yousefi")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "High-performance word permutation generator")
set(CPACK_PACKAGE_VERSION ${PROJECT_VERSION})
set(CPACK_PACKAGE_INSTALL_DIRECTORY ${CPACK_PACKAGE_NAME})
set(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}/LICENSE")
set(CPACK_RESOURCE_FILE_README "${CMAKE_CURRENT_SOURCE_DIR}/README.md")

# Platform-specific packaging
if(WIN32)
    set(CPACK_GENERATOR "WIX;ZIP")
    set(CPACK_WIX_UPGRADE_GUID "12345678-1234-1234-1234-123456789012")
elseif(APPLE)
    set(CPACK_GENERATOR "DragNDrop;TGZ")
else()
    set(CPACK_GENERATOR "DEB;RPM;TGZ")
    set(CPACK_DEBIAN_PACKAGE_MAINTAINER "Pooria Yousefi")
    set(CPACK_RPM_PACKAGE_LICENSE "MIT")
endif()

include(CPack)

# Modern development tools integration
option(BUILD_TESTING "Build tests" ON)
if(BUILD_TESTING)
    enable_testing()
    add_subdirectory(tests)
endif()

# Development environment setup
add_custom_target(setup-dev
    COMMAND ${Python3_EXECUTABLE} -m venv venv
    COMMAND ${CMAKE_COMMAND} -E chdir venv 
            $<IF:$<PLATFORM_ID:Windows>,Scripts/python,bin/python> -m pip install -r "${CMAKE_CURRENT_BINARY_DIR}/requirements.txt"
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Setting up development environment"
)

# Configuration summary
message(STATUS "FindWord Configuration Summary:")
message(STATUS "  Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "  C++ standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "  Compiler: ${CMAKE_CXX_COMPILER_ID} ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "  Python: ${Python3_EXECUTABLE}")
message(STATUS "  Install prefix: ${CMAKE_INSTALL_PREFIX}")
if(ipo_supported AND CMAKE_BUILD_TYPE STREQUAL "Release")
    message(STATUS "  IPO/LTO: Enabled")
endif()
