from Lemmatizer import lemmatize_text
import os
from Stopwords import all_stop_words

class PositionalIndex:
    def __init__(self):
        self.doc_id = 0
        self.index = {}
        self.file_index = {}
        self.stop_words = all_stop_words()

    def add(self, token, doc_id, offset):
        self.index[token].append((doc_id, offset))

    def addFile(self, filename, file_index):
        # read file and get the text
        f = open(filename, 'r')
        text = f.read()
        text = text.lower()
        f.close()

        # lemmatize and tokenize text
        tokenized_sentences = lemmatize_text(text)
        token_by_sentence = text.split('.')
        for token in token_by_sentence:
            if(token==''):
                token_by_sentence.remove(token)
        token_by_para = text.split('\n')
        for token in token_by_para:
            if(token==''):
                token_by_para.remove(token)


        # creating the index
        i = int(1)
        for tokens in tokenized_sentences:
            file_indexes = []
            for token in tokens:
                if token not in self.stop_words:
                    if token in self.index:
                        self.index[token][0] += 1
                        if file_index in self.index[token][1]:
                            self.index[token][1][file_index].append(i)
                        else:
                            self.index[token][1][file_index] = [i]
                    else:
                        # print(f"token: {token}  and  file_index: {file_index}")
                        self.index[token] = [1, {}]
                        """The first element of the list tells the number of documents in which 
                        the word is present. The second element stores the document id and the
                        position of the word in the document. The third element stores the
                        sentence number in which the word is present. The fourth element stores
                        the paragraph number in which the word is present."""
                        self.index[token][1][file_index] = [i]   # position in the document
            i += 1


    # creating inverse index for each file in dataset
    def addDirectory(self, dirname='Dataset'):
        i = int(1)
        for filename in os.listdir(dirname):
            self.file_index[filename] = i
            self.addFile(dirname + '/' + filename, i)
            i += 1


    # saves posting lists to a file
    def store_posting_list(self, filename):
        f = open(filename, 'w')
        f.write(str(self.index))
        f.close()


    # creates posting list if it does not exist or is empty
    # else loads the posting list from the file
    def get_posting_list(self):
        exist = os.path.exists("Indexes/positional_index.txt")
        print(exist)
        if exist:
            if os.stat("Indexes/positional_index.txt").st_size != 0: # check if file is not empty
                file = open('Indexes/positional_index.txt',mode='r')
                text = str(file.read())
                file.close()
                dictionary = eval(text)
                self.index = dictionary
        else:
            self.create_posting_list()


    # creates posting list
    def create_posting_list(self, filename='Indexes/positional_index.txt'):
        self.addDirectory()
        print(self.index)
        self.store_posting_list(filename)


    def lookup(self, token):
        return self.index[token]

    def __str__(self):
        return str(self.index)

if __name__ == '__main__':
    p = PositionalIndex()
    p.get_posting_list()
    print(p)