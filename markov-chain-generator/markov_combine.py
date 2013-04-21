#!/usr/bin/env python

import sys
from sys import argv
import random
import string
import twitter

api = twitter.Api(consumer_key='zx9ZpF09r8fphXa6IbeoNQ', consumer_secret= 'wBMlkbUCBDdV1jdfRPt3RNlOTHj9vpHW8jHkwmiI10', access_token_key='1278820627-RnkDosijnJIXTplgvlbnErcvWuxSRLjQgZp9WdR', access_token_secret='ikeEmcIdhbmTi5fH6QJ2ZY2rn8enSLf3RR2wpmJXrzA')

script, filename, filename2, length_of_key = argv


def make_chains(corpus, length_of_key):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""

    split_txt = corpus.split()
    length_of_key = int(length_of_key)
    markov_text = {}
    capital_dict = {}

    for i, word in enumerate(split_txt):

        if i < len(split_txt)-length_of_key-1:
            tuple_list = []
            
            for j in range(0,length_of_key):
                tuple_list.append(split_txt[i+j]) 
          
            current_value = split_txt[i+length_of_key]
            current_tuple = tuple(tuple_list)
            
            if current_tuple in markov_text:
                markov_text[current_tuple].append(current_value)
                
                if current_tuple[0][0] in string.ascii_uppercase:
                    capital_dict[current_tuple] = [current_value]
            else:
                markov_text[current_tuple] = [current_value]


    return_list = [markov_text, capital_dict]
    return return_list

def make_text(chains, length_of_key, capital_dict):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""

    first_lookup = random.choice(capital_dict.keys())
    length_of_key = int(length_of_key)
    first_value = chains[first_lookup][random.randint(0,len(chains[first_lookup])-1)]
    printout_list = []

    #starts printout list with original words
    for i in range(0, length_of_key):
        printout_list.append(first_lookup[i])

    # adds first value to printout list
    printout_list.append(first_value)

    #make next key
    for i in range(0,8):
        lookup_tuple_list = []
      
        for j in range(0,length_of_key):
            lookup_tuple_list.append(printout_list[i+j+1])
       
        lookup_tuple = tuple(lookup_tuple_list)
        
        if lookup_tuple in chains:
            temp_value = chains[lookup_tuple][random.randint(0,len(chains[lookup_tuple])-1)]
            allowed_punctuation = ".?\""  
         
            if temp_value[-1] == "." or temp_value[-1] == "?" or temp_value[-1] == '"':
                printout_list.append(temp_value)
                break
           
            else:
                printout_list.append(temp_value)
        else:
            else_counter += 1
            backup_lookup = random.choice(capital_dict.keys())
            backup_value = chains[backup_lookup][random.randint(0,len(chains[backup_lookup])-1)]
           
            for j in range(0, length_of_key):
                printout_list.append(backup_lookup[j])

            printout_list.append(backup_value)

    return printout_list
    

def main():
    args = sys.argv

    text = open(filename)
    input_text = text.read()
    text.close()

    text2 = open(filename2)
    input_text2 = text2.read()
    text.close()

    both_dicts_text1 = make_chains(input_text, length_of_key)
    both_dicts_text2 = make_chains(input_text2, length_of_key)

    dict1 = both_dicts_text1[0]
    capital1= both_dicts_text1[1]

    dict2 = both_dicts_text2[0]
    capital2= both_dicts_text2[1]
   

    random_text = make_text(dict1, length_of_key, capital1)
    random_text2 = make_text(dict2, length_of_key, capital2)

    string_random_text = string.join(random_text)
    string_random_text2 = string.join(random_text2)

    total_string = string_random_text + " " + string_random_text2
    
    if len(total_string) < 140:
        api.PostUpdate(total_string)
        print "blah"
    else:
        print "Greater than 140"

    print string_random_text
    print string_random_text2

    

if __name__ == "__main__":
    main()

