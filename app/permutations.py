import logging
import string

logger = logging.getLogger(__name__)


def generate_word_permutations(sentence, max_words=4):
    """
    Generates permutations of the words in `sentence`, grouping
    up to `max_words` words at a time. Returns a list of lists.
    """
    logger.info(f"Generating word permutations... (max_words={max_words})")

    # Remove punctuation except apostrophes
    translator = str.maketrans("", "", string.punctuation.replace("'", ""))
    sentence = sentence.translate(translator)

    words = sentence.split()
    n = len(words)
    results = []

    def helper(start_idx, current_combination):
        if start_idx == n:
            results.append(current_combination)
            return
        for end in range(start_idx + 1, min(start_idx + max_words + 1, n + 1)):
            group = " ".join(words[start_idx:end])
            helper(end, current_combination + [group])

    helper(0, [])
    logger.info(f"Finished generating {len(results):,} permutations. Sorting now...")

    # Sort so that longer permutations come first
    results.sort(key=lambda x: -len(x))
    return results
