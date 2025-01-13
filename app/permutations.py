import re


def generate_all_sentence_permutations(text, max_word_count_per_sentence):
    print(f"Checking text\n   {text}\n")

    # Regex to split on . ! ? followed by whitespace or end of string
    sentence_endings = r"(?<=[.!?])\s+"

    sentences = re.split(sentence_endings, text)

    # Regex to remove . ! ? from a sentence
    sentences = [re.sub(r"[.!?]", "", sentence) for sentence in sentences]

    results = []

    for sentence in sentences:
        print(f'Checking sentence "{sentence}"')
        sentence_result = generate_sentence_permutations(
            sentence, max_word_count_per_sentence
        )

        results.append(sentence_result)

    return results


def count_sentence_permutations(word_count, max_word_count):
    print(
        f"Counting permutations for {word_count} word(s) w/ max_word_count={max_word_count}"
    )
    # DP array to store number of permutations for 0 to n words
    dp = [0] * (word_count + 1)
    dp[0] = 1  # Base case: 1 way to partition 0 words

    for i in range(1, word_count + 1):
        for j in range(1, min(max_word_count, i) + 1):
            dp[i] += dp[i - j]

    return dp[word_count]


def generate_sentence_permutations_v3(sentence, max_word_count):
    words = sentence.split()
    total_number_of_words = len(words)

    # DP table where dp[i] stores all groupings starting at index i
    dp = [[] for _ in range(total_number_of_words + 1)]
    dp[total_number_of_words] = [[]]  # Base case: empty grouping at the end

    # Fill DP table backwards
    for start in range(total_number_of_words - 1, -1, -1):
        local_result = []
        # Generate groupings for all valid end indices
        for end in range(
            start + 1, min(start + max_word_count + 1, total_number_of_words + 1)
        ):
            # Current group: words[start:end]
            current_group = " ".join(words[start:end])
            # Combine with all groupings from dp[end]
            for suffix in dp[end]:
                local_result.append([current_group] + suffix)
        dp[start] = local_result

    return dp[0]


def generate_sentence_permutations_v2(sentence, max_word_count):
    words = sentence.split()
    total_number_of_words = len(words)
    memo = {}

    def backtrack(start):
        # Return memoized result if available
        if start in memo:
            return memo[start]

        # Base case: If we've reached the end, return an empty grouping
        if start == total_number_of_words:
            return [[]]

        local_result = []
        for end in range(
            start + 1, min(start + max_word_count + 1, total_number_of_words + 1)
        ):
            next_group = " ".join(words[start:end])
            # Recursively get permutations for the remaining words
            for suffix in backtrack(end):
                local_result.append([next_group] + suffix)

        # Memoize and return
        memo[start] = local_result
        return local_result

    return backtrack(0)


def generate_sentence_permutations(sentence, max_word_count):
    words = sentence.split()
    total_number_of_words = len(words)
    result = []

    stack = [(0, [])]

    while stack:
        start, current_group = stack.pop()

        # If we've reached the end of the sentence, add the current grouping to the result
        if start == total_number_of_words:
            result.append(current_group)
            continue

        # Iterate over all possible lengths of the next group, but limit to max_concat_words
        for end in range(
            start + 1, min(start + max_word_count + 1, total_number_of_words + 1)
        ):
            # Create the next group by joining words from start to end
            next_group = " ".join(words[start:end])
            # Push the new state into the stack
            stack.append((end, current_group + [next_group]))

    return result