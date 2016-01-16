import json
import numpy as np
import time
from data.clusterer import Clusterer
from data.lyric_formatter import get_word_map
from data.feature_matrix_calculator import convert_lyric_to_feature_set
from data.distance_calculator import distance

def answer(question):
    with open("data/json/lyric_dict.json", "r") as infile:
        lyric_dict = json.load(infile)

    clusterer = Clusterer()
    clusterer.generate_clusters()

    input_map = get_word_map(question)
    label = clusterer.predict([convert_lyric_to_feature_set(question, input_map)])[0]
    relevant_lyrics = clusterer.cluster_map[label]
    relevant_lyric_dict = {k:v for k, v in zip(relevant_lyrics, [lyric_dict[l] for l in relevant_lyrics])}

    dists = []

    now = time.time()

    for lyric in relevant_lyric_dict:
        dists.append({
            "lyric": lyric,
            "dist": distance(input_map, relevant_lyric_dict[lyric])
        })

    max_dist = float("-inf")
    the_lyric = None
    for dist_obj in dists:
        a_dist = dist_obj["dist"]
        if a_dist is not None and a_dist > max_dist:
            max_dist = a_dist
            the_lyric = dist_obj["lyric"]

    then = time.time()
    print(then-now)
    return the_lyric

# For testing.
if __name__ == "__main__":
    the_lyric = answer("What is my best friend's name")
    print("")
    print(the_lyric)
