#!/usr/bin/env python

import sys
from sys import argv
import random
import string

script, filename, length_of_key = argv


def make_chains(corpus, length_of_key):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""

    split_txt = corpus.split()

    length_of_key = int(length_of_key)

    markov_text = {}

    for i, word in enumerate(split_txt):

        if i < len(split_txt)-length_of_key-1:
            tuple_list = []
            for j in range(0,length_of_key):
                tuple_list.append(split_txt[i+j]) 
            #word is always the first item in tuple
            #make a tuple of length length_of_key
            #tuple needs to be (word, word+1, word+2,....word+length_of_key)
            current_value = split_txt[i+length_of_key+1]
            current_tuple = tuple(tuple_list)
            
            if current_tuple in markov_text:
                markov_text[current_tuple].append(current_value)

            else:
                markov_text[current_tuple] = [current_value]

    return markov_text


def make_text(chains, length_of_key):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""

    first_lookup = random.choice(chains.keys())
    
    length_of_key = int(length_of_key)

    first_value = chains[first_lookup][random.randint(0,len(chains[first_lookup])-1)]

    printout_list = []
    else_counter = 0

    for i in range(0, length_of_key):
        printout_list.append(first_lookup[i])

    printout_list.append(first_value)

    for i in range(0,50):
        lookup_tuple = (printout_list[i+1], printout_list[i+2])
        if lookup_tuple in chains:   
            printout_list.append(chains[lookup_tuple][random.randint(0,len(chains[lookup_tuple])-1)])
        else:
            else_counter += 1
            backup_lookup = random.choice(chains.keys())
            backup_value = chains[backup_lookup][random.randint(0,len(chains[backup_lookup])-1)]
            for j in range(0, length_of_key):
                printout_list.append(backup_lookup[j])

            printout_list.append(backup_value)

            #printout_list.extend(backup_lookup, backup_value)
            # printout_list.append(backup_lookup[0])
            # printout_list.append(backup_lookup[1])
            # printout_list.append(backup_value)

    #print printout_list
    #print len(printout_list)
    print else_counter, "else counter"
    return printout_list
    

def main():
    args = sys.argv


    text = open(filename)
    input_text = text.read()
    text.close()

    chain_dict = make_chains(input_text, length_of_key)

    random_text = make_text(chain_dict, length_of_key)

    string_random_text = string.join(random_text)

    print string_random_text


    

if __name__ == "__main__":
    main()

