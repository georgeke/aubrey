import json
import numpy as np
from collections import defaultdict

"""
Generates a feature matrix for all lyrics, with each feature value being the number of times
a word in the bag of words appears in a given lyric.

Each row is a lyric, in the order they are stored in JSON, and each column is a word from the
bag of words, ordered as they are in the JSON file.
"""

def convert_lyric_to_feature_set(lyric, its_dict, bag_of_words):
    arr = [0] * len(bag_of_words)
    word_counts = defaultdict(int)
    for word in its_dict["words"]:
        word_counts[word] += 1
    for col, word_from_bag in enumerate(bag_of_words):
        if word_counts[word_from_bag] > 0:
            arr[col] = word_counts[word_from_bag]
    return arr

def save_feature_matrix():
    with open("json/bag_of_words.json", "r") as infile:
        bag_of_words = json.load(infile)

    with open("json/lyric_dict.json", "r") as infile:
        lyric_dict = json.load(infile)

    feature_matrix = [[]] * len(lyric_dict)

    for (row, (lyric, its_dict)) in enumerate(lyric_dict.items()):
        feature_matrix[row] = convert_lyric_to_feature_set(lyric, its_dict, bag_of_words)

    with open("json/feature_matrix.json", "w") as outfile:
        json.dump(feature_matrix, outfile)

if __name__ == "__main__":
    save_feature_matrix()
