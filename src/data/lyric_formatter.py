import json
import numpy as np
import nltk
from nltk.corpus import wordnet as wn
import sys
sys.path.append("..")
import answerer

DATA_FILE = "json/lyrics_subset.json"

if __name__ == "__main__":
    with open(DATA_FILE, "r") as infile:
        lyrics = json.load(infile)["lyrics"]

    # add keywords to each lyric
    lydict = {}
    count = 0
    for l in lyrics:
        print("{} of {}".format(count, len(lyrics)))
        lydict[l] = answerer.get_word_map(l)
        count += 1

    with open("json/lyric_dict.json", "w") as outfile:
        json.dump(lydict, outfile)
