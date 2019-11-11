#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 12:09:26 2019

@author: kewilliams

find number of meshIDs

"""

def countArticles(tempDict):
    count = 0
    for key in tempDict:
        count += tempDict[key]
    return count
    
    
def get_key(val, my_dict): 
    for key, value in my_dict.items(): 
         if val == value: 
             return key 
  
    return "key doesn't exist"

meshDict = {}

with open('/home/kewilliams/Documents/CSC-450/preprocessed_data/all_file_terms.txt') as inFile:

# create dictionary with meshID:# of articles with ID
    for line in inFile:
        text = line.strip('\n').split('\t')
        if text[2] in meshDict:
            meshDict[text[2]] = int(meshDict[text[2]]) + 1
        else:
            meshDict[text[2]] = 1
            
treeMeshDict = {}
meshTreeDict = {}
meshTermDict = {}


with open('/home/kewilliams/Documents/GitHub/CPP_setup/data_for_mysql/MeshTreeHierarchyWithScopeNotes.txt') as inFile:

# create a dictionary for TreeID:MeshID, MeshID:TreeID, TreeID:DiseaseName
    for line in inFile:
        text = line.strip('\n').split('\t')
        if text[0].startswith('C04'):
            treeMeshDict[text[0]] = text[1]
            meshTreeDict[text[1]] = text[0]
            meshTermDict[text[0]] = text[2]


replacedTerms = {}

def modifyKeys (i, modifyDict):
    
    keysToRemove = []
    for key in modifyDict:
        if len(key) >= i:
            newKey = key[:-4]
            if treeMeshDict[newKey] in meshDict:    
                meshDict[treeMeshDict[newKey]] += modifyDict[key]
            else:
                meshDict[treeMeshDict[newKey]] = modifyDict[key]
            keysToRemove.append(key)
            
            replacedTerms[key] = newKey
            
    # remove child keys from meshDict
    for item in keysToRemove:
        removedTreeIDs.append(item)
        del meshDict[treeMeshDict[item]]
            
        
histology = 'C04.557.470.200'
breast = 'C04.588.180'

# remove all keys in meshDict less than level 3
for key in treeMeshDict:
    if key.startswith(breast + '.') and treeMeshDict[key] in meshDict:
        meshDict[treeMeshDict[breast]] += meshDict[treeMeshDict[key]]
        del meshDict[treeMeshDict[key]]
    elif len(key) < 8 and treeMeshDict[key] in meshDict:
        del meshDict[treeMeshDict[key]]
    elif key.startswith(histology) and treeMeshDict[key] in meshDict:
        del meshDict[treeMeshDict[key]]
    
        

i = 32

termDict = {meshTreeDict[i]:meshDict[i] for i in meshTreeDict if i in meshDict}

removedTreeIDs = []

while i >= 20:
    modifyKeys(i, termDict)
    termDict = {meshTreeDict[i]:meshDict[i] for i in meshTreeDict if i in meshDict}
    i -= 4

    
# dictionary with tree ID and count of values if less than 200 articles with the ID
lowTermDict = {meshTreeDict[i]:meshDict[i] for i in meshTreeDict if i in meshDict and meshDict[i] < 200}

while i >= 12:
    
    modifyKeys(i, lowTermDict)
    lowTermDict = {meshTreeDict[i]:meshDict[i] for i in meshTreeDict if i in meshDict and meshDict[i] < 200}
    
    i -= 4 # move up tree one node

updatedDict = {meshTreeDict[i]:meshDict[i] for i in meshTreeDict if i in meshDict and meshDict[i] >= 200}


for key in replacedTerms:
    term = replacedTerms[key]
    termLength = len(term)
    while term not in updatedDict and termLength >= 12:
        term = term[:-4]
        termLength = len(term)
        if term in updatedDict:
            replacedTerms[key] = term

## view keys in csv file and track possible removal
#
#keysToRemove = []
#possibleRemoval = []
#
#for key in newTermDict:
#    if newTermDict[key] < 200:
#        possibleRemoval.append(key)
##        if len(key) < 8:
##            keysToRemove.append(key) # if not enough articles no further reduction
##        else:
##            possibleRemoval.append(key)
#
#possibleRemoval.sort()
#
#newTermList = list(newTermDict)
#newTermList.sort()
#
#possibleKeep = []
#
#i = 0
#for j in range(len(newTermList)):
#    if possibleRemoval[i] == newTermList[j]:
#        print(possibleRemoval[i])
#        print(newTermList[j+1])
#        if newTermList[j+1].startswith(str(possibleRemoval[i])):
#            possibleKeep.append(possibleRemoval[i])
#        i += 1
#        if i >= len(possibleRemoval):
#            break
#
#for item in possibleRemoval:
#    if item not in possibleKeep:
#        del meshDict[treeMeshDict[item]]
#
with open('/home/kewilliams/Documents/CSC-450/changed_meshID.csv', 'w') as writeFile:
    for item in updatedDict:
        if updatedDict[item] >= 200:
            writeFile.write(item + '\t' + treeMeshDict[item] + '\t' + meshTermDict[item] + '\t' + str(updatedDict[item]) + '\n')
            
with open('/home/kewilliams/Documents/CSC-450/new_mesh_associations.txt', 'w') as writeFile:
    writeFile.write('old\tnew\n')
    for item in replacedTerms:
        writeFile.write(treeMeshDict[item] + '\t' + treeMeshDict[replacedTerms[item]] + '\n')

#with open('/home/kewilliams/Documents/CSC-450/possible_keep_treeIDs.txt', 'w') as writeFile:
#    for item in possibleKeep:
#        writeFile.write(item + '\n')
#

            
        

