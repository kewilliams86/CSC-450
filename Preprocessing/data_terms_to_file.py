#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 11:58:00 2019

@author: kewilliams
"""

from collections import defaultdict

dataFile = "/home/kewilliams/Documents/GitHub/CSC-450/Data_Sets/extracted_pubmed19n0001.txt"
termFile = "/home/kewilliams/Documents/GitHub/CSC-450/Term_Files/disease2pubtator_processed"
outFile = "/home/kewilliams/Documents/GitHub/CSC-450/Data_Sets/pubmed19n0001_data_terms.txt"

def splitLine (line):
    return line.strip('\n').split('\t')

pmidTermDict = defaultdict(list)

with open(dataFile) as inFile:
    for line in inFile:
        pmidTermDict[eval(splitLine(line)[0])] = []


with open(termFile) as inFile:
    inFile.readline() #ignore first line (explainatory text)
    for line in inFile:
        data = splitLine(line)
        if data[0] in pmidTermDict:
            pmidTermDict[data[0]].append(data[1])


#count = 0

with open(outFile, 'w') as writeFile:
    with open(dataFile) as inFile:
        for line in inFile:
            data = splitLine(line)
            termList = pmidTermDict[eval(data[0])]
            terms = ('\t').join(termList)
            writeFile.write(eval(data[0]) + '\t' + eval(data[1]) + '\t' + eval(data[5]) + '\t' + terms + '\n')
#            count += 1
#            if count >= 100:
#                break
            