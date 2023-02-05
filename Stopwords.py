import spacy
import nltk
from nltk.corpus import stopwords
import os


# creaating a list of stop words from nltk and spacy. Add new stopwords here
def all_stop_words():
    try: # try to get stop words from nltk if not download them
        stop_words = stopwords.words('english')
    except LookupError:
        print('Downloading nltk stop words, try running again')
        nltk.download('stopwords')
        stop_words = stopwords.words('english')

    try: # try to get stop words from spacy if not download them
        en_model = spacy.load('en_core_web_sm')
    except OSError:
        print('Downloading spacy en model, try running again')
        os.system('python -m spacy download en_core_web_sm')
        en_model = spacy.load('en_core_web_sm')
    spacy_stopwords = en_model.Defaults.stop_words
    stop_words.append(spacy_stopwords)

    stop_words.append('(')
    stop_words.append(')')
    stop_words.append('[')
    stop_words.append('2')
    stop_words.append(']')
    stop_words.append('{')
    stop_words.append('}')
    stop_words.append(':')
    stop_words.append(';')
    stop_words.append('à')
    stop_words.append('%')
    stop_words.append('!')
    stop_words.append('?')
    stop_words.append('\'')
    stop_words.append('\"')
    stop_words.append('``')
    stop_words.append('...')
    stop_words.append('’')
    stop_words.append('“')
    stop_words.append('”')
    stop_words.append('–')
    stop_words.append(',')
    stop_words.append('.')
    stop_words.append('\'s')
    stop_words.append('\'\'')

    return stop_words