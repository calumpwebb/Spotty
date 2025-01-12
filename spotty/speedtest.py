import time
import matplotlib.pyplot as plt
import numpy as np
from colorama import Fore, Style, init
from spotty.permutations import (
    generate_sentence_permutations,
    generate_sentence_permutations_v2,
    generate_sentence_permutations_v3,
    count_sentence_permutations,
)

# Initialize colorama
init(autoreset=True)

# Constants
TRIALS_PER_TEST = 1  # Number of trials per configuration
SENTENCE_LENGTH_RANGE = range(2, 50)  # Sentence lengths to test
WORD_COUNT_RANGE = range(2, 10)  # Max word counts to test

# List of functions to test
TEST_FUNCTIONS = [
    ("generate_sentence_permutations", generate_sentence_permutations),
    ("generate_sentence_permutations_v2", generate_sentence_permutations_v2),
    ("generate_sentence_permutations_v3", generate_sentence_permutations_v3),
]


# Helper: Normalize results for comparison
def normalize_results(results):
    return sorted([sublist for sublist in results])


# Test function
def test_performance():
    results = []
    win_counts = {name: 0 for name, _ in TEST_FUNCTIONS}  # Track wins for each function
    total_times = {name: 0 for name, _ in TEST_FUNCTIONS}  # Track total runtime
    avg_times = {name: [] for name, _ in TEST_FUNCTIONS}  # Track average times per test

    for max_sentences in SENTENCE_LENGTH_RANGE:
        for max_word_count in WORD_COUNT_RANGE:
            input_sentence = "A " * max_sentences
            total_permutations = count_sentence_permutations(
                max_sentences, max_word_count
            )

            # Print test header
            print(
                f"\n{Fore.CYAN}{Style.BRIGHT}Starting Test: max_sentences={max_sentences}, max_word_count={max_word_count}{Style.RESET_ALL}"
            )
            print(
                f"{Fore.MAGENTA}Total permutations: {total_permutations}{Style.RESET_ALL}\n"
            )

            function_times = {}
            reference_result = None

            for function_name, function in TEST_FUNCTIONS:
                times = []

                for trial in range(TRIALS_PER_TEST):
                    print(
                        f"{Fore.YELLOW}  Trial {trial + 1} for {function_name}...{Style.RESET_ALL}"
                    )

                    # Measure runtime
                    start = time.time()
                    result = function(input_sentence.strip(), max_word_count)
                    end = time.time()
                    times.append(end - start)

                    # Validate results across functions
                    normalized_result = normalize_results(result)
                    if reference_result is None:
                        reference_result = normalized_result
                    else:
                        if normalized_result != reference_result:
                            raise ValueError(
                                f"{Fore.RED}Mismatch detected!{Style.RESET_ALL}\n"
                                f"Function {function_name} produced:\n{result}\n"
                                f"Expected (from reference):\n{reference_result}"
                            )

                avg_time = sum(times) / len(times)
                function_times[function_name] = avg_time
                total_times[function_name] += sum(times)  # Total time for all trials
                avg_times[function_name].append(
                    avg_time
                )  # Store average time for this test

                print(
                    f"{Fore.GREEN}{Style.BRIGHT}Results for {function_name}:{Style.RESET_ALL}"
                )
                print(f"  {Fore.BLUE}Avg time: {avg_time:.4f}s\n")

            # Identify the fastest function for this test
            fastest_time = min(function_times.values())
            for function_name, avg_time in function_times.items():
                if avg_time == fastest_time:
                    win_counts[function_name] += 1

            results.append(
                {
                    "max_sentences": max_sentences,
                    "max_word_count": max_word_count,
                    "total_permutations": total_permutations,
                    "function_times": function_times,
                }
            )

            print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")

    return results, win_counts, total_times, avg_times


# Visualization Function
def visualize_results(win_counts, total_times, avg_times):
    function_names = list(win_counts.keys())

    # Compute metrics
    total_runtimes = [total_times[fn] for fn in function_names]
    avg_of_averages = [np.mean(avg_times[fn]) for fn in function_names]
    total_wins = [win_counts[fn] for fn in function_names]

    # Plot Total Wins
    plt.figure(figsize=(8, 6))
    plt.bar(function_names, total_wins, color=["#4caf50", "#2196f3"])
    plt.title("Total Wins by Function")
    plt.ylabel("Number of Wins")
    plt.xlabel("Function")
    plt.show()

    # Plot Total Runtime
    plt.figure(figsize=(8, 6))
    plt.bar(function_names, total_runtimes, color=["#4caf50", "#2196f3"])
    plt.title("Total Runtime by Function")
    plt.ylabel("Total Time (s)")
    plt.xlabel("Function")
    plt.show()


# Run tests and log results
if __name__ == "__main__":
    results, win_counts, total_times, avg_times = test_performance()

    visualize_results(win_counts, total_times, avg_times)

    # Print a summary of all tests
    print(f"\n{Fore.GREEN}{Style.BRIGHT}Summary of Tests:{Style.RESET_ALL}")
    for fn_name, _ in TEST_FUNCTIONS:  # Extract only the function name
        print(f"{Fore.CYAN}{fn_name}:")
        print(f"  Total Wins: {win_counts[fn_name]}")
        print(f"  Total Time: {total_times[fn_name]:.4f}s")
        print(f"  Avg of Averages: {np.mean(avg_times[fn_name]):.4f}s")
