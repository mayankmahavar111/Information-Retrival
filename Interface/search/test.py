import operator

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer ,WordNetLemmatizer

stop = set(stopwords.words('english'))
stemmer = PorterStemmer()
lemma = WordNetLemmatizer()

"""
x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
sorted_x = sorted(x.items(), key=operator.itemgetter(1),reverse=True)
print sorted_x
"""


def preprocess(que):
    tokens=word_tokenize(que)
    print tokens
    temp = []
    for token in tokens:
        if token.isalpha() == True and token  not in stop:
            temp.append(stemmer.stem(token.lower()))
    query = " ".join(temp)
    return query

query="my name is mayank"
print preprocess(query)