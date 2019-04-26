import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import os
from csv import writer
import re
import json   

all_tokens = []
all_words = []
stoplist = list(stopwords.words('english'))
path = os.getcwd() + '/docs' 
file_list = os.listdir(path)

def tokenize():

    print("Tokenizing...")

    os.chdir(path)
    file_list = os.listdir(path)

    for filename in file_list:

        l = open(filename, 'r')
        contents = l.read()

        reg = re.compile('[^a-zA-Z]')
        contents = reg.sub(' ', contents)
        contents = contents.lower()

        token = nltk.word_tokenize(contents)
        
        for item in token:
            if item not in all_tokens:

                all_tokens.append(item)

            all_words.append(item)
    
    os.chdir('../') # goes back to previous directory 

    t = open("tokens.txt", "a")

    for item in all_tokens:
        data = item + "\n"
        t.write(data)

    t.close()

    print("Tokens written to 'tokens.txt'")

    f = open("all_words.txt", "w")

    for word in all_words:
        word = word + '\n'
        f.write(word)

def indexing_terms():

    print('Indexing...')   

    all_file_names = os.listdir(path)
    
    data = create_index(all_file_names) 

    print(data)
  
    with open('data.txt', 'w') as outfile:

        json.dump(data, outfile)
    
    os.remove("all_words.txt") 
    
def bigram_index():
    print("Creating bigram index...")

    bigram_index = {}
    bigram_list = []

    tokens = open('tokens.txt', 'r')

    for word in tokens:

        word = word.strip()
        word = '$' + word 
        word = list(word)

        i = 0
        while i != len(word):

            if i != len(word) - 1:
                bigram = word[i] + word[i+1]
                all_words = getAll(bigram)
                bigram_index[bigram] = {'words': all_words}
                
            else:  
                bigram = word[i] + word[0]
                all_words = getAll(bigram)
                bigram_index[bigram] = {'words': all_words}
            
            i += 1      

    with open('bigram_index.txt', 'w') as outfile:

        json.dump(bigram_index, outfile, indent=4)

def search(target):

    with open('data.txt', 'r') as json_file:
        data = json.load(json_file)

    if target in stoplist:
        print("Error: search item is too vague. Please be more specific.")
        main()

    elif target in data:
        print(data[target]["location"])

    else:
        word = '$' + target 
        word = list(word)
        bigram_list = []
        correction = []

        i = 0
        while i != len(word):

            if i != len(word) - 1:
                bigram = word[i] + word[i+1]
                bigram_list.append(bigram)
            else:  
                bigram = word[i] + word[0]
                bigram_list.append(bigram)

            i += 1      
            
            for bigram in bigram_list:
                
                with open('bigram_index.txt', 'r') as json_bigram:
                    bigrams = json.load(json_bigram)

                count = 0
                if bigram in bigrams:
                    for item in bigrams[bigram]['words']:
                        
                        if count == 8:
                            break

                        elif word in stoplist:
                            print("Search is too vague, please try another word.")
                            main()

                        else:
                            
                            if nltk.jaccard_distance(set(word), set(item)) < .6:
                                if word not in stoplist:
                                    correction.append(item)
                            
                            count += 1  

                        #print(bigrams[bigram]['words'])
            
            print("Invalid word. Did you mean: " + ", ".join(correction))
            main()

    task = input('Search another term (y/n)? ') 
    task = task.lower()

    if task == 'y':
        main()

    else:
        print('Goodbye.')



def getAll(target):

    f = open('tokens.txt', 'r')
    word_list = []

    if target.startswith('$') == True:
        for word in f:
            word = word.strip()
            if word.startswith(target[1]):
                word_list.append(word)
            
    elif target.endswith('$') == True:
        for word in f:
            word = word.strip()
            if word.endswith(target[0]) == True:
                word_list.append(word)
    else:
        for word in f:
            word = word.strip()
            if target in word:
                word_list.append(word)
    
    return word_list

def term_locations(term): # finds the location of each term for indexing

    location_list = []

    if '/docs' not in os.getcwd():

        os.chdir(path)

    for filename in file_list: # goes through each file to see if the term is in that file, if so, appends to location_list
        
        l = open(filename, 'r')

        contents = l.read()       
        
        if term in contents:

            location_list.append(filename)

    return location_list

def create_index(target):
    
    all_words = []
    all_tokens = []
    index_data = {}

    f = open('all_words.txt', 'r')

    for word in f:
        word = word.strip()
        all_words.append(word)

    f.close
    
    f = open('tokens.txt', 'r')

    for word in f:   
        word = word.strip()
        all_tokens.append(word)

    f.close()

    for item in all_tokens: 
        frequency = 0

        # Shows progress
        print(item)

        location_list = term_locations(item)

        frequency = all_words.count(item)

        index_data[item] = {'frequency': frequency, 'location': location_list}

    os.chdir('../')

    return index_data

def main():

    #tokenize()

    #indexing_terms()

    #bigram_index()

    term = input("Search: ")
    term = term.lower()
    search(term)
    
main()