from InverseIndex import InverseIndex
from Soundex import Soundex
from Lemmatizer import lemmatize_text
from Stopwords import all_stop_words
import os
from Query import Query


class SoundexIndex(InverseIndex):
    def __init__(self):
        # super.__init__()
        self.soundex = Soundex()
        self.index = {}
        self.stop_words = all_stop_words()
        self.file_index = {}


    def addFile(self, filename, file_index):
        # read file and get the text
        f = open(filename, 'r')
        text = f.read()
        text = text.lower()
        f.close()

        # lemmatize and tokenize text
        tokenized_sentences = lemmatize_text(text)

        # creating the index
        for tokens in tokenized_sentences:
            for token in tokens:
                if token not in self.stop_words:
                    soundex = self.soundex.getSoundex(token)
                    if soundex in self.index:
                        self.index[soundex].append(file_index)
                    else:
                        self.index[soundex] = [file_index]


    def get_posting_list(self):
        exist = os.path.exists("Indexes/soundex_index.txt")
        # print(exist)
        if exist:
            if os.stat("Indexes/soundex_index.txt").st_size != 0: # check if file is not empty
                file = open('Indexes/soundex_index.txt',mode='r')
                text = str(file.read())
                file.close()
                dictionary = eval(text)
                self.index = dictionary
        else:
            self.create_posting_list("Indexes/soundex_index.txt")

    def test_query(self, query):
        q = Query(query)
        self.get_posting_list()
        return q.soundex_query(self.index)


# test soundex index
if __name__ == "__main__":
    soundex_index = SoundexIndex()
    soundex_index.get_posting_list()
    print(soundex_index.index)
