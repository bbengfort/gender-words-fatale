How Language Reflects Gender- An Analysis
=========================================

An implementation of [Neal Caren's Gender analysis of the New York Times](http://nbviewer.ipython.org/5105037).

After this post went viral, I thought I'd do a quick knock up of my own Python code to check it
out. Neal gives most of his code on the website, but I generally take a more class based approach
to things, and I have my own style of attempting to create modular components for NLP tasks - for
instance, I leave it to tokenizers to do their own thing. 

Currently this is just a quick 10 min knock up-- not too robust, but interesting enough. I've also
uploaded Arthur Conan Doyle's *The Adventures of Sherlock Holmes* if you simply download both files
and run the script, it will spit out the counts of each sentence's gender. 

Otherwise, use the script as follows:

    from gender import GenderParser

    parser = GenderParser('/path/to/text/file.txt')
    parser.parse()
   
    counts = parser.counters
    
    sentence_genders = counts.sents
    word_genders     = counts.words
    word_frequency   = counts.wfreq
    proper_nouns     = counts.wcase
