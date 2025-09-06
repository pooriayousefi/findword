cmake_minimum_required(VERSION 3.20)

# Modern testing framework
find_package(Python3 REQUIRED COMPONENTS Interpreter)

# Create test executable for unit tests
add_executable(test_findword test_findword.cpp)
target_link_libraries(test_findword PRIVATE)
set_target_properties(test_findword PROPERTIES
    CXX_STANDARD 23
    CXX_STANDARD_REQUIRED ON
)

# Add tests
add_test(NAME unit_tests COMMAND test_findword)
add_test(NAME python_integration 
         COMMAND ${Python3_EXECUTABLE} "${CMAKE_CURRENT_SOURCE_DIR}/test_integration.py"
         WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# Functional tests with different inputs
add_test(NAME test_basic_word 
         COMMAND findword "TEST"
         WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

add_test(NAME test_complex_word 
         COMMAND findword "LISTEN"
         WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# Set test properties
set_tests_properties(unit_tests PROPERTIES TIMEOUT 30)
set_tests_properties(python_integration PROPERTIES TIMEOUT 60)
set_tests_properties(test_basic_word PROPERTIES TIMEOUT 30)
set_tests_properties(test_complex_word PROPERTIES TIMEOUT 60)
