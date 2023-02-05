import re
import os
from Lemmatizer import lemmatize_text
from InverseIndex import InverseIndex
from Stopwords import all_stop_words


class BiwordIndex(InverseIndex):
    def __init__(self):
        self.index = {}
        self.file_index = {}
        self.file_to_int = {}
        self.stop_words = all_stop_words()

    def build_index(self, path):
        # stop_words = self.all_stop_words()
        # print('stop words: ', stop_words)
        for root, dirs, files in os.walk(path):
            i = int(1)
            for file in files:
                self.file_to_int[file] = i
                i += 1
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    text = text.lower()
                    text = re.sub(r'[^\w\s]', '', text)
                    text = re.sub(r'\d+', '', text)
                    text = re.sub(r'\s+', ' ', text)
                    text = text.strip()
                    text = lemmatize_text(text)
                    for _ in range(len(text)):
                        sentence = text.pop()
                        sentence = [word for word in sentence if word not in self.stop_words]
                        sentence = [word for word in sentence if word != '']
                        sentence = [word for word in sentence if len(word) > 1]
                        text.insert(0, sentence)

                    for sentence in text:
                        for i in range(len(sentence) - 1):
                            biword = sentence[i] + ' ' + sentence[i + 1]
                            if biword not in self.index:
                                self.index[biword] = [self.file_to_int[file]]
                            else:
                                self.index[biword].append(self.file_to_int[file])
                        self.file_index[file] = sentence
            for key, value in self.index.items():
                self.index[key] = list(set(value))
            self.store_posting_list('Indexes/biword_index.txt')


    def search(self, query):
        query = query.lower()
        query = re.sub(r'[^\w\s]', '', query)
        query = re.sub(r'\d+', '', query)
        query = re.sub(r'\s+', ' ', query)
        query = query.strip()
        query = lemmatize_text(query)
        query = [word for word in query if word != '']
        query = [word for word in query if len(word) > 1]
        result = []
        query = query[0]
        for i in range(len(query) - 1):
            biword = query[i] + ' ' + query[i + 1]
            if biword in self.index:
                result.append(self.index[biword])
        if len(result) == 0:
            return []
        elif len(result) == 1:
            return result[0]
        else:
            result = result[0]
            for i in range(1, len(result)):
                result = list(set(result) & set(result[i]))
        return result


    def get_posting_list(self, path="./Dataset"):
        exist = os.path.exists("Indexes/biword_index.txt")
        if exist:
            if os.stat("Indexes/biword_index.txt").st_size != 0:
                file = open('Indexes/biword_index.txt',mode='r')
                text = str(file.read())
                file.close()
                dictionary = eval(text)
                self.index = dictionary
        else:
            self.build_index(path)

    def get_file_index(self):
        return self.file_index

    def get_biword_file_count(self, biword):
        return len(self.index[biword])


if __name__=='__main__':
    biword_index = BiwordIndex()
    biword_index.get_posting_list('./Dataset')
    # print(biword_index.get_index())
    query = 'world war'
    result = biword_index.search(query)
    print(list(set(result)))