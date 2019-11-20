#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 16:07:33 2019

@author: kewilliams

Partial code adapted from the response by user 'slider' on stackoverflow
https://stackoverflow.com/questions/37605710/tokenize-a-paragraph-into-sentence-and-then-into-words-in-nltk
"""

from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
from collections import defaultdict
from nltk.corpus import stopwords
import nltk
import timeit

stop_word = stopwords.words('english')
stop_word_set = set(stopwords.words('english')) # curious for speed testing, O(1) instead of linear

lemma_function = WordNetLemmatizer()

tag_map = defaultdict(lambda : wn.NOUN)
tag_map['J'] = wn.ADJ
tag_map['V'] = wn.VERB
tag_map['R'] = wn.ADV

def lemmatizeText(text):
    
    #unsure of how tokenization parses ' and "
#    pattern = re.compile("\'|\"|\-") # remove -, ', " before lemmatization
#    text = pattern.sub('', text)
    text = text.replace('-', '') # only remove '-', want to reduce word with -

    sent_text = nltk.sent_tokenize(text)
    data = []
    for s in sent_text:
        sentence = []
        tokens = word_tokenize(s)
        for token, tag in pos_tag(tokens):
            lemma = lemma_function.lemmatize(token, tag_map[tag[0]])
            if lemma.isalnum() and not lemma.isdigit() and len(lemma) > 2 and lemma not in stop_word_set:
                sentence.append(lemma.lower())
        data.append((' ').join(sentence))
    return (' ').join(data)

directory = '/home/kewilliams/Documents/CSC-450/preprocessed_data/'

beginTime = timeit.default_timer()


articleCount = 0
t0 = timeit.default_timer()

print('writing to file...')
with open(directory + 'all_file_terms_lemmatize.txt', 'w') as writeFile:
    with open(directory + 'all_articles_no_mod.txt') as inFile:
        for line in inFile:
            articleCount += 1
            data = line.strip('\n').split('\t')
            writeFile.write(lemmatizeText(data[0]) + '\t' + lemmatizeText(data[1]) + '\t' + data[2] + '\n')
            if articleCount % 20000 == 0:
                t1 = timeit.default_timer()
                print(str(articleCount) + ' articles written... ' + str(t1 - t0) + ' seconds')
                t0 = timeit.default_timer()
                
endTime = timeit.default_timer()

totalTime = endTime - beginTime
totalMin = totalTime // 60
totalSec = totalTime % 60
print('Total time spent = ' + str(totalMin) + 'minutes and ' + str(totalSec) + ' seconds')