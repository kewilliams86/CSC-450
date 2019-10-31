#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 12:18:13 2019

@author: kewilliams

stem full text files

requires words.py script from CPP_setup repository on GitHub
CPP_setup/stem/

previous evaluation decised snowball stemmer to be ideal
"""

from nltk import SnowballStemmer
from words import getWords
import os
import sys
import argparse
import timeit


def writeToFile (inputDirectory, outputDirectory):
    
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
                    text = stemLine(line)
                    writeFile.write(text)

        if count % 20 == 0:
            t2 = timeit.default_timer()
            time = "Time elapsed: " + str(t2-t1) + ' seconds'
            print(str(count) + ' articles written... ' + time)
        count += 1    
    
    
def stemLine (line):

    snow = SnowballStemmer('english')
    
    text = line.strip('\n').split('\t')
    
    title = getWords(text[1])
    title = [snow.stem(t) for t in title]
    
    abstract = getWords(text[2]) 
    abstract = [snow.stem(a) for a in abstract]
    
    line = text[0] + '\t' + (' ').join(title) + '\t' + (' ').join(abstract) + '\t' + ('\t').join(text[3:]) + '\n'
    return line
            
            
# main program
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Extract dcast article information from PubMed xml files')
ap.add_argument("inputDirectory", help = "directory of input files")
ap.add_argument("outputDirectory", help = "directory of output files")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

#file and directory locations
inputDirectory = args['inputDirectory']
outputDirectory = args['outputDirectory']

# make sure read from directory
if not inputDirectory.endswith('/'):
    inputDirectory += '/'

# make sure output to directory
if not outputDirectory.endswith('/'):
    outputDirectory += '/'

if not os.path.exists(outputDirectory):
    os.makedirs(outputDirectory)
    
writeToFile (inputDirectory, outputDirectory)