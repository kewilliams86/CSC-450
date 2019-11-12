#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 16:46:57 2019

@author: kewilliams
"""
from nltk.stem import WordNetLemmatizer
#import nltk

lemmatizer = WordNetLemmatizer()

# most common words in breast cancer articles
with open('/home/kewilliams/Documents/CSC-450/preprocessed_data/all_file_terms.txt') as inFile:
    breastCancerCount = 0
    articleCount = 0
    wordDict = {}
    breastWordDict = {}
    for line in inFile:
        data = line.strip('\n').split('\t')
        title = data[0].split(' ')
        abstract = data[1].split(' ')
        text = set()
        [text.add(w) for w in abstract]
        [text.add(w) for w in title]
        articleCount += 1
#        if data[2] == 'D001943':
#            breastCancerCount += 1
#            text = {lemmatizer.lemmatize(word) for word in text}
#            for word in text:
#                if word in breastWordDict and word in wordDict:
#                    breastWordDict[word] += 1
#                    wordDict[word] += 1
#                else:
#                    breastWordDict[word] = 1
#                    wordDict[word] = 1
#
#        else:
#            text = {lemmatizer.lemmatize(word) for word in text}
#            for word in text:
#                if word in wordDict:
#                    wordDict[word] += 1
#                else:
#                    wordDict[word] = 1
        
        text = {lemmatizer.lemmatize(word) for word in text}
        for word in text:
            if word in wordDict:
                wordDict[word] += 1
            else:
                wordDict[word] = 1


with open('/home/kewilliams/Documents/CSC-450/most_common_words_percent.csv', 'w') as writeFile:
    [writeFile.write(key + '\t' + str(wordDict[key]) + '\t' + str(round(wordDict[key] / articleCount, 3)) + '\n') for key in wordDict if wordDict[key] > 10000]

#with open('/home/kewilliams/Documents/CSC-450/most_common_words_percent_breast_cancer.csv', 'w') as writeFile:
#    writeFile.write('# of articles\t' + str(breastCancerCount) + '\n\n')
#    [writeFile.write(key + '\t' + str(breastWordDict[key]) + '\t' + str(round(breastWordDict[key] / breastCancerCount, 3)) + '\n') for key in breastWordDict if breastWordDict[key] > 5000]