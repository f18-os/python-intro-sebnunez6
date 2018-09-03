#! /usr/bin/env python3

import sys        # command line arguments
import os         # checking if file exists

# set input and output files
if len(sys.argv) is not 3:
    print("Correct usage: wordCountTest.py <input text file> <output file>")
    exit()

textFile = sys.argv[1]
outputFile = sys.argv[2]

#checking input file
if not os.path.exists(textFile):
    print ("text file input %s doesn't exist! Exiting" % textFile)
    exit()

#checking output file
if not os.path.exists(outputFile):
    print ("outfile input %s doesn't exist! Creating file" % textFile)

#creates dictionary
wordTracker = {}

#reads file
input = open(textFile, "r") 
str = input.read()

#holds file
list = str.split()

for word in list:
	#gets rid of any symbols associated with the word and makes the word all lowercase
	resultingword = word.lower().replace(".","").replace("\"","").replace(",","").replace(";","").replace(":","")
	
	#checks for compound words joined by - or '
	compoundword = resultingword.split("-")
	if not len(compoundword) > 1:
		compoundword = resultingword.split("'")
	for resultingword in compoundword:
		if resultingword in wordTracker:
			wordTracker[resultingword]+=1
		else:
			wordTracker.setdefault(resultingword,1)


sortedTracker = sorted(wordTracker)

#writes to file
output = open(outputFile,"w")
for word in sortedTracker:
	if word.isalpha():
 		output.write(word + " %s\n"%wordTracker[word])
output.close()
