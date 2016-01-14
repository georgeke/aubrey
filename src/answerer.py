import json
import numpy as np
import nltk
from nltk.corpus import wordnet as wn
import time

def get_word_map(l):
    """
    TODO() assign weights to each of these?
    JJ: adjective or numeral, ordinalResource 'tokenizers/punkt/english.pickle' not found.
    JJR: adjective, comparative
    JJS: adjective, superlative
    NN: noun
    NNS: noun, plural
    RB: adverb
    RBR: adverb, comparative
    RBS: adverb, superlative
    VB: verb, base
    VBD: verb, past tense
    VBG: verb, present participle
    VBN: verb, past participle
    VBP: verb, present tense, not 3rd person singular
    VBZ: ^                        ^
    other potential tags:
      CD: numeral, cardinal
      NNP: proper nouns
      MD: modal auxiliary (can, couldn't, will, would)
      PRP: pronoun, personal
      PRP$: pronoun, possessive
      UH: interjection
    """
    tags = ["JJ", "JJR", "JJS", "NN", "NNS", "RB", "RBR",
            "RBS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

    tokens = nltk.word_tokenize(l)
    tokens = list(set(tokens))
    tagged = nltk.pos_tag(tokens)

    word_dict = {
        "N": [],
        "R": [],
        "V": [],
        "J": []
    }
    count = 0
    for tup in tagged:
        for k in word_dict.keys():
            if tup[1][0] == k:
                count += 1
                word_dict[k].append(tup[0])
                break
    word_dict["count"] = count
    return word_dict

def distance(lyric_dict1, lyric_dict2):
    """
    Returns the distance between two lyrics
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
    return None

def answer(question):
    with open("./data/json/lyric_dict.json", "r") as infile:
        lydict = json.load(infile)

    dists = []

    input_map = get_word_map(question)
    print(input_map)

    now = time.time()

    max_count = float("-inf")
    for lyric in lydict:
        dists.append({
            "lyric": lyric,
            "dist": distance(input_map, lydict[lyric])
        })

    min_dist = float("-inf")
    the_lyric = None
    for dist_obj in dists:
        a_dist = dist_obj["dist"]
        if a_dist is not None and a_dist > min_dist:
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
