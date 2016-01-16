import json
import numpy as np
from collections import defaultdict

"""
Generates a feature matrix for all lyrics, with each feature value being the number of times
a word in the bag of words appears in a given lyric.

Each row is a lyric, in the order they are stored in JSON, and each column is a word from the
bag of words, ordered as they are in the JSON file.
"""

if __name__ == "__main__":
    with open("json/bag_of_words.json", "r") as infile:
        bag_of_words = json.load(infile)

    with open("json/lyric_dict.json", "r") as infile:
        lyric_dict = json.load(infile)

    feature_matrix = np.zeros((len(lyric_dict), len(bag_of_words)))

    for (row, (lyric, its_dict)) in enumerate(lyric_dict.items()):
        word_counts = defaultdict(int)
        for word in its_dict["words"]:
            word_counts[word] += 1
        for col, word_from_bag in enumerate(bag_of_words):
            if word_counts[word_from_bag] > 0:
                feature_matrix[row][col] = word_counts[word_from_bag]

    with open("json/feature_matrix.json", "w") as outfile:
        json.dump(feature_matrix.tolist(), outfile)
