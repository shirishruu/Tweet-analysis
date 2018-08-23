from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn import decomposition
from sklearn.decomposition import NMF
import numpy as np  # a conventional alias
import glob
import os
import string
import nltk
from sklearn.metrics.pairwise import euclidean_distances, cosine_similarity
from scipy.cluster.hierarchy import ward, dendrogram
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
import scipy.stats as stats

names=[]
corpus=[]


co = PlaintextCorpusReader("./election",".*\.txt")

for fileids in co.fileids():
    names.append(fileids)
    corpus.append(co.raw(fileids))

print len(names), 'documents in the corpus'
print names[:30]


for idx in range(len(corpus)-1, -1, -1):
    print
    print names[idx]
    print corpus[idx][:70].replace('\n', ' ')



vectorizer = TfidfVectorizer(stop_words='english', min_df=2)
dtm = vectorizer.fit_transform(corpus)
print dtm.shape
vocab = vectorizer.get_feature_names() # list of unique vocab, we will use this later
print len(vocab), '# of unique words'
print vocab[-10:]
print vocab[:10]

print 'num of documents, num of unique words'


num_topics = 50

clf = NMF(n_components=num_topics)
doctopic = clf.fit_transform(dtm)
print num_topics, clf.reconstruction_err_

topic_words = []
num_top_words = 5
for topic in clf.components_:
    #print topic.shape, topic[:5]
    word_idx = np.argsort(topic)[::-1][0:num_top_words] # get indexes with highest weights
    #print 'top indexes', word_idx
    topic_words.append([vocab[i] for i in word_idx])
    #print topic_words[-1]
    #print

print '__lol__' * 10    
    
    
for t in range(len(topic_words)):
    print "Topic {}: {}".format(t, ' '.join(topic_words[t][:15]))