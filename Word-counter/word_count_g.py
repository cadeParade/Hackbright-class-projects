from sys import argv
script, filename = argv
import re
import string

# open file and return as a string we can work with
f = open(filename)
text = f.read()
f.close()

lower_text = text.lower() 

lower_text = re.sub('[!_.,?""''\];:\'\-\()--]', ' ', lower_text)
#print lower_text

list_of_strings = lower_text.split()
#print list_of_strings
# for string in list_of_strings:
	# string.strip()

# build empty dictionary for key:word, value:occurances
word_dict = {}

# initialize key values to 0
key_val = 0

# read each word 
for item in list_of_strings:
	word_dict[item] = word_dict.get(item, 0) + 1
	# word_dict.setdefault(item, key_val) 
	# value = word_dict[item]
	# word_dict[item] = value + 1

#print key and values- not sorted 
#for key, value in word_dict.iteritems():
 #       print "key = %r value = %r" % (key, value)

#prints key and value but sorted by the value 
#for item in sorted(word_dict, key=word_dict.get, reverse=True):
#	print item, word_dict[item]


#Sorts words having the same frequency alphabetically.
list_of_tuples = word_dict.items()

#sorts by value
second_list_of_tuples = sorted(list_of_tuples, 
							   key=lambda word_dict : word_dict[0], 
							   reverse=False )
#sorts by key
final_sorted_list_of_tuples =sorted(second_list_of_tuples, 
									key=lambda second_list_of_tuples: 
									second_list_of_tuples[1] )

print final_sorted_list_of_tuples