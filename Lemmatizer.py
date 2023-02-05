import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import pos_tag


# finds pos tag of the words in a sentence
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


# lemmatizes a sentence
def lemmatize_sentence(sentence):
    try:
        lemmatizer = WordNetLemmatizer()
    except LookupError: # if not present download the resource
        print("NLTK resource not present. Downloading wordnet...")
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    try:
        # tag each word in the sentence with its part of speech
        pos_tagged_sentence = pos_tag(nltk.word_tokenize(sentence))
    except LookupError: # if not present download the resource
        print("NLTK resource not present. Downloading averaged_perceptron_tagger...")
        nltk.download('averaged_perceptron_tagger')
        pos_tagged_sentence = pos_tag(nltk.word_tokenize(sentence))

    for word, tag in pos_tagged_sentence:
        wordnet_pos = get_wordnet_pos(tag) or wordnet.NOUN
        # lemmatize the word based on POS tag
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos=wordnet_pos))
    return lemmatized_sentence


# lemmatizes a text present in a file
def lemmatize_text(text):
    lemmatized_text = []
    for sentence in nltk.sent_tokenize(text):
        lemmatized_text.append(lemmatize_sentence(sentence))
    return lemmatized_text


if __name__ == "__main__":
    text = "The striped bats are hanging on their feet for best"
    print(lemmatize_text(text))
