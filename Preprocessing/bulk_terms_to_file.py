#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 12:09:26 2019

@author: kewilliams

database retrieval of cancer related pmids, retrieve corresponding terms, write to file
for bulk conversion of all 972 files.

requires words.py from GitHub repository CPP_setup

if printing to single file, add 'True' as an additional argument at command line

testPMIDget.py username password inputdirectory outputdirectory [singleFile]

"""

import mysql.connector
from mysql.connector import errorcode
import argparse
import sys
from collections import defaultdict
import os
from words import testValid, getWords
from nltk.corpus import stopwords


stop_words = stopwords.words('english') #load english stopwords

retractedPmid = []

# query database for all cancer related PMIDs
# store all PMIDs into defaultdict keys with an empty list as values
def dCastDatabase (userName, password):
    
    pmidDict = defaultdict(list)
    
    try:
        cnx = mysql.connector.connect(user=userName, password=password,
                                      database='dcast')
    except mysql.connector.Error as err:
        
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = cnx.cursor(buffered=True)
        cursor.execute('select * from PubMesh')
        
        #fetchone retrieves tuple (pmid, diseaseID, None)
        data = cursor.fetchone()
        while data is not None:
            if data[1].startswith('D'): #only count descriptor terms, no supplemental
                pmidDict[data[0]].append(data[1])
            data = cursor.fetchone()

        cnx.close()
    return pmidDict

#remove  \n \\n object background methods conclusions
def modifyText(text):
    text = text.replace('\n', '').replace('\\n', '').replace('OBJECTIVE', '').replace('BACKGROUND', '')
    text = text.replace('METHODS', '').replace('CONCLUSIONS', '')
    # get list of words, no punctuation, no numbers, > 2 length, no stopwords
    words = [w for w in getWords(text) if testValid(w, stop_words)] 
    return (' ').join(words) #return modified string

# read each file in the directory, write each line to new file with the disease terms added to the end
def writeToFile (pmidDict, inputDirectory, outputDirectory, singleFile):
    
    #retrieve all files, place into a list and sort
    directory = os.fsencode(inputDirectory)
    fileList = [os.fsdecode(file) for file in os.listdir(directory)]
    fileList.sort()
    directory = eval(str(directory)[1:]) #alter directory string to reflect accurate name
    
    count = 1 #counter to indicate # of files written    

    if singleFile == True:
        with open(outputDirectory + 'all_file_terms.txt', 'w') as writeFile:
            for file in fileList:
                with open(directory + file) as inFile:
                    for line in inFile:
                        writeLine(line, writeFile)
                if count % 50 == 0:
                    print(str(count) + ' articles written...')
                count += 1        
    
    else:
        # iterate through all files, open matching input and output files
        for file in fileList:
            with open(directory + file) as inFile:
                with open(outputDirectory + file[:-4] + '_terms.txt', 'w') as writeFile: # remove .txt from file
                    for line in inFile:                    
                        writeLine(line, writeFile)
            if count % 50 == 0:
                print(str(count) + ' articles written...')             
            count += 1
        
#    with open('retracted_pmids.txt', 'w') as writeFile:
#        writeFile.write("Retracted PMIDs not written to file:\n")
#        for item in retractedPmid:
#            writeFile.write(str(item) + '\n')


def writeLine (line, writeFile):
    # split input line, write desired indices of data and add tab delimited terms    
    data = line.strip('\n').split('\t')
    
    # tab delimited term string
    terms = ('\t').join(pmidDict[eval(eval(data[0]))])
    
    if data[1].startswith("RETRACTED:"): #skip retracted article, add pmid to list
        retractedPmid.append(eval(data[0]))
    
    #eval(eval()) used to convert ascii encapsulation to string to int
    elif len(pmidDict[eval(eval(data[0]))]) == 1: #if only one descriptor term
        data[1] = modifyText(eval(data[1]))
        data[5] = modifyText(eval(data[5]))
        writeFile.write(data[1] + '\t' + data[5] + '\t' + terms + '\n')
            
        
# main program
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Write PMID, title, abstract and corresponding MeshTerms to file')
ap.add_argument("username", help="dcast username")
ap.add_argument("password", help="dcast password")
ap.add_argument("inputDirectory", help = "directory of input files")
ap.add_argument("outputDirectory", help = "directory of output files")
ap.add_argument("singleFile", type = bool, help = "True if output to single file", nargs = '?', default = False)

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

#dcast database information
userName = args['username']
password = args['password']

#file and directory locations
inputDirectory = args['inputDirectory']
outputDirectory = args['outputDirectory']
singleFile = args['singleFile']

# make sure read from directory
if not inputDirectory.endswith('/'):
    inputDirectory += '/'

# make sure output to directory
if not outputDirectory.endswith('/'):
    outputDirectory += '/'

if not os.path.exists(outputDirectory):
    os.makedirs(outputDirectory)

print('Retrieving PMIDS from database...')
pmidDict = dCastDatabase (userName, password)
print('Writing to file(s)...')
writeToFile (pmidDict, inputDirectory, outputDirectory, singleFile)
print('All files written to selected directory...')

