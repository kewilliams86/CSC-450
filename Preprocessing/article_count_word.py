#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 16:46:57 2019

@author: kewilliams

write file containing all words present in at least 10% of articles

usage: article_count_word.py inputFile significantWordKeepFile
"""
import sys
import argparse


def createKeepWordSet(keepWordFile):
    with open(keepWordFile) as inFile:
        return {line.strip('\n') for line in inFile}


def countWords (readFile):    
    # most common words in breast cancer articles
    with open(readFile) as inFile:
        articleCount = 0
        wordDict = {}
        for line in inFile:
            data = line.strip('\n').split('\t')
            title = data[0].split(' ')
            abstract = data[1].split(' ')
            
            text = set()
            [text.add(w) for w in abstract]
            [text.add(w) for w in title]
            
            articleCount += 1
            
            text = [word for word in text]
            
            for word in text:
                if word in wordDict:
                    wordDict[word] += 1
                else:
                    wordDict[word] = 1
            if articleCount % 20000 == 0:
                print(str(articleCount) + ' articles processed')
    return wordDict, articleCount

def writeToFile (outFile, keepWordSet, wordDict, articleCount):
    with open(outFile[:-4] + '_word_count.csv', 'w') as writeFile:
        [writeFile.write(key + '\t' + str(wordDict[key]) + '\t' + str(round(wordDict[key] / articleCount, 3)) + '\n') \
         for key in wordDict if (wordDict[key] / articleCount) >= .02 and key not in keepWordSet]

ap = argparse.ArgumentParser(description='Count words in input file and write to file if present in 10% of articles')
ap.add_argument("inputFile", help = "Input file")
ap.add_argument('keepWordFile', help = 'File for potentially meaninful words to keep')

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

#file locations
inputFile = args['inputFile']
keepWordFile = args['keepWordFile']

keepWordSet = createKeepWordSet(keepWordFile)
output = countWords(inputFile)
writeToFile(inputFile, keepWordSet, output[0], output[1])