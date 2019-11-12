#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 16:46:57 2019

@author: kewilliams
"""

# most common words in breast cancer articles
with open('/home/kewilliams/Documents/CSC-450/preprocessed_data/all_file_terms.txt') as inFile:
    breastCancerCount = 0
    wordDict = {}
    breastWordDict = {}
    for line in inFile:
        data = line.strip('\n').split('\t')
        title = data[0].split(' ')
        abstract = data[1].split(' ')
        if data[2] == 'D001943':
            breastCancerCount += 1
            for word in title:
                if word in wordDict:
                    breastWordDict[word] += 1
                    wordDict[word] += 1
                else:
                    breastWordDict[word] = 1
                    wordDict[word] = 1
            for word in title:
                if word in wordDict:
                    breastWordDict[word] += 1
                    wordDict[word] += 1
                else:
                    breastWordDict[word] = 1
                    wordDict[word] = 1
        else:
            for word in title:
                if word in wordDict:
                    wordDict[word] += 1
                else:
                    wordDict[word] = 1
            for word in title:
                if word in wordDict:
                    wordDict[word] += 1
                else:
                    wordDict[word] = 1

with open('/home/kewilliams/Documents/CSC-450/most_common_words.csv', 'w') as writeFile:
    [writeFile.write(key + '\t' + str(wordDict[key]) + '\n') for key in wordDict if wordDict[key] > 5000]

with open('/home/kewilliams/Documents/CSC-450/most_common_words_breast_cancer.csv', 'w') as writeFile:
    writeFile.write('# of articles\t' + str(breastCancerCount) + '\n\n')
    [writeFile.write(key + '\t' + str(wordDict[key]) + '\n') for key in wordDict if wordDict[key] > 500]

