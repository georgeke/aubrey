import json
import nltk
import numpy as np

"""
For one-time, general purpose function calls
"""

DATA_FILE = "json/lyrics.json"

def remove_duplicates(lyrics):
    lyrics = list(set(lyrics))

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
    with open(DATA_FILE, "r") as infile:
        lyrics = json.load(infile)["lyrics"]

    # Function calls here
    print_stats(lyrics)

    with open(DATA_FILE, "w") as outfile:
        json.dump({"lyrics": lyrics}, outfile)
