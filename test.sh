#!/bin/bash

# Test script for FindWord application
# This script tests basic functionality and validates outputs

set -e  # Exit on any error

echo "==================================="
echo "FindWord Application Test Suite"
echo "==================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test results
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test
run_test() {
    local test_name="$1"
    local input_word="$2"
    local expected_words="$3"
    
    echo -e "${YELLOW}Running test: $test_name${NC}"
    echo "Input word: $input_word"
    
    # Run findword and capture output
    if output=$(./findword "$input_word" 2>&1); then
        echo "Output:"
        echo "$output"
        
        # Check if expected words are in output
        local all_found=true
        for word in $expected_words; do
            if echo "$output" | grep -q "$word"; then
                echo -e "${GREEN}✓ Found expected word: $word${NC}"
            else
                echo -e "${RED}✗ Missing expected word: $word${NC}"
                all_found=false
            fi
        done
        
        if $all_found; then
            echo -e "${GREEN}✓ Test PASSED: $test_name${NC}"
            ((TESTS_PASSED++))
        else
            echo -e "${RED}✗ Test FAILED: $test_name${NC}"
            ((TESTS_FAILED++))
        fi
    else
        echo -e "${RED}✗ Test FAILED: $test_name (execution error)${NC}"
        echo "Error output: $output"
        ((TESTS_FAILED++))
    fi
    
    echo ""
}

# Check if executable exists
if [ ! -f "./findword" ]; then
    echo -e "${RED}Error: findword executable not found${NC}"
    echo "Please run 'make' to build the application first"
    exit 1
fi

# Check if Python environment is set up
if [ ! -d "env" ]; then
    echo -e "${YELLOW}Python environment not found. Setting up...${NC}"
    make setup-python
fi

# Activate Python environment
source env/bin/activate

echo "Starting tests..."
echo ""

# Test 1: Basic functionality with "TEST"
run_test "Basic Test" "TEST" "TEST"

# Test 2: Common word "LISTEN"
run_test "Listen Test" "LISTEN" "LISTEN SILENT ENLIST"

# Test 3: Short word "CAT"
run_test "Cat Test" "CAT" "CAT"

# Test 4: Complex word "EARTH"
run_test "Earth Test" "EARTH" "EARTH HEART"

# Test 5: Error handling - empty argument
echo -e "${YELLOW}Testing error handling...${NC}"
if ./findword 2>&1 | grep -q "Usage"; then
    echo -e "${GREEN}✓ Error handling test PASSED${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ Error handling test FAILED${NC}"
    ((TESTS_FAILED++))
fi

echo ""
echo "==================================="
echo "Test Results Summary"
echo "==================================="
echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
echo "Total tests: $((TESTS_PASSED + TESTS_FAILED))"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed! ✓${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed! ✗${NC}"
    exit 1
fi
