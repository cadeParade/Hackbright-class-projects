from sys import argv

script, filename = argv

import string

import timeit


a = string.lowercase

countlist = [0]*26
#print countlist

def count_function(filename):

	ftext = open(filename).read()
	lowertext = ftext.lower()
	
	for letter in lowertext:
		if letter in a:
			current_order = ord(letter)
			normalized_ord = current_order-97
			countlist[normalized_ord] += 1
		else:
			continue
	return countlist

	
count_function(filename)

counts = str(countlist).strip('[]')

print counts