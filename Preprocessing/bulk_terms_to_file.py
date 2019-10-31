#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 12:09:26 2019

@author: kewilliams

database retrieval of cancer related pmids, retrieve corresponding terms, write to file
for bulk conversion of all 972 files.

testPMIDget.py username password inputdirectory outputdirectory
"""

import mysql.connector
from mysql.connector import errorcode
import argparse
import sys
from collections import defaultdict
import os


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
            pmidDict[data[0]].append(data[1])
            data = cursor.fetchone()

        cnx.close()
    return pmidDict

#remove  \n \\n object background methods conclusions
def removeKeywords(text):
    return text.replace('\n', '').replace('\\n', '').replace('OBJECTIVE', '').replace('BACKGROUND', '').replace('METHODS', '').replace('CONCLUSIONS', '')

# read each file in the directory, write each line to new file with the disease terms added to the end
def writeToFile (pmidDict, inputDirectory, outputDirectory):
    
    
    
    #retrieve all files, place into a list and sort
    directory = os.fsencode(inputDirectory)
    fileList = [os.fsdecode(file) for file in os.listdir(directory)]
    fileList.sort()
    directory = eval(str(directory)[1:]) #alter directory string to reflect accurate name
    
    retractedPmid = []
    count = 1 #counter to indicate # of files written
    
    # iterate through all files, open matching input and output files
    for file in fileList:
        with open(directory + file) as inFile:
            with open(outputDirectory + file[:-4] + '_terms.txt', 'w') as writeFile: # remove .txt from file
                for line in inFile:
                    # split input line, write desired indices of data and add tab delimited terms
                    data = line.strip('\n').split('\t')
                    
                    #eval(eval()) used to convert ascii encapsulation to string to int
                    # tab delimited term string
                    terms = ('\t').join(pmidDict[eval(eval(data[0]))])
                    
                    data[1] = removeKeywords(eval(data[1]))
                    data[5] = removeKeywords(eval(data[5]))
                    
                    if data[1].startswith("RETRACTED:"):
                        retractedPmid.append([eval(data[0]), file])
                    else: # .replace('\\n') handles rare case of '\n' mid abstract or title
                        writeFile.write(eval(data[0]) + '\t' + data[1] + '\t' + data[5] + '\t' + terms + '\n')

        if count % 50 == 0:
            print(str(count) + ' articles written')                
        count += 1
    with open('retracted_pmids.txt', 'w') as writeFile:
        writeFile.write("Retracted PMIDs not written to file:\n")
        for item in retractedPmid:
            writeFile.write(str(item[0]) + '\t' + str(item[1]) + '\n')
            
        
# main program
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Write PMID, title, abstract and corresponding MeshTerms to file')
ap.add_argument("username", help="dcast username")
ap.add_argument("password", help="dcast password")
ap.add_argument("inputDirectory", help = "directory of input files")
ap.add_argument("outputDirectory", help = "directory of output files")

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
print('Writing to files...')
writeToFile (pmidDict, inputDirectory, outputDirectory)
print('All files written to selected directory...')

