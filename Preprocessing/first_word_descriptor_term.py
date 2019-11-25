#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 12:04:48 2019

@author: kewilliams

usage: first_word_descriptor_term.py keepMeshFile keepWordFile remappedMeshIDFile descFile2019 nlpType(optional(stem/lemmatize))
"""
import re
from nltk.corpus import stopwords
import string
import sys
import argparse
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import SnowballStemmer

def getTerms(termSet, termDict):
    
    table = str.maketrans('', '', string.punctuation)

    terms = [termDict[key].translate(table) for key in termDict]
    
    wordCountDict = {}
    
    for term in terms:
        temp = term.split(' ')[0].lower()
        if temp in wordCountDict:
            wordCountDict[temp] += 1
        else:
            wordCountDict[temp] = 1
            
        termSet.add(temp.lower())
    
    return termSet

ap = argparse.ArgumentParser(description='identify potentially meaningful words')
ap.add_argument("keepMeshFile", help = "File with meshIDs being kept")
ap.add_argument('keepWordFile', help = 'File for potentially meaninful words to keep')
ap.add_argument('remappedfile', help = 'File of remapped mesh IDs')
ap.add_argument("descFile", help = "File with descriptor terms")
ap.add_argument("nlpType", help = "Type of NLP processing", nargs = '?', default = None)

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

#file locations
keepMeshFile = args['keepMeshFile']
keepWordFile = args['keepWordFile']
remappedFile = args['remappedfile']
descFile = args['descFile']
nlpType = args['nlpType']

#keepMeshFile = '/home/kewilliams/Documents/CSC-450/keep_meshID.csv'
#keepWordFile = '/home/kewilliams/Documents/CSC-450/keep_meaningful.txt'
#nlpType = None
#remappedFile = '/home/kewilliams/Documents/CSC-450/new_mesh_associations.txt'
#descFile = '/home/kewilliams/Documents/CSC-450/term_id/processed/desc2019.txt'

pattern = re.compile("\'|\"|\-")
stop_words = set(stopwords.words('english'))

with open(keepMeshFile) as inFile:
    termDict = {line.split('\t')[1] : line.strip('\n').split('\t')[2].strip('"') for line in inFile}
    
termSet = set()
termSet = getTerms(termSet, termDict)
    
with open(remappedFile) as readFile:
    idSet = {line.split('\t')[0] for line in readFile}

with open(descFile) as readFile:
    termDict = {eval(line.split('\t')[0]) : eval(line.split('\t')[1]) for line in readFile if eval(line.split('\t')[0]) in idSet}

termSet = getTerms(termSet, termDict) 


remove_words = []
remove_words.append('cell')
remove_words.append('neoplasm')
remove_words.append('neoplasms')
remove_words.append('multiple')

[termSet.remove(term) for term in remove_words]

if nlpType == 'stem':
    snow = SnowballStemmer('english')
    termSet = {snow.stem(term) for term in termSet}
elif nlpType == 'lemmatize':
    lemmatizer = WordNetLemmatizer()
    termSet = {lemmatizer.lemmatize(term) for term in termSet}

with open(keepWordFile, 'w') as writeFile:
    [writeFile.write(term + '\n') for term in termSet]