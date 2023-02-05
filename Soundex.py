import re

class Soundex:
    def __init__(self):
        self.soundex = {}
        self.soundex['b'] = self.soundex['f'] = self.soundex['p'] = self.soundex['v'] = '1'
        self.soundex['c'] = self.soundex['g'] = self.soundex['j'] = self.soundex['k'] = self.soundex['q'] = self.soundex['s'] = self.soundex['x'] = self.soundex['z'] = '2'
        self.soundex['d'] = self.soundex['t'] = '3'
        self.soundex['l'] = '4'
        self.soundex['m'] = self.soundex['n'] = '5'
        self.soundex['r'] = '6'
        self.soundex['a'] = self.soundex['e'] = self.soundex['i'] = self.soundex['o'] = self.soundex['u'] = self.soundex['y'] = self.soundex['h'] = self.soundex['w'] = '0'
        self.soundex[' '] = ' '
        self.soundex['.'] = '.'

    def hasAlphaOnly(self, inputString):
        return re.search(r'^[a-zA-Z]+$', inputString)

    def getSoundex(self, word):
        word = word.lower()
        if not self.hasAlphaOnly(word):
            return word
        soundex = word[0]
        for i in range(1, len(word)):
            if self.soundex[word[i]] != self.soundex[word[i-1]]:
                soundex += self.soundex[word[i]]
        soundex = soundex.replace('0', '')
        soundex = soundex[:4].ljust(4, '0')
        return soundex