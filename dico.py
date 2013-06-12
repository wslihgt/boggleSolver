"""load dictionaries of words, modify to fit the required language
"""

import numpy as np
import unicodedata as ud

def rmdiacritics(char):
    '''
    Return the base character of char, by "removing" any
    diacritics like accents or curls and strokes and the like.
    '''
    desc = ud.name(unicode(char))
    cutoff = desc.find(' WITH ')
    if cutoff != -1:
        desc = desc[:cutoff]
    return ud.lookup(desc)

def strip_accents(s):
   return ''.join(c for c in ud.normalize('NFD', s)
                  if ud.category(c) != 'Mn')

def addWordToPrefix(prefix, word):
    currentdico = prefix
    # capword = [rmdiacritics(c).upper() for c in word]
    #capword = [strip_accents(c).upper() for c in word]
    capword = strip_accents(unicode(word, 'latin1')).upper()
    ##print word, capword
    for c in capword:
        if c not in currentdico:
            currentdico[c] = {}
        currentdico = currentdico[c]
    currentdico['EOW'] = None

# dicofilename = 'beep.txt' ## English
dicofilename = 'liste.de.mots.francais.frgut.txt'
txtfile = open(dicofilename)

lines = txtfile.readlines()
txtfile.close()

words = []
prefix = {}
for l in lines:
    word = l.strip().split('\t')[0]
    words.append(word)
    
    addWordToPrefix(prefix, word)

