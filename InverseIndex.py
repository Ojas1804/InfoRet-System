
import os
from Stopwords import all_stop_words
import re
from Lemmatizer import lemmatize_text


# class for inverse index
class InverseIndex:
    def __init__(self):
        self.index = {}
        self.file_index = {}
        self.stop_words = all_stop_words()


    def no_number_preprocessor(tokens):
        r = re.sub('(\d)+', '', tokens.lower())
        return r


    # creates  inverse index
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
                    if token in self.index:
                        self.index[token].append(file_index)
                    else:
                        self.index[token] = [file_index]


    # creating inverse index for each file in dataset
    def addDirectory(self, dirname='Dataset'):
        i = int(1)
        for filename in os.listdir(dirname):
            self.file_index[filename] = i
            self.addFile(dirname + '/' + filename, i)
            i += 1


    # returns the posting list for a word
    def lookup(self, word):
        if word in self.index:
            return self.index[word]
        else:
            return []


    def __str__(self):
        return str(self.index)


    # saves posting lists to a file
    def store_posting_list(self, filename):
        f = open(filename, 'w')
        f.write(str(self.index))
        f.close()


    # creates posting list if it does not exist or is empty
    # else loads the posting list from the file
    def get_posting_list(self):
        exist = os.path.exists("Indexes/inverted_index.txt")
        if exist:
            if os.stat("Indexes/inverted_index.txt").st_size != 0: # check if file is not empty
                file = open('Indexes/inverted_index.txt',mode='r')
                text = str(file.read())
                file.close()
                dictionary = eval(text)
                self.index = dictionary
        else:
            self.create_posting_list()


    # creates posting list
    def create_posting_list(self, filename='Indexes/inverted_index.txt'):
        self.addDirectory()
        for key, value in self.index.items():
            self.index[key] = list(set(value))
        self.store_posting_list(filename)




# main funtion to test the class
if __name__ == '__main__':
    index = InverseIndex()
    index.create_posting_list()
    for key, value in index.index.items() :
        print (key, value)