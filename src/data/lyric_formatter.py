import json
import nltk
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict

"""
Generates a lyric dictionary as well as a bag of words

Lyric Dictionary:
    Maps each lyric to a dictionary
    Each dictionary maps a word type (e.g. noun) to a list of words in the lyric of that word type

Bag of words:
    List of unique words in all the lyrics, to be used in our feature set
    Reduced dimensionality by:
        1. Removing common/stop words (NLTK does this in tokenization)
        2. Filtering out words that only appear 1 or 2 times
        3. 'Stemming': reducing words to their root, so as to reduce 'same' words in different forms
"""

DATA_FILE = "json/lyrics.json"

def get_word_map(l):
    """
    TODO() assign weights to each of these?
    JJ: adjective or numeral, ordinal
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

if __name__ == "__main__":
    with open(DATA_FILE, "r") as infile:
        lyrics = json.load(infile)["lyrics"]

    lydict = {}
    word_counter = defaultdict(int)
    bag_of_words = []
    stemmer = SnowballStemmer("english")
    count = 0
    for l in lyrics:
        print("{} of {}".format(count, len(lyrics)))
        word_map = get_word_map(l)

        words = []
        for arr in word_map.values():
            if isinstance(arr, list):
                words.extend(stemmer.stem(word) for word in arr)
        for word in words:
            word_counter[word] += 1
        filtered_words = [word for word in words if word_counter[word] > 1]
        bag_of_words.extend(filtered_words)
        word_map["words"] = filtered_words

        lydict[l] = word_map
        count += 1
    bag_of_words = list(set(bag_of_words))

    with open("json/lyric_dict.json", "w") as outfile:
        json.dump(lydict, outfile)

    with open("json/bag_of_words.json", "w") as outfile:
        json.dump(bag_of_words, outfile)
