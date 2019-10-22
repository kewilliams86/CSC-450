#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 11:58:00 2019

@author: kewilliams

no database retrieval, for small sample only due to inefficiency

usage: sample_data_term_to_file.py [-h] inputFile outputFile disease2pubtator_processed
"""

from collections import defaultdict
import argparse
import sys

def splitLine (line):
    return line.strip('\n').split('\t')


def pmidToDict (dataFile, pmidTermDict):
    with open(dataFile) as inFile:
        for line in inFile:            
            pmidTermDict[eval(splitLine(line)[0])] = []
    return pmidToDict

def addTerms (termFile, pmidTermDict):
    with open(termFile) as inFile:
        inFile.readline() #ignore first line (explainatory text)
        for line in inFile:
            data = splitLine(line)
            if data[0] in pmidTermDict:
                pmidTermDict[data[0]].append(data[1])
    return pmidTermDict

def writeToFile (outFile, pmidTermDict):
    count = 0
    
    with open(outFile, 'w') as writeFile:
        with open(dataFile) as inFile:
            for line in inFile:
                data = splitLine(line)
                terms = ('\t').join(pmidTermDict[eval(data[0])])
                writeFile.write(eval(data[0]) + '\t' + eval(data[1]) + '\t' + eval(data[5]) + '\t' + terms + '\n')
                count += 1
                if count >= 100:
                    break
                
            
# main program
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Extract dcast article information from PubMed xml files')
ap.add_argument("inputFile", help="input file")
ap.add_argument("outputFile", help = "output file")
ap.add_argument("disease2pubtator_processed", help="disease2pubtator_processed file")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

dataFile = args['inputFile']
outFile = args['outputFile']
termFile = args['disease2pubtator_processed']

pmidTermDict = defaultdict(list)


print('Adding PMID to dictionary...')
pmidToDict (dataFile, pmidTermDict)
print('Adding terms to dictionary...')
pmidTermDict = addTerms(termFile, pmidTermDict)
print('Writing to file...')
writeToFile (outFile, pmidTermDict)