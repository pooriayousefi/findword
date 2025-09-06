cmake_minimum_required(VERSION 3.20)
project(findword
    VERSION 1.0.0
    DESCRIPTION "Modern C++ application"
    HOMEPAGE_URL "https://github.com/pooriayousefi/findword"
    LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Include standard modules
include(GNUInstallDirs)

# Set default build type
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    message(STATUS "Setting build type to 'Release' as none was specified.")
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

# Create the executable
add_executable(findword findword.cpp)

# Set target properties
set_target_properties(findword PROPERTIES
    CXX_STANDARD 20
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
    DEBUG_POSTFIX "_debug"
)

# Platform-specific settings
if(WIN32)
    target_compile_definitions(findword PRIVATE _WIN32_WINNT=0x0601)
elseif(APPLE)
    target_compile_definitions(findword PRIVATE __APPLE__)
else()
    target_compile_definitions(findword PRIVATE __linux__)
endif()

# Compiler-specific options for cross-platform support
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(findword PRIVATE
        $<$<CONFIG:Debug>:-g -O0 -Wall -Wextra -Wpedantic -Wshadow>
        $<$<CONFIG:Release>:-O3 -DNDEBUG>
    )
    if(CMAKE_BUILD_TYPE STREQUAL "Debug")
        target_compile_options(findword PRIVATE -fsanitize=address,undefined)
        target_link_options(findword PRIVATE -fsanitize=address,undefined)
    endif()
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    target_compile_options(findword PRIVATE
        $<$<CONFIG:Debug>:/Zi /Od /W4 /permissive->
        $<$<CONFIG:Release>:/O2 /DNDEBUG>
    )
endif()

# Installation
install(TARGETS findword
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    COMPONENT Runtime
)

install(FILES README.md
    DESTINATION ${CMAKE_INSTALL_DOCDIR}
    COMPONENT Documentation
    OPTIONAL
)

# Configuration summary
message(STATUS "findword Configuration Summary:")
message(STATUS "  Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "  C++ standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "  Compiler: ${CMAKE_CXX_COMPILER_ID} ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "  Platform: ${CMAKE_SYSTEM_NAME}")
