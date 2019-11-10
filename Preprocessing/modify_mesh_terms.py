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
            
# dictionary with tree ID and count of values if less than 200 articles with the ID
lowTermDict = {meshTreeDict[i]:meshDict[i] for i in meshTreeDict if i in meshDict and meshDict[i] < 200}
 
i = 32
removedTreeIDs = []

while i >= 12:
    
    keysToRemove = []
    
    # add child node to parent (tree is 3 char + '.' per node)
    # track keys added to parent for removal
    for key in lowTermDict:
        if len(key) >= i:
            newKey = key[:-4]
            if treeMeshDict[newKey] in meshDict:    
                meshDict[treeMeshDict[newKey]] += lowTermDict[key]
            else:
                meshDict[treeMeshDict[newKey]] = lowTermDict[key]
            keysToRemove.append(key)
    
    # remove child keys from meshDict
    for item in keysToRemove:
        removedTreeIDs.append(item)
        del meshDict[treeMeshDict[item]]
        del lowTermDict[item]  # possibly redundant      
    
    lowTermDict = {meshTreeDict[i]:meshDict[i] for i in meshTreeDict if i in meshDict and meshDict[i] < 200}
    
    i -= 4 # move up tree one node


newTermDict = {meshTreeDict[i]:meshDict[i] for i in meshTreeDict if i in meshDict}

print(str(countArticles(meshDict)) + ' articles')

del newTermDict['C04'] # remove generic cancer articles
del meshDict[treeMeshDict['C04']]

print(str(countArticles(meshDict)) + ' articles after deleting \'C04\'')


# view keys in csv file and track possible removal

keysToRemove = []
possibleRemoval = []

for key in newTermDict:
    if newTermDict[key] < 200:
        possibleRemoval.append(key)
#        if len(key) < 8:
#            keysToRemove.append(key) # if not enough articles no further reduction
#        else:
#            possibleRemoval.append(key)

possibleRemoval.sort()

newTermList = list(newTermDict)
newTermList.sort()

possibleKeep = []

i = 0
for j in range(len(newTermList)):
    if possibleRemoval[i] == newTermList[j]:
        print(possibleRemoval[i])
        print(newTermList[j+1])
        if newTermList[j+1].startswith(str(possibleRemoval[i])):
            possibleKeep.append(possibleRemoval[i])
        i += 1
        if i >= len(possibleRemoval):
            break

for item in possibleRemoval:
    if item not in possibleKeep:
        del meshDict[treeMeshDict[item]]

with open('/home/kewilliams/Documents/CSC-450/changed_meshID.csv', 'w') as writeFile:
    for item in meshDict:
        writeFile.write(item + '\t' + meshTreeDict[item] + '\t' + meshTermDict[meshTreeDict[item]] + '\t' + str(meshDict[item]) + '\n')

with open('/home/kewilliams/Documents/CSC-450/possible_keep_treeIDs.txt', 'w') as writeFile:
    for item in possibleKeep:
        writeFile.write(item + '\n')


            
        

