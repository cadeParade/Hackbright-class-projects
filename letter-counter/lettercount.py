import string

from sys import argv

script, filename = argv

def count_function(filename):

	ftext = open(filename).read()

	listtext = []

	for char in ftext:
		listtext.append(char)

	a = string.printable
	
	charcount = []

	for i in a:
		charcount.append(listtext.count(i))

	return str(charcount).strip('[]')

print count_function(filename)


#return table thing (fancy!)
