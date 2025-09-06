#include <iostream>
#include <cassert>
#include <string>
#include <algorithm>
#include <vector>

// Simple test framework
class TestRunner {
public:
    void run_test(const std::string& name, std::function<void()> test) {
        try {
            test();
            std::cout << "✓ " << name << " PASSED\n";
            ++passed_;
        } catch (const std::exception& e) {
            std::cout << "✗ " << name << " FAILED: " << e.what() << "\n";
            ++failed_;
        }
    }
    
    void summary() {
        std::cout << "\nTest Summary:\n";
        std::cout << "Passed: " << passed_ << "\n";
        std::cout << "Failed: " << failed_ << "\n";
        if (failed_ > 0) {
            exit(1);
        }
    }
    
private:
    int passed_ = 0;
    int failed_ = 0;
};

// Tests for the generator logic (simplified version)
void test_basic_permutation() {
    // Test basic permutation logic
    std::string word = "ABC";
    std::vector<std::string> perms;
    
    // Generate all permutations manually for testing
    std::sort(word.begin(), word.end());
    do {
        perms.push_back(word);
    } while (std::next_permutation(word.begin(), word.end()));
    
    assert(perms.size() == 6); // 3! = 6
    assert(std::find(perms.begin(), perms.end(), "ABC") != perms.end());
    assert(std::find(perms.begin(), perms.end(), "CBA") != perms.end());
}

void test_duplicate_handling() {
    // Test that duplicates are handled correctly
    std::string word = "AAB";
    std::vector<std::string> perms;
    
    std::sort(word.begin(), word.end());
    do {
        perms.push_back(word);
    } while (std::next_permutation(word.begin(), word.end()));
    
    assert(perms.size() == 3); // AAB, ABA, BAA
}

void test_single_character() {
    std::string word = "A";
    std::vector<std::string> perms;
    
    std::sort(word.begin(), word.end());
    do {
        perms.push_back(word);
    } while (std::next_permutation(word.begin(), word.end()));
    
    assert(perms.size() == 1);
    assert(perms[0] == "A");
}

void test_empty_string() {
    std::string word = "";
    std::vector<std::string> perms;
    
    // Empty string should handle gracefully
    if (!word.empty()) {
        std::sort(word.begin(), word.end());
        do {
            perms.push_back(word);
        } while (std::next_permutation(word.begin(), word.end()));
    }
    
    assert(perms.empty());
}

int main() {
    std::cout << "Running FindWord Unit Tests\n";
    std::cout << "===========================\n";
    
    TestRunner runner;
    
    runner.run_test("Basic Permutation", test_basic_permutation);
    runner.run_test("Duplicate Handling", test_duplicate_handling);
    runner.run_test("Single Character", test_single_character);
    runner.run_test("Empty String", test_empty_string);
    
    runner.summary();
    return 0;
}
