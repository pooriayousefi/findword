
#include <iostream>
#include <fstream>
#include <string>
#include <string_view>
#include <stdexcept>
#include <exception>
#include <ranges>
#include <coroutine>
#include <valarray>
#include <algorithm>
#include <chrono>
#include <thread>
#include <unordered_set>

namespace
{
	// resumable generator data structure
	template<class T> struct generator
	{
		struct promise_type
		{
			T current_value;
			constexpr decltype(auto) initial_suspend() { return std::suspend_always{}; }
			constexpr decltype(auto) final_suspend() noexcept { return std::suspend_always{}; }
			constexpr decltype(auto) get_return_object() { return generator{ std::coroutine_handle<promise_type>::from_promise(*this) }; }
			constexpr decltype(auto) return_void() { return std::suspend_never{}; }
			constexpr decltype(auto) yield_value(T value) noexcept { current_value = std::move(value); return std::suspend_always{}; }
			inline void unhandled_exception() { std::terminate(); }
		};
		struct sentinel {};
		struct iterator
		{
			using iterator_category = std::input_iterator_tag;
			using value_type = T;
			using difference_type = ptrdiff_t;
			using pointer = T*;
			using reference = T&;
			using const_reference = const T&;
			std::coroutine_handle<promise_type> handle;
			explicit iterator(std::coroutine_handle<promise_type>& h) :handle{ h } {}
			constexpr iterator& operator++()
			{
				handle.resume();
				return *this;
			}
			constexpr void operator++(int) { (void)operator++(); }
			constexpr reference operator*() { return handle.promise().current_value; }
			constexpr pointer operator->() { return std::addressof(operator*()); }
			constexpr const_reference operator*() const { return handle.promise().current_value; }
			constexpr pointer operator->() const { return std::addressof(operator*()); }
			constexpr bool operator==(sentinel) { return handle.done(); }
			constexpr bool operator==(sentinel) const { return handle.done(); }
		};
		std::coroutine_handle<promise_type> handle;
		explicit generator(std::coroutine_handle<promise_type> h) :handle{ h } {}
		~generator() { if (handle) handle.destroy(); }
		generator(const generator&) = delete;
		generator(generator&& other) noexcept :handle(other.handle) { other.handle = nullptr; }
		generator& operator=(const generator&) = delete;
		generator& operator=(generator&& other) noexcept { handle = other.handle; other.handle = nullptr; return *this; }
		constexpr T get_value() { return handle.promise().current_value; }
		constexpr bool next() { handle.resume(); return !handle.done(); }
		constexpr bool resume() { handle.resume(); return !handle.done(); }
		constexpr decltype(auto) begin()
		{
			handle.resume();
			return iterator{ handle };
		}
		constexpr decltype(auto) end() { return sentinel{}; }
	};
}

int main(int argc, char* argv[])
{
	auto wordfinder = [](std::string_view word) -> generator<std::string>
	{
		const auto SIZE = word.size();
		std::valarray<size_t> indices(size_t(0), SIZE);
		for (auto i : std::ranges::views::iota(size_t(0), SIZE))
			indices[i] = i;
		auto index_to_iterator = [&](size_t i) { return std::ranges::next(word.begin(), i); };
		do
		{
			for (auto i : std::ranges::views::iota(size_t(2), SIZE))
			{
				std::string permutated_word{};
				permutated_word.reserve(SIZE);
				for (auto j : std::ranges::views::iota(size_t(0), i))
					permutated_word.push_back(*index_to_iterator(indices[j]));
				co_yield permutated_word;
			}
			std::string last_permutated_word{};
			for (auto& idx : indices)
				last_permutated_word.push_back(*index_to_iterator(idx));
			co_yield last_permutated_word;
	    } while (std::next_permutation(std::ranges::begin(indices), std::ranges::end(indices)));
    };
	std::ofstream ofile{};
	try
	{
		if (argc != 2)
			throw std::runtime_error("Usage: findword <word>");
		else
		{
			ofile.open("permutated_words.txt", std::ios_base::out | std::ios_base::trunc);
			if (!ofile.is_open())
				throw std::runtime_error("Error opening file");

			std::string word{ argv[1] };
			std::string_view word_view{ word };
			std::unordered_set<std::string> permutated_words{};

			auto ti = std::chrono::high_resolution_clock::now();
			auto findwords = wordfinder(word_view);
			for (auto& permutated_word : findwords)
				permutated_words.emplace(permutated_word);
			auto tf = std::chrono::high_resolution_clock::now();
			auto permutation_runtime = std::chrono::duration<double>(tf - ti).count();
			// std::cout
			// 	<< "\nPermutation runtime: " << permutation_runtime << " seconds"
			// 	<< "\nNumber of permutated words are: " << permutated_words.size()
			// 	<< std::endl;

			for (auto& permutated_word : permutated_words)
				ofile << permutated_word << '\n';

			ofile.flush();
			ofile.close();

			auto syserr = system("python findword.py");
			if (syserr != 0)
				throw std::runtime_error("Error in Python virtual environment activation and running script");
		}		
		return 0;
	}
	catch (const std::exception& xxx)
	{
		std::cerr << xxx.what() << std::endl;
		if (ofile.is_open())
			ofile.close();
		std::this_thread::sleep_for(std::chrono::seconds(3));
		return 1;
	}
}