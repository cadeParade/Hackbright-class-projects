from sys import argv

#open scores.txt
#save each line of scores.txt into list item
# make each list item into dict key and value (split by spaces??)
#print out sorted dict

script, filename = argv

restaurants_list = []

text_file = open(filename).readlines()

for i,item in enumerate(text_file):
#	print i, "This is i"
#	print item, "This is item"
	text_file[i] = item.strip("\n")

#text_file.split(":")
restaurant_dict = {}
for item in text_file:
	current_item = item.split(":")
#	print current_item
	restaurant_dict[current_item[0]] = current_item[1]

for item in sorted(restaurant_dict.iterkeys()):
	print item, restaurant_dict[item]

#print restaurant_dict

#for item in text_file:
	#do something.