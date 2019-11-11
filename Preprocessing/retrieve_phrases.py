#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 13:52:59 2019

@author: kevin
"""
from nltk.corpus import stopwords
import os
from nltk.stem import WordNetLemmatizer
import nltk


def getPhrases(readFile, punctuation, stopWordSet, phraseDict, lemmatizer):
    with open(readFile) as inFile:
        words = inFile.readline().split(' ') #read all words from file
        phrase = ''
        count = 0 # count of words in phrase
        for i in range(len(words) - 1): #iterate through all words
            #if word not punctuation or stop word
            if words[i] not in stopWordSet and words[i] not in punctuation and words[i] != '':
                phrase += lemmatizer.lemmatize(words[i]) + ' '
                count += 1
                
            else:
                #if at least 2 consecutive words
                if count >= 2:
                    phrase = phrase[:-1] #last character is a ' '
                    if phrase in phraseDict: #increment count of phrase if in dict
                        value = phraseDict.get(phrase)
                        phraseDict[phrase] = value + 1
                    else:
                        phraseDict[phrase] = 1 #first instance of phrase
                #reset count and phrase
                count = 0
                phrase = ''
    return phraseDict

#create set of stop words
stopWordSet = {word for word in stopwords.words('english')}

punctuation = {'.', ',', '\'', '"', ';', ':', '-', '\\', '(', ')', '[', ']', '{', '}', '>', 
               '<', '?', '/', '!', '@', '#', '$', '%', '^', '&', '*', '+', '=', '~', '`'}

lemmatizer = WordNetLemmatizer()
nltk.download('wordnet')


directory = os.fsencode('450_files/')
fileList = [os.fsdecode(file) for file in os.listdir(directory)]
fileList.sort()
directory = eval(str(directory)[1:])

phraseDict = {}

print('creating phrase dictionary...')

count = 0
fileLocation = 0

for file in fileList:
    fileLocation += 1
    phraseDict = getPhrases(directory + file, punctuation, stopWordSet, phraseDict, lemmatizer)
    if fileLocation % 200 == 0:
        count += 1
        with open('Phrases/phrases' + str(count) + '.csv', 'w') as writeFile:
            print('Files ' + str(fileLocation - 200) + ' - ' + str(fileLocation) + ' written')
            [writeFile.write(key + '\t' + str(phraseDict[key]) + '\n') for key in phraseDict if phraseDict[key] >= 20]
            phraseDict = {}
    
with open('Phrases/phrases' + str(count) + '.csv', 'w') as writeFile:
     [writeFile.write(key + '\t' + str(phraseDict[key]) + '\n') for key in phraseDict if phraseDict[key] >= 20]
     print(str(fileLocation) + ' files written')

print('Compiling all phrases...')