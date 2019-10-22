#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 12:09:26 2019

@author: kewilliams

database retrieval of cancer related pmids, retrieve corresponding terms, write to file
for bulk conversion of all 972 files.

testPMIDget.py username password inputdirectory outputdirectory disease2pubtatorfile 
"""

import mysql.connector
from mysql.connector import errorcode
import argparse
import sys
from collections import defaultdict
import os

def splitLine (line):
    return line.strip('\n').split('\t')


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
        cursor.execute('select distinct pmid from PubMesh')
        pmids = set(cursor.fetchall())
        cnx.close()
        for pmid in pmids:
            pmidDict[str(pmid)[1:-2]] = [] # string (pmid,) -- remove (,)
    return pmidDict

# iterate through disease2pubtator file and append terms to matching PMIDs in dictionary
def addTerms (pmidDict, diseaseFile):
# add disease descriptor terms to pmid in default dict
    with open(diseaseFile) as inFile:
        inFile.readline() #ignore first line (explainatory text)
        for line in inFile:
            data = splitLine(line)
            if data[0] in pmidDict:
                pmidDict[data[0]].append(data[1])
    return pmidDict

# read each file in the directory, write each line to new file with the disease terms added to the end
def writeToFile (pmidDict, inputDirectory, outputDirectory):
    
    #retrieve all files, place into a list, and sort
    directory = os.fsencode(inputDirectory)
    fileList = [os.fsdecode(file) for file in os.listdir(directory)]
    fileList.sort()
    directory = eval(str(directory)[1:]) #alter directory string to reflect accurate name
    
    count = 1 #counter to indicate # of files written
    
    # iterate through all files, open matching input and output files
    for file in fileList:
        with open(directory + file) as inFile:
            with open(outputDirectory + file + 'terms.txt', 'w') as writeFile:
                for line in inFile:
                    # split input line, write desired indices of data and add tab delimited terms
                    data = splitLine(line)
                    terms = ('\t').join(pmidDict[eval(data[0])])
                    writeFile.write(eval(data[0]) + '\t' + eval(data[1]) + '\t' + eval(data[5]) + '\t' + terms + '\n')
        
        if count % 50 == 0:
            print(str(count) + ' articles written')                
        count += 1    
            
        
# main program
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Extract dcast article information from PubMed xml files')
ap.add_argument("username", help="dcast username")
ap.add_argument("password", help="dcast password")
ap.add_argument("inputDirectory", help = "directory of input files")
ap.add_argument("outputDirectory", help = "directory of output files")
ap.add_argument("disease2pubtatorfile", help = "disease2pubtator file")

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
diseaseFile = args['disease2pubtatorfile']

if not os.path.exists(outputDirectory):
    os.makedirs(outputDirectory)

print('Retrieving PMIDS from database...')
pmidDict = dCastDatabase (userName, password)
print('Adding Terms to PMID dictionary...')
pmidDict = addTerms (pmidDict, diseaseFile)
print('Writing to files...')
writeToFile (pmidDict, inputDirectory, outputDirectory)
print('All files written to selected directory...')

