import numpy as wnp
import nltk
from nltk.corpus import wordnet as wn

lyrics = [ ]

distance_matrix = np.zeros((len(lyrics), len(lyrics)))

def get_word_map(l):
    tokens = nltk.word_tokenize(l)
    tagged = nltk.pos_tag(tokens)
    
    # TODO() assign weights to each of these?
    # JJ: adjective or numeral, ordinal
    # JJR: adjective, comparative
    # JJS: adjective, superlative
    # NN: noun
    # NNS: noun, plural
    # RB: adverb
    # RBR: adverb, comparative
    # RBS: adverb, superlative
    # VB: verb, base
    # VBD: verb, past tense
    # VBG: verb, present participle
    # VBN: verb, past participle
    # VBP: verb, present tense, not 3rd person singular
    # VBZ: ^                        ^
    # other potential tags:
    #   CD: numeral, cardinal
    #   NNP: proper nouns
    #   MD: modal auxiliary (can, couldn't, will, would)
    #   PRP: pronoun, personal
    #   PRP$: pronoun, possessive
    #   UH: interjection
    tags = ["JJ", "JJR", "JJS", "NN", "NNS", "RB", "RBR", 
            "RBS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
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

# TODO: store in db
# add keywords to each lyric
lydict = {}
max_line_count = float("-inf")
for l in lyrics:
    lydict[l] = get_word_map(l)
    if lydict[l]["count"] > max_line_count:
        max_line_count = lydict[l]["count"]

# TODO: compute pairwise distances    
# for l1 in lyrics:
#     for l2 in lyrics:
#         if l1 != l2:
#             pass

dists = []

input_map = get_word_map("<QUESTION HERE>")

stupid_array = {
    "N": wn.NOUN,
    "R": wn.ADV,
    "V": wn.VERB,
    "J": wn.ADJ
}

max_count = float("-inf")
for lyric in lydict:
    dist = 0
    count = 0
    #print(lyric)
    for key in stupid_array: 
        for word1 in input_map[key]:
            best_dist = float("-inf")
            for word2 in lydict[lyric][key]:
                try:
                    a = wn.synsets(word1, pos=stupid_array[key])[0]
                    b = wn.synsets(word2, pos=stupid_array[key])[0]
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
        min_dist = norm_distl
        the_lyric = dist_obj["lyric"]

print("")
print(the_lyric)
