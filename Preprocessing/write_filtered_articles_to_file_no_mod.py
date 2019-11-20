#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 12:09:26 2019

@author: kewilliams

database retrieval of cancer related pmids, retrieve corresponding terms, write to file
for bulk conversion of all 972 files.

requires words.py from GitHub repository CPP_setup

if printing to single file, add 'True' as an additional argument at command line

write_filtered_articles_to_file_no_mod.py username password inputdirectory outputdirectory keepMeshIDFile newMeshAssociationFile [singleFile]

"""

import mysql.connector
from mysql.connector import errorcode
import argparse
import sys
import os


def createAssociationDict(termFile):
    newAssociationDict = {}
    with open(termFile) as inFile:
        inFile.readline() #skip header
        for line in inFile:
            data = line.strip('\n').split('\t')
            newAssociationDict[data[0]] = data[1]
    return newAssociationDict

            
def createKeepMeshSet(keepFile):
    keepMeshSet = {}
    with open(keepFile) as inFile:
        keepMeshSet = {line.split('\t')[1] for line in inFile}
    return keepMeshSet


def filterPmid(pmidDict, newAssociationDict, keepMeshSet):
    updatedDict = {}
    for key in pmidDict:
        if pmidDict[key] == None: # skip articles with more than one MeSH ID
            continue
        elif pmidDict[key] in keepMeshSet: # pmid MeSH ID in keepMeshSet
            updatedDict[key] = pmidDict[key]
        elif pmidDict[key] in newAssociationDict: # pmid MeSH ID in newAssociation
            updatedDict[key] = newAssociationDict[pmidDict[key]]
    return updatedDict

retractedPmid = []

# query database for all cancer related PMIDs
# store all PMIDs into defaultdict keys with an empty list as values
def dCastDatabase (userName, password):
    
    pmidDict = {}
    
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
                if data[0] in pmidDict:
                    pmidDict[data[0]] = None
                else:
                    pmidDict[data[0]] = data[1] # pmids with multiple IDs get None
            data = cursor.fetchone()

        cnx.close()
    return pmidDict

#remove  \n \\n object background methods conclusions
def modifyText(text):
    text = text.replace('\n', '').replace('\\n', '').replace('OBJECTIVE', '').replace('BACKGROUND', '')
    text = text.replace('METHODS', '').replace('CONCLUSIONS', '')
    return text

# read each file in the directory, write each line to new file with the disease terms added to the end
def writeToFile (updatedDict, inputDirectory, outputDirectory, singleFile):
    
    #retrieve all files, place into a list and sort
    directory = os.fsencode(inputDirectory)
    fileList = [os.fsdecode(file) for file in os.listdir(directory)]
    fileList.sort()
    directory = eval(str(directory)[1:]) #alter directory string to reflect accurate name
    
    count = 1 #counter to indicate # of files written    

    if singleFile == True:
        with open(outputDirectory + 'all_articles_no_mod.txt', 'w') as writeFile:
            for file in fileList:
                with open(directory + file) as inFile:
                    for line in inFile:
                        writeLine(line, writeFile, updatedDict)
                if count % 50 == 0:
                    print(str(count) + ' articles written...')
                count += 1        
    
    else:
        # iterate through all files, open matching input and output files
        for file in fileList:
            with open(directory + file) as inFile:
                with open(outputDirectory + file[:-4] + '_no_mod.txt', 'w') as writeFile: # remove .txt from file
                    for line in inFile:                    
                        writeLine(line, writeFile, updatedDict)
            if count % 50 == 0:
                print(str(count) + ' articles written...')             
            count += 1


def writeLine (line, writeFile, updatedDict):
    # split input line, write desired indices of data and add tab delimited terms    
    data = line.strip('\n').split('\t')
    
    if data[1].startswith("RETRACTED:"): #skip retracted article, add pmid to list
        return
    
    # if article with single MeSH ID and in filtered dictionary
    if eval(eval(data[0])) in updatedDict and updatedDict[eval(eval(data[0]))] != None:
        #eval(eval()) used to convert ascii encapsulation to string to int
        data[1] = modifyText(eval(data[1]))
        data[5] = modifyText(eval(data[5]))
        writeFile.write(data[1] + '\t' + data[5] + '\t' + updatedDict[eval(eval(data[0]))] + '\n')
            
        
# main program
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Write PMID, title, abstract and corresponding MeshTerms to file')
ap.add_argument("username", help="dcast username")
ap.add_argument("password", help="dcast password")
ap.add_argument("inputDirectory", help = "directory of input files")
ap.add_argument("outputDirectory", help = "directory of output files")
ap.add_argument("keepMeshFile", help = "File with MeSH IDs being retained")
ap.add_argument("newTermFile", help = "File with new MeSH associations")
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
keepFile = args['keepMeshFile']
termFile = args['newTermFile']
singleFile = args['singleFile']

# make sure read from directory
if not inputDirectory.endswith('/'):
    inputDirectory += '/'

# make sure output to directory
if not outputDirectory.endswith('/'):
    outputDirectory += '/'

if not os.path.exists(outputDirectory):
    os.makedirs(outputDirectory)

print('Processing new associations...')
newAssociationDict = createAssociationDict(termFile)
print('Creating set of MeSH IDs to keep...')
keepMeshSet = createKeepMeshSet(keepFile)
print('Retrieving PMIDS from database...')
pmidDict = dCastDatabase (userName, password)
print('Filtering out PMIDs...')
updatedDict = filterPmid(pmidDict, newAssociationDict, keepMeshSet)
print('Writing to file(s)...')
writeToFile (updatedDict, inputDirectory, outputDirectory, singleFile)
print('All files written to selected directory...')

