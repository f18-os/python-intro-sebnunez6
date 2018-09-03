#! /usr/bin/env python3

import sys        # command line arguments
import os         # checking if file exists


# set input and output files
if len(sys.argv) is not 3:
    print("Correct usage: wordCountTest.py <input text file> <output file>")
    exit()

textFile = sys.argv[1]
outputFile = sys.argv[2]

if not os.path.exists(textFile):
    print ("text file input %s doesn't exist! Exiting" % textFile)
    exit()

wordTracker = {}
fo = open(textFile, "r")
str = fo.read()
list = str.split()
for word in list:
	resultingword = word.lower().replace(".","").replace(",","").replace(";","").replace(":","")
	if(wordTracker.has_key(resultingword))
		

