import json
import numpy as np
from sklearn.cluster import KMeans
from collections import defaultdict

class Clusterer():
    CLUSTER_SIZE = 500

    def __init__(self):
        with open("json/feature_matrix.json", "r") as infile:
            self._feature_matrix = json.load(infile)

        with open("json/lyrics.json", "r") as infile:
            self._lyrics = json.load(infile)

    @property
    def cluster_map(self):
        return self._cluster_map

    def generate_clusters(self):
        self._model = KMeans(n_clusters=int(len(self._lyrics) / self.CLUSTER_SIZE))
        self._model.fit(self._feature_matrix)

        self._cluster_map = defaultdict(list)
        for cluster_label, lyric in zip(self._model.labels_, self._lyrics):
            self._cluster_map[cluster_label].append(lyric)

    def predict(self, X):
        return self._model.predict(X)
