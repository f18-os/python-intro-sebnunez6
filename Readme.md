This repository contains the code for the python introduction lab. The
purpose is to have a fairly simple python assignment that introduces
the basic features and tools of python

In the repository are two plain text files with lots of words. Your
assignment is to create a python 2 program which:
* takes as input the name of an input file and output file
* example

`$ python wordCount.py input.txt output.txt`
* keeps track of the total the number of times each word occurs in the text file 
* excluding white space and punctuation
* is case-insensitive
* print out to the output file (overwriting if it exists) the list of
  words sorted in descending order with their respective totals
  separated by a space, one word per line

To test your program we provide wordCountTest.py and two key
files. This test program takes your output file and notes any
differences with the key file. An example use is:

`$ python wordCountTest.py declaration.txt myOutput.txt declarationKey.txt`

The re regular expression library and python dictionaries should be
used in your program. 

Note that there are two major dialects of Python.  Python 3.0 is
incompatible with 2.7.   As a result, Python 2.7 remains popular.  All
of our examples are in 2.7.  We (mildly) encourage students to use 2.7
for their assignments. 

###Student Portion
wordCount.py utilizes a dictionary to keep track of each word in the input file.
If the word is already present in the dictionary the value containing the repetitions
is updated. Otherwise the word is added to the dictionary and it's value is set to one
for the first appearance. One the file has been completely added the dictionary is
sorted into a list. It is then used to output into the output file provided. The
sorted list is used to access the values of the dictionary in alphabetical order.
File path and system argv manipulation was received from Dr. Freudenthal's code

Inside the shell folder is a executable python script for a shell. The shell utilizes python3
Code was partially received from Dr. Freudenthal 's os demos and the concept of using dup2 was discussed 
with the IA Edward Seymour. 
