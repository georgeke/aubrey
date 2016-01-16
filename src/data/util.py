import json
import time
import nltk
import numpy as np
from lyric_formatter import save_lyric_dict_and_bag_of_words
from feature_matrix_calculator import save_feature_matrix
from clusterer import Clusterer

"""
For one-time, general purpose function calls
"""

DATA_FILE = "json/lyrics.json"

def _remove_duplicates(lyrics):
    lyrics = list(set(lyrics))

def _time(func):
    now = time.time()
    func()
    then = time.time()
    return then - now

def clean_and_save_lyrics():
    with open(DATA_FILE, "r") as infile:
        lyrics = json.load(infile)

    _remove_duplicates(lyrics)

    with open(DATA_FILE, "w") as outfile:
        json.dump(lyrics, outfile)

def run_full_pipeline():
    print("Generating lyric_dict and bag of words took {.2f}s".format(_time(save_lyric_dict_and_bag_of_words)))
    print("Generating feature matrix took {.2f}s".format(_time(save_feature_matrix)))
    clusterer = new Clusterer()
    print("Clustering took {.2f}s".format(_time(clusterer.generate_clusters)))

def print_stats(lyrics):
    with open("json/bag_of_words.json", "r") as infile:
        bag_of_words = json.load(infile)

    lengths = [len(l.split(" ")) for l in lyrics]
    max_l = np.max(lengths)
    print("Number of lyrics: {}".format(len(lyrics)))
    print("Average lyric length: {} words".format(np.mean(lengths)))
    print("Lyric length range: [{}, {}]".format(np.min(lengths), max_l))
    print("Longest lyric: {}".format([l for l in lyrics if len(l.split(" ")) >= max_l][0]))
    print("Recommended # of clusters: {}".format(int(len(lyrics) / 500)))
    print("Number of unique words: {}".format(len(bag_of_words)))

if __name__ == "__main__":
    print_stats(lyrics)
