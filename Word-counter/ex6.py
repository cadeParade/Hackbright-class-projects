

# OBJECT OF PROGRAM
# count instances of each word in text file
# print a list of how many instances of each word are in text file

import string

from sys import argv

script, filename = argv

text_file = open(filename).readlines()
#print lowertext


#open file
#create empty dict
all_words_dict = {}

punct = string.printable[62:]

#for each line in file
def dictionary(filename):
	for line in text_file:
		current_line = line.lower()
	#	print line
		#split current line into list of words
		split_current_line = current_line.split(" ")
		
		#for each word in split line check dict if word key is already there
		for word in split_current_line:
			#if it is there, add 1 to word value
			
			strippedwords = word.strip(punct)

			if strippedwords in all_words_dict:
				all_words_dict[strippedwords] += 1
			else:
				all_words_dict[strippedwords] = 1
			#if it isn't there, add item to dict, make value 1

	return all_words_dict

dicttext = dictionary(filename)
  
for key, value in dicttext.iteritems():
	print key, value

#get rid of \r and \n and all special characters
#make everything lowercase. DONE!!!




