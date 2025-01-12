from spotty.permutations import *

TEST_CASES = [
    # {
    #     "text": "This is easy man",
    #     "max_word_count_per_sentence": 2,
    #     "result": [
    #         [
    #             ["This is easy", "man"],
    #             ["This is", "easy man"],
    #             ["This is", "easy", "man"],
    #             ["This", "is easy man"],
    #             ["This", "is easy", "man"],
    #             ["This", "is", "easy man"],
    #             ["This", "is", "easy", "man"],
    #         ]
    #     ],
    # },
    # {
    #     "text": "This is a test string which should be very easy to split",
    #     "max_word_count_per_sentence": 2,
    # },
    {"text": "a " * 4, "max_word_count_per_sentence": 2},
]


def run_tests(test_cases):
    for test_case in test_cases:
        text = test_case["text"]
        max_word_count_per_sentence = test_case["max_word_count_per_sentence"]

        total_permutations = count_sentence_permutations(
            len(text.split()), max_word_count_per_sentence
        )
        print(f"Total permutations: {total_permutations}")
        sentence_results = generate_all_sentence_permutations(
            text, max_word_count_per_sentence
        )

        print(total_permutations, len(sentence_results[0]))

        print(sentence_results)


if __name__ == "__main__":
    run_tests(TEST_CASES)
