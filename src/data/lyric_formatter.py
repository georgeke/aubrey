import json
import numpy as np
import nltk
from nltk.corpus import wordnet as wn

DATA_FILE = "json/lyrics_subset.json"

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

if __name__ == "__main__":
    with open(DATA_FILE, "r") as infile:
        lyrics = json.load(infile)["lyrics"]

    # add keywords to each lyric
    lydict = {}
    for l in lyrics:
        lydict[l] = get_word_map(l)

    with open("lyric_dict.json", "w") as outfile:
        json.dump(lydict, outfile)
