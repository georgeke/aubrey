# Aubrey

Ask any question, and have it answered with a relevant Drake lyric.

#### How it works
We use a combination of clustering and natural language processing to determine the lyric that the most related to an inputted question.
  1. Using the [NLTK](http://www.nltk.org/) python library, all lyrics are tokenized based on the [WordNet corpus](http://www.nltk.org/howto/wordnet.html), and then tagged for their part of speech. 
  2. We also build up a list of unique tokens (bag of words) for all of Drake's lyrics. 
  3. Each lyric is converted from their tokenized form into a feature vector, with each being the number of occurences of a word in the bag of words in the lyric. For example of bag_of_words = ["dog", "tree", "poop"] and the lyric is "A dog eat dog tree.", then the resulting vector would be [2, 1, 0].
  4. Combining the vectors of each lyric gives us a sparse matrix that can be passed into a clustering algorithm such as [KMeans](http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html). This will split our lyrics into a group of X clusters, with each cluster having lyrics that are 'similar'. Judging whether the clustering went well is difficult, and leaves room for exploration in both the clustering algorithm and the tweaking of the algorithm itself.
  5. Now, when a user asks a question, we take that question and let the clustering model predict which cluster it should fit in.
  6. We then compare each lyric in the cluster to the question, and find the one with the closest match. This is done using pairwise comparisons between each corresponding token between the question and a lyric. Only tokens with the same part of speech are considered. The pairwise comparison is judged using the synset in WordNet.

#### Challenges
  1. The comparison between a question and a lyric can take a long time, as pairwise calculation of similarity between two tokens can be slow at time. We tried to mitigate this by clustering lyrics into smaller groups, so that there are fewer lyrics to compare to. Further improvement can still be made, as some questions can still take up to 30s to answer.
  2. Using a bag of words technique for representing lyrics may not be a good way to cluster lyrics. Words that are synonyms are not considered, and this may end up splitting up similar lyrics into different clusters. Having 'washy' clusters could prevent a question from matching with a super relevant lyric. Work can still be put into a smarter way to represent sentences that takes into consideration synonym graphs.
  3. The bag of words originally had many similar words that were considered different because of varying inflections of tenses. This made the dimensionality very high and clustering was slowed down. To reduce dimensionallity, 3 techniques were used:
    1. [Stemming](https://en.wikipedia.org/wiki/Stemming): reducing a word to its root/base form, so that words like ran and running will be treated as the same token.
    2. Filtering out rare words: there were plenty of rare words that appeared only once in all of Drake's lyrics.
    3. Removing common/stop words (e.g. to, a, the, etc.). Luckily, WordNet accounts for stopwords during tokenization.
  4. The lyrics themselves needed cleaning up in some areas. For example, there were a lot of verbs contracted to drop their last g, such as "runnin'" or "cookin" (notice some have and some do not have the trailing apostrophe). This was cleaned up with some regex. Another example is varying unicode characters for the same meaning (e.g. U+0027 vs U+2019 for an apostrophe). Most of these issues were cleared with search and replace and some good ol' manual labour. There are still other lingering nuances, such as trailing punctuation (e.g. lyrics ending in commas), and Lyrics That Capitilize Every Letter In The Line.

Started at [CalHacks 2.0](http://www.calhacks.io/)
