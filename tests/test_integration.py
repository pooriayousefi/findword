#!/usr/bin/env python3
"""
Integration tests for FindWord application
Modern Python testing with comprehensive validation
"""

import subprocess
import sys
import os
import json
from pathlib import Path
from typing import List, Dict, Any

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        
    def run_test(self, name: str, test_func):
        """Run a single test with error handling"""
        try:
            test_func()
            print(f"✓ {name} PASSED")
            self.passed += 1
        except Exception as e:
            print(f"✗ {name} FAILED: {e}")
            self.failed += 1
    
    def summary(self):
        """Print test summary and exit with appropriate code"""
        print(f"\nTest Summary:")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        
        if self.failed > 0:
            sys.exit(1)
        else:
            print("All tests passed! ✓")

class FindWordTester:
    def __init__(self, executable_path: str = "./findword"):
        self.executable = executable_path
        self.runner = TestRunner()
        
    def run_findword(self, word: str) -> tuple[str, str, int]:
        """Run findword and return stdout, stderr, returncode"""
        try:
            result = subprocess.run(
                [self.executable, word],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            raise Exception(f"Timeout running findword with '{word}'")
        except FileNotFoundError:
            raise Exception(f"Executable not found: {self.executable}")
    
    def test_basic_functionality(self):
        """Test basic word finding functionality"""
        stdout, stderr, code = self.run_findword("TEST")
        
        if code != 0:
            raise Exception(f"Non-zero exit code: {code}, stderr: {stderr}")
        
        # Should find at least the word TEST itself
        lines = stdout.strip().split('\n')
        words = [line.strip() for line in lines if line.strip()]
        
        if not words:
            raise Exception("No words found in output")
        
        if "TEST" not in words:
            raise Exception("Original word 'TEST' not found in output")
    
    def test_complex_word(self):
        """Test with a more complex word"""
        stdout, stderr, code = self.run_findword("LISTEN")
        
        if code != 0:
            raise Exception(f"Non-zero exit code: {code}, stderr: {stderr}")
        
        lines = stdout.strip().split('\n')
        words = [line.strip() for line in lines if line.strip()]
        
        expected_words = ["LISTEN", "SILENT"]
        found_expected = [word for word in expected_words if word in words]
        
        if len(found_expected) == 0:
            raise Exception(f"None of expected words {expected_words} found in output")
    
    def test_short_word(self):
        """Test with a short word"""
        stdout, stderr, code = self.run_findword("CAT")
        
        if code != 0:
            raise Exception(f"Non-zero exit code: {code}, stderr: {stderr}")
        
        lines = stdout.strip().split('\n')
        words = [line.strip() for line in lines if line.strip()]
        
        if "CAT" not in words:
            raise Exception("Original word 'CAT' not found in output")
    
    def test_error_handling(self):
        """Test error handling with no arguments"""
        try:
            result = subprocess.run([self.executable], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                raise Exception("Expected non-zero exit code with no arguments")
            
            if "Usage" not in result.stderr and "Usage" not in result.stdout:
                raise Exception("Expected usage message in error output")
                
        except subprocess.TimeoutExpired:
            raise Exception("Timeout running findword with no arguments")
    
    def test_python_environment(self):
        """Test that Python environment is properly set up"""
        try:
            import spellchecker
            # Test basic functionality of spellchecker
            spell = spellchecker.SpellChecker()
            test_words = ["hello", "world", "asdfghjkl"]
            valid_words = [word for word in test_words if word in spell]
            
            if len(valid_words) < 2:
                raise Exception("Spellchecker not working properly")
                
        except ImportError:
            raise Exception("pyspellchecker not installed or not accessible")
    
    def run_all_tests(self):
        """Run all integration tests"""
        print("Running FindWord Integration Tests")
        print("=" * 40)
        
        # Check if executable exists
        if not os.path.exists(self.executable):
            print(f"Executable not found: {self.executable}")
            print("Trying alternative locations...")
            
            # Try different possible locations
            alternatives = [
                "./build/default/bin/findword",
                "./build/release/bin/findword",
                "./build/debug/bin/findword",
                "../findword"
            ]
            
            for alt in alternatives:
                if os.path.exists(alt):
                    self.executable = alt
                    print(f"Found executable at: {alt}")
                    break
            else:
                print("No executable found. Please build the project first.")
                sys.exit(1)
        
        # Run tests
        self.runner.run_test("Python Environment", self.test_python_environment)
        self.runner.run_test("Basic Functionality", self.test_basic_functionality)
        self.runner.run_test("Complex Word", self.test_complex_word)
        self.runner.run_test("Short Word", self.test_short_word)
        self.runner.run_test("Error Handling", self.test_error_handling)
        
        self.runner.summary()

def main():
    """Main test runner"""
    tester = FindWordTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
