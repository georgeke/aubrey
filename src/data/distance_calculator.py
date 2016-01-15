import json
import numpy as np
import nltk
from nltk.corpus import wordnet as wn

def distance(lyric_dict1, lyric_dict2):
    """
    Returns the distance between two lyrics, the greater the magnitude, the 'closer' the lyrics are
    1. Calculate the path_similarity value for each pair of tokens (that have the same part of speech)
       between lyric1 and lyric2
    2. Sum them up and divide the number of pairings that added to that sum to normalize for lengths of lyrics
       (i.e. a long lyric with a large sum should have a similar distance to a shorter lyric with a smaller sum.
        This is to balance quality of matches with quantity of matches)
    """
    CHAR_TO_WORDNET = {
        "N": wn.NOUN,
        "R": wn.ADV,
        "V": wn.VERB,
        "J": wn.ADJ
    }

    dist = 0
    count = 0
    for key in CHAR_TO_WORDNET:
        for word1 in lyric_dict1[key]:
            best_dist = float("-inf")
            for word2 in lyric_dict2[key]:
                try:
                    a = wn.synsets(word1, pos=CHAR_TO_WORDNET[key])[0]
                    b = wn.synsets(word2, pos=CHAR_TO_WORDNET[key])[0]
                    # Maximum returned by path_similarity is 1 (same words)
                    value = a.path_similarity(b)
                    if value is None:
                        value = 0

                    if value > best_dist:
                        best_dist = value
                except IndexError:
                    continue
            if np.isfinite(best_dist):
                count += 1
                dist += best_dist

    if count == 0:
        dist = float("-inf")

    if np.isfinite(dist) and count > 0:
        return dist / count
    return 0

if __name__ == "__main__":
    with open("json/lyric_dict.json", "r") as infile:
        lydict = json.load(infile)

    distance_matrix = np.zeros((len(lydict), len(lydict)))

    for y,dict_y in enumerate(lydict.values()):
        for x, dict_x in enumerate(lydict.values()):
            if y != x:
                distance_matrix[y][x] = distance(dict_y, dict_x)

    with open("json/distance_matrix.json", "w") as outfile:
        json.dump(distance_matrix.tolist(), outfile)
