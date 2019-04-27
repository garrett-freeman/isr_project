# isr_project

This was a project for my information storage and retrieval course. We were assigned to create a program that:
* scrapes a website
* Creates a new folders with all documents in the website
* Creates tokens of all words and a bigram index of all words
* Allows a user to search a term and find the location of the term in the docs

The scarper.py program will scrape a website and creates the documents to be scanned through and tokenized. The parser.py program allows the user to creates the tokens, bigram index, and an index containing each word, its frequency, and location. Once those have been created then it allows the user to search a term, if the term is mispelled it will offer some suggestions using the jaccard coefficient to determine whaat terms might be best. Otherwise it allowed the user to find the location of a specified term.
