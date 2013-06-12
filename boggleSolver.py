"""a program to solve a boggle problem
"""

import numpy as np
import string
from dico import prefix, words

alphabet = np.array([l for l in string.ascii_uppercase])
alphabet_size = len(alphabet)

extendIncrement = []
for r in [-1, 0, 1]:
    for c in [-1, 0, 1]:
        extendIncrement.append([r,c])
extendIncrement.remove([0,0])

directions = {
    0: ' ',
    ( 1, 1): '\\', #'/',
    ( 1, 0): '|',
    ( 1,-1): '/',
    ( 0,-1): '-',
    (-1,-1): '\\',
    (-1, 0): '|',
    (-1, 1): '/',
    ( 0, 1): '-'
    }

def initArray(array, rows, cols, type='num'):
    if (not(isinstance(array, np.ndarray)) and
        not(isinstance(array, str)) and array is not None):
        print array
        raise TypeError("array must be a string or an ndarray")
    elif array is None: # redundant with 'else'
        random_draw = np.int32(np.random.rand(rows, cols)
                               * alphabet_size)
        if type == 'alpha':
            narray = alphabet[random_draw]
        else:
            narray = random_draw
    elif isinstance(array, str) and len(array) == rows * cols:
        array.upper()
        narray = np.array([l for l in array]).reshape(rows, cols)
        if type == 'num':
            narray = np.int32(narray)
        else:
            narray = np.array(
                [[elt.upper() for elt in row] for row in narray])
    elif array.shape == (rows, cols):
        narray = array
        if type=='num':
            narray = np.int32(narray)
        else:
            narray = np.array(
                [[elt.upper() for elt in row] for row in array])
    else: # letters is None or letters.shape != (rows, cols):
        random_draw = np.int32(np.random.rand(rows, cols)
                               * alphabet_size)
        if type == 'alpha':
            narray = alphabet[random_draw]
        else:
            narray = random_draw
        
    return narray

class LetterGrid(object):
    def __init__(self, letters='abcdefghijklmnop',
                 points=None,
                 bonus=None,
                 rows=4, cols=4):
        """initialize the grids, random if none provided
        """
        self.rows = rows
        self.cols = cols
        self.points = np.ones([rows, cols])
        self.bonus = np.ones([rows, cols])
        
        ##if (not(isinstance(letters, np.ndarray)) or
        ##    not(isinstance(letters, str))):
        ##elif len(letters) == rows * cols:
        ##    self.letters = np.array([l for l in letters]).reshape(rows, cols)
        ##elif letters.shape != (rows, cols):
        ##    self.letters = letters
        ##else: # letters is None or letters.shape != (rows, cols):
        ##    random_draw = np.int32(np.random.rand(rows, cols)
        ##                           * alphabet_size)
        ##    self.letters = alphabet[random_draw]
        self.letters = initArray(letters, rows=rows, cols=cols, type='alpha')
        if points is not None:
            self.points = initArray(points, rows=rows, cols=cols, type='num')
        if bonus is not None:
            self.bonus = initArray(bonus, rows=rows, cols=cols, type='num')

