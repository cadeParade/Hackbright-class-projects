#!/usr/bin/env python

import sys
from sys import argv
import random
import string

script, filename = argv


def make_chains(corpus):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""

    split_txt = corpus.split()

    markov_text = {}

    for i, word in enumerate(split_txt):

        if i < len(split_txt)-2:
            third_word = split_txt[i+2]
            current_tuple = (word, split_txt[i+1])

            if current_tuple in markov_text:
                markov_text[current_tuple].append(third_word)

            else:
                markov_text[current_tuple] = [third_word]

    return markov_text


def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""

    first_lookup = random.choice(chains.keys())
    
    first_value = chains[first_lookup][random.randint(0,len(chains[first_lookup])-1)]

    printout_list = [first_lookup[0], first_lookup[1], first_value]

    for i in range(0,50):
        lookup_tuple = (printout_list[i+1], printout_list[i+2])
        if lookup_tuple in chains:   
            printout_list.append(chains[lookup_tuple][random.randint(0,len(chains[lookup_tuple])-1)])
        else:
            backup_lookup = random.choice(chains.keys())
            backup_value = chains[backup_lookup][random.randint(0,len(chains[backup_lookup])-1)]
            printout_list.extend(backup_lookup, backup_value)
            # printout_list.append(backup_lookup[0])
            # printout_list.append(backup_lookup[1])
            # printout_list.append(backup_value)

    print printout_list
    print len(printout_list)

    return printout_list
    

def main():
    args = sys.argv


    text = open(filename)
    input_text = text.read()
    text.close()

    chain_dict = make_chains(input_text)

    random_text = make_text(chain_dict)

    string_random_text = string.join(random_text)

    print string_random_text


    

if __name__ == "__main__":
    main()

