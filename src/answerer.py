import json
import numpy as np
import time
import data.lyric_formatter as lyric_formatter

def answer(question):
    with open("data/"+lyric_formatter.OUT_FILE, "r") as infile:
        lydict = json.load(infile)

    dists = []

    input_map = lyric_formatter.get_word_map(question)

    now = time.time()

    for lyric in lydict:
        dists.append({
            "lyric": lyric,
            "dist": 1#distance_calculator.distance(input_map, lydict[lyric])
        })

    min_dist = float("inf")
    the_lyric = None
    for dist_obj in dists:
        a_dist = dist_obj["dist"]
        if a_dist is not None and a_dist < min_dist:
            min_dist = a_dist
            the_lyric = dist_obj["lyric"]

    then = time.time()
    print(then-now)
    return the_lyric

# For testing.
if __name__ == "__main__":
    the_lyric = answer("What should I eat for dinner?")
    print("")
    print(the_lyric)