class Path(object):
    def __init__(self, letterGrid=None, sequence=[]):
        """a class aiming at providing wrapping operations
        around a path in the letterGrid, keeping track of
        the path, how it can be extended, whether it is valid,
        etc.
        """
        if isinstance(letterGrid, LetterGrid):
            self.letterGrid = letterGrid
        else:
            raise ValueError("raising error for now, lettergrid wrong")
        self.sequence = sequence
        currentPrefixDico = prefix
        for s in self.sequence:
            c = self.letterGrid.letters[s[0],s[1]]
            if c not in currentPrefixDico:
                raise ValueError(''.join([self.letterGrid.letters[s[0], s[1]]
                                          for s in self.sequence])
                                 + ' is not a valid word prefix')
            currentPrefixDico = currentPrefixDico[c]
        self.possibleLetters = currentPrefixDico
        if 'EOW' in self.possibleLetters:
            print ''.join([self.letterGrid.letters[s[0],s[1]]
                           for s in self.sequence]),
            print self.sequence
            self.isWord = True
        else:
            self.isWord = False

    def extend(self, ):
        """returns a list of Paths that are valid extensions of the
        instance path. 
        """
        extendedPaths = []
        for item in self.possibleExtendToItem():
            newSequence = list(self.sequence)
            newSequence.append(item)
            path = Path(letterGrid=self.letterGrid,
                        sequence=newSequence)
            extendedPaths.append(path)
            
        return extendedPaths

    def isValid(self):
        """check if this prefix exists in the dictionary
        """
        return False

    def possibleExtendToItem(self):
        """checks the last element of the path, and 
        """
        items = []
        if len(self.sequence):
            lastItem = self.sequence[-1]
        else:
            lastItem = [0,0] # np.argmax(self.letterGrid.bonus)
        for inc in extendIncrement:
            nextItem = [lastItem[0] + inc[0],
                        lastItem[1] + inc[1]]
            if (nextItem[0]>=0 and nextItem[0] < self.letterGrid.rows
                and nextItem[1]>=0 and nextItem[1] < self.letterGrid.cols
                and nextItem not in self.sequence
                and self.letterGrid.letters[nextItem[0], nextItem[1]] in
                self.possibleLetters):
                items.append(nextItem)
        return items
    
    def __string__(self):
        print self.word(), self.score()
        print self.onTheGrid()
    
    def word(self):
        return ''.join([self.letterGrid.letters[s[0], s[1]]
                       for s in self.sequence])

    def onTheGrid(self):
        """graphical representation of the path on the grid
        """
        stringPath = ''
        prefix = '        '
        nl, nc = self.letterGrid.letters.shape
        gridPath = np.zeros([2*nl-1, 2*nc-1])
        gridPath = [0,] * (2*nl-1)
        for row in range(2*nl-1):
            gridPath[row] = [0,] * (2*nc - 1)
        ##s = ('          X  X  X  X\n' +
        ##     '          X  X  X  X\n' +
        ##     '          X  X  X  X\n' +
        ##     '          X  X  X  X\n')
        
        
        for ns, s in enumerate(self.sequence):
            if ns!=0:
                gridPath[s[0]+self.sequence[ns-1][0]][
                    s[1]+self.sequence[ns-1][1]] = (
                    (s[0] - self.sequence[ns-1][0],
                     s[1] - self.sequence[ns-1][1])
                    )
            gridPath[2*s[0]][2*s[1]] = ns + 1
            
        # print gridPath
        
        for row in range(2 * nl - 1):
            stringPath += prefix
            if row%2:
                stringPath += ' ' + directions[gridPath[row][0]] + ' '
            else:
                stringPath += '%2d ' %gridPath[row][0]
            for col in range(1, nc):
                if row%2:
                    stringPath += ' ' + directions[gridPath[row][2*col-1]] + ' '
                    stringPath += ' ' + directions[gridPath[row][2*col]] + ' '
                else:
                    # stringPath += '   '
                    stringPath += ' ' + directions[gridPath[row][2*col-1]] + ' '
                    stringPath += '%2d ' %gridPath[row][2*col] 
            stringPath += '\n'
        
        return stringPath
    
    def score(self):
        """compute the score for the word
        """
        score = 0
        totMul = 1
        for s in self.sequence:
            score += self.letterGrid.points[s[0],s[1]]
            totMul *= self.letterGrid.bonus[s[0],s[1]]
        return score * totMul

class Ruzzle(object):
    def __init__(self, letters=None, bonus=None, points=None):
        self.letterGrid = LetterGrid(letters=letters,
                                     bonus=bonus,
                                     points=points,
                                     rows=4, cols=4)

    def listAllWords(self):
        """Take the letter Grid, compute all words and list them
        in order of 
        """
        # words can start from any place, start paths for each:
        
        pathList = []
        
        for r in range(self.letterGrid.rows):
            for c in range(self.letterGrid.cols):
                pathList.append(Path(self.letterGrid,
                                     sequence=[[r,c]]))
                
        words = []
        while(len(pathList)):
            paths = list(pathList)
            pathList = []
            for n, p in enumerate(paths):
                if p.isWord:
                    words.append(p)
                pathList.extend(p.extend())
                
        scores = [w.score() for w in words]
        sortIndex = np.argsort(scores)
        sortedWords = []
        for i in sortIndex:
            sortedWords.append(words[i])
            print words[i].word(), words[i].score()
            print words[i].onTheGrid()
            
        return sortedWords


##if __name__=='__main__':
##    import optparse
    
##    parser = optparse.Parser()
