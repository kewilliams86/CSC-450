#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 15:21:25 2019

@author: kewilliams
"""

import argparse
import sys
from collections import defaultdict
import os




# main program
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Remove articles with unwanted MeSH IDs')
ap.add_argument("inputFile", help = "Input file")
ap.add_argument("outputFile", help = "Output file")
ap.add_argument("keepMeshFile", help = "File with MeSH IDs being retained")
ap.add_argument("newTermFile", help = "File with new MeSH associations")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

#file locations
inputFile = args['inputFile']
outputFile = args['outputFile']
keepFile = args['keepMeshFile']
termFile = args['newTermFile']


newAssociationDict = {}
with open(termFile) as inFile:
    inFile.readline() #skip header
    for line in inFile:
        data = line.strip('\n').split('\t')
        newAssociationDict[data[0]] = data[1]
        
keepMeshSet = {}
with open(keepFile) as inFile:
    keepMeshSet = {line.split('\t')[1] for line in inFile}
        
        
with open(outputFile, 'w') as writeFile:
    with open(inputFile) as inFile:    
        for line in inFile:
            data = line.strip('\n').split('\t')
            if data[2] in keepMeshSet:
                writeFile.write(line)
            elif data[2] in newAssociationDict:
                writeFile.write(data[0] + '\t' + data[1] + '\t' + newAssociationDict[data[2]] + '\n')