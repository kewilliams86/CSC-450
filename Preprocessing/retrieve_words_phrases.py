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

#create set of stop words
stopWordSet = {word for word in stopwords.words('english')}

punctuation = {'.', ',', '\'', '"', ';', ':', '-', '\\', '(', ')', '[', ']', '{', '}', '>', 
               '<', '?', '/', '!', '@', '#', '$', '%', '^', '&', '*', '+', '=', '~', '`'}
               
lemmatizer = WordNetLemmatizer()
nltk.download('wordnet')

def getPhrases(readFile, phraseDict):
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
                if count >= 1:
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




lemmatizer = WordNetLemmatizer()
nltk.download('wordnet')

directory = os.fsencode('/home/kewilliams/Documents/CSC-450/preprocessed_data/raw_text_punctuation/')
fileList = [os.fsdecode(file) for file in os.listdir(str(directory)[1:].strip("'"))]
fileList.sort()
directory = eval(str(directory)[1:])

phraseDict = {}

print('creating phrase dictionary...')

count = 0
fileLocation = 0

for file in fileList:
    fileLocation += 1
    phraseDict = getPhrases(directory + file, phraseDict)
    if fileLocation % 200 == 0:
        count += 1
        with open('/home/kewilliams/Documents/CSC-450/Phrases/phrases' + str(count) + '.csv', 'w') as writeFile:
            print('Files ' + str(fileLocation - 200) + ' - ' + str(fileLocation) + ' written')
            [writeFile.write(key + '\t' + str(phraseDict[key]) + '\n') for key in phraseDict if phraseDict[key] >= 20]
            phraseDict = {}
    
with open('/home/kewilliams/Documents/CSC-450/Phrases/phrases' + str(count) + '.csv', 'w') as writeFile:
     [writeFile.write(key + '\t' + str(phraseDict[key]) + '\n') for key in phraseDict if phraseDict[key] >= 20]
     print(str(fileLocation) + ' files written')

print('Compiling all phrases...')

directory = os.fsencode('/home/kewilliams/Documents/CSC-450/Phrases/')
fileList = [os.fsdecode(file) for file in os.listdir(directory)]
fileList.sort()
directory = eval(str(directory)[1:])

phraseDict = {}

for file in fileList:
    with open(directory + file) as inFile:
        for line in inFile:
            data = line.strip('\n').split('\t')
            if data[0] in phraseDict:
                value = phraseDict[data[0]]
                phraseDict[data[0]] = int(value) + int(data[1])
            else:    
                phraseDict[data[0]] = data[1]

print('writing file...')

with open('/home/kewilliams/Documents/CSC-450/all_phrases.csv', 'w') as writeFile:
    [writeFile.write(key + '\t' + str(phraseDict[key]) + '\n') for key in phraseDict if int(phraseDict[key]) >= 100]