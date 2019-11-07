#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 12:18:13 2019

@author: kewilliams

stem full text files

requires words.py script from CPP_setup repository on GitHub
CPP_setup/stem/

previous evaluation decided snowball stemmer to be ideal

usage: stem_terms.py inputDirectory outputDirectory
"""

from nltk import SnowballStemmer
from words import getWords
import os
from pathlib import Path
import sys
import argparse
import timeit


def writeToFile (inputDirectory, outputDirectory, singleFile):
    
    if singleFile == True:
        print('writing to file...')
        count = 1
        with open(inputDirectory) as inFile:
            with open(outputDirectory + 'all_file_terms_stem.txt', 'w') as writeFile:
                for line in inFile:
                    data = line.split('\t')
                    text = stemLine(data[0], data[1])
                    writeFile.write(text + '\t' + data[2])
                    
                    if count % 20000 == 0:
                        print(str(count) + ' articles written...')
                    count += 1
        
    else:
        #retrieve all files, place into a list and sort
        directory = os.fsencode(inputDirectory)
        fileList = [os.fsdecode(file) for file in os.listdir(directory)]
        fileList.sort()
        directory = eval(str(directory)[1:]) #alter directory string to reflect accurate name
    
        count = 1 #counter to indicate # of files written
        t1 = timeit.default_timer()
        # iterate through all files, open matching input and output files
        for file in fileList:
            with open(directory + file) as inFile:
                with open(outputDirectory + file[:-4] + '_stem.txt', 'w') as writeFile: # remove .txt from file
    
                    for line in inFile:
                        data = line.split('\t')
                        text = stemLine(data[0], data[1])
                        writeFile.write(text + '\t' + data[2])
    
            if count % 20 == 0:
                t2 = timeit.default_timer()
                time = "Time elapsed: " + str(t2-t1) + ' seconds'
                print(str(count) + ' articles written... ' + time)
            count += 1    
    
    
def stemLine (title, abstract):

    snow = SnowballStemmer('english')
    
    title = [snow.stem(t) for t in title.split()]
    abstract = [snow.stem(a) for a in abstract.split()]

    return (' ').join(title) + '\t' + (' ').join(abstract)
            
            
# main program
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Extract dcast article information from PubMed xml files')
ap.add_argument("inputDirectory", help = "directory of input files or filename")
ap.add_argument("outputDirectory", help = "directory of output file(s)")
ap.add_argument("singleFile", type = bool, help = "optional argument for single file input", nargs = '?', default = False)

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

#file and directory locations
inputDirectory = args['inputDirectory']
outputDirectory = args['outputDirectory']
singleFile = args['singleFile']

if singleFile == False:
    # make sure read from directory
    if not inputDirectory.endswith('/'):
        inputDirectory += '/'

# make sure output to directory
if not outputDirectory.endswith('/'):
    outputDirectory += '/'

if not os.path.exists(outputDirectory):
    os.makedirs(outputDirectory)
    
writeToFile (inputDirectory, outputDirectory, singleFile)