#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 12:04:03 2019

@author: kewilliams
"""

from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
from collections import defaultdict
from nltk.corpus import stopwords
from nltk import SnowballStemmer
import nltk


def lemmatizeText(text, stop_word_set):
    
    stop_word_set = set(stopwords.words('english')) # curious for speed testing, O(1) instead of linear
    #unsure of how tokenization parses ' and "
#    pattern = re.compile("\'|\"|\-") # remove -, ', " before lemmatization
#    text = pattern.sub('', text)
    text = text.replace('-', '') # only remove '-', want to reduce word with -
    
    lemma_function = WordNetLemmatizer()

    tag_map = defaultdict(lambda : wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV

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

def stemLine (text):

    snow = SnowballStemmer('english')
    
    text = [snow.steam(t) for t in text.split()]

    return (' ').join(text)