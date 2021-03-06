import json
import numpy as np
import time
from nltk.corpus import wordnet as wn
from data.clusterer import Clusterer
from data.lyric_formatter import get_word_map
from data.feature_matrix_calculator import convert_lyric_to_feature_set

class Answerer():
    def __init__(self):
        with open("data/json/lyric_dict.json", "r") as infile:
            self.lyric_dict = json.load(infile )

        with open("data/json/bag_of_words.json", "r") as infile:
            self.bag_of_words = json.load(infile)

        self.clusterer = Clusterer("data")
        self.clusterer.generate_clusters()

    def distance(self, lyric_dict1, lyric_dict2):
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
        return None

    def answer(self, question):
        input_map = get_word_map(question)
        label = self.clusterer.predict([convert_lyric_to_feature_set(question, input_map, self.bag_of_words)])[0]
        relevant_lyrics = self.clusterer.cluster_map[label]
        relevant_lyric_dict = {k:v for k, v in zip(relevant_lyrics, [self.lyric_dict[l] for l in relevant_lyrics])}

        dists = []

        now = time.time()

        for lyric in relevant_lyric_dict:
            dists.append({
                "lyric": lyric,
                "dist": self.distance(input_map, relevant_lyric_dict[lyric])
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
    answerer = Answerer()
    the_lyric = answerer.answer("What is my best friend's name")
    print("")
    print(the_lyric)
