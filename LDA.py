from __future__ import division, print_function
from gensim import corpora, models, similarities, matutils
import re
import nltk
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import logging


names=[]
docs=[]


co = PlaintextCorpusReader("./election",".*\.txt")


logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO

for fileids in co.fileids():
    names.append(fileids)
    docs.append(co.words(fileids))

#print(len(names), 'documents in the corpus')
#print(names[:10])

dic = corpora.Dictionary(docs)
#print(dic)

corpus = [dic.doc2bow(text) for text in docs]
#print(type(corpus), len(corpus))

tfidf = models.TfidfModel(corpus)
#print(type(tfidf))

corpus_tfidf = tfidf[corpus]
#print(type(corpus_tfidf))

NUM_TOPICS = 50
model = models.ldamodel.LdaModel(corpus_tfidf, 
                                 num_topics=NUM_TOPICS, 
                                 id2word=dic, 
                                 update_every=1, 
                                 passes=5)
                                 
print("LDA model")
topics_found = model.print_topics(50)
counter = 1
for t in topics_found:
    print("Topic {}: {}".format(counter, t))
    counter += 1