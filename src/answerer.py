import json
import numpy as np
import nltk
import data.lyric_formatter as lyric_formatter
from nltk.corpus import wordnet as wn

# hardcode for now.
INPUT = "What should I add to my curry"

with open("./data/json/lyric_dict.json", "r") as infile:
    lydict = json.load(infile)

dists = []

input_map = lyric_formatter.get_word_map(INPUT)

char_to_wordnet = {
    "N": wn.NOUN,
    "R": wn.ADV,
    "V": wn.VERB,
    "J": wn.ADJ
}

max_count = float("-inf")
for lyric in lydict:
    dist = 0
    count = 0
    for key in char_to_wordnet:
        for word1 in input_map[key]:
            best_dist = float("-inf")
            for word2 in lydict[lyric][key]:
                try:
                    a = wn.synsets(word1, pos=char_to_wordnet[key])[0]
                    b = wn.synsets(word2, pos=char_to_wordnet[key])[0]
                    #print(a, b)
                    #print(a.path_similarity(b))
                    value = a.path_similarity(b)
                    if value is None:
                        value = 0

                    d = value
                    if d > best_dist:
                        best_dist = d
                except IndexError:
                    continue
            if np.isfinite(best_dist):
                count += 1
                dist += best_dist

    if count == 0:
        dist = float("-inf")

    dists.append({
        "lyric": lyric,
        "dist": dist,
        "count": count
    })

    if count > max_count:
        max_count = count

min_dist = float("-inf")
the_lyric = None
for dist_obj in dists:
    if dist_obj["count"] == 0:
        continue

    norm_dist = dist_obj["dist"] / dist_obj["count"]
    print(dist_obj["lyric"])
    print(norm_dist)
    print("")
    if norm_dist is not None and norm_dist > min_dist:
        min_dist = norm_dist
        the_lyric = dist_obj["lyric"]

print("")
print(the_lyric)
