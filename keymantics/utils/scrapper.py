from urllib.request import urlopen
from bs4 import BeautifulSoup
from sklearn.externals import joblib
import pandas as pd
import numpy as np
from keymantics.utils.preproc import TweetTokeniser, preproc
import sys


import re
from unidecode import unidecode
import nltk
import string
from nltk.stem.snowball import FrenchStemmer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn import preprocessing
from sklearn.decomposition import TruncatedSVD


class TweetTokeniser(BaseEstimator, TransformerMixin):
    def __init__(self, stemming=False, field='description'):
        self.stemming = stemming
        self.stemmer = FrenchStemmer()
        self.field = field

    #         if self.stemming == True:
    #             self.stemmer = FrenchStemmer()
    #         else:
    #             self.stemmer = None

    def tokenize(self, content):
        if content is None:
            return None
        else:
            # remove http links
            content = re.sub(r'http\S+', '', content)
            # remove formatting
            content = re.sub("\s+", " ", content)
            # convert to lower case
            content = content.lower()
            # Remove accent
            content = unidecode(content)
            # Remove number
            content = re.sub("[0-9]\w+", "", content)
            # remove punctuation (preserving intra-word dashes)
            punct = string.punctuation.replace("-", "")
            regex = re.compile('[%s]' % re.escape(punct))
            content = regex.sub(' ', content)

            # remove extra white space
            content = re.sub(" +", " ", content)
            # remove leading and trailing white space
            content = content.strip()
            # tokenize
            tokens = content.split(" ")
            # remove stopwords
            stpwds = nltk.corpus.stopwords.words("french")
            others = set(['le', 'les', 'la', 'etait'])
            _ = [stpwds.append(i) for i in others if i not in stpwds]
            tokens = [token for token in tokens if token not in stpwds and len(token) > 2]
            if self.stemming == True:
                tokens = [self.stemmer.stem(t) for t in tokens]
            return tokens

    def fit(self, X, y=None):
        pass
        return self

    def transform(self, X, y=None):
        tokens = []
        if self.field == 'title':
            l = X.title
        else:
            l = X.description
        if isinstance(l, str):
            l = [l]
        for txt in l:
            tokens.append(self.tokenize(txt))
        join_tokens = [" ".join(i) for i in tokens]
        return join_tokens


# turn sparse array to array
class preproc(BaseEstimator, TransformerMixin):
    def __init__(self, normalize=False, dim_reduc=None,k=0.5):
        self.normalize = normalize
        self.dim_reduc = dim_reduc
        self.k = k

    def transform(self, X):
        if self.normalize:
            X = self.scaler.transform(X)
        if self.dim_reduc=='svd':
            X = self.svd.transform(X)
        elif self.dim_reduc=='lsi':
            pass

        return X.toarray()

    def fit(self, X, y=None):
        if self.normalize:
            # Normalization
            self.scaler = preprocessing.StandardScaler().fit(X)
        if self.dim_reduc=='svd':
            n_components = round(X.shape[1]*self.k)
            self.svd = TruncatedSVD(n_components=n_components).fit(X)
        if self.dim_reduc=='lsi':
            pass
        return self


class Scrapper(object):
    def __init__(self):
        self.clf_type = None
        self.clf_product = None
        self.types = {0:'Fiche Technique', 1:'Comparatif'}
        self.products = {0:'Smartphone', 1: 'Automobile'}

    def extract_url(self, url):
        try:
            resp = urlopen(url)
            soup = BeautifulSoup(resp.read(), 'html.parser')
        except Exception as e:
            print(url)
            print(e)
            soup = None

        if soup is not None:
            title = soup.title
            descr = None
            i = 0
            metas = soup.findAll('meta')
            while descr is None and i < len(metas):
                m = metas[i]
                if 'name' in m.attrs and 'description' in m.attrs['name']:
                    descr = m.attrs['content']
                elif 'property' in m.attrs and 'description' in m.attrs['property']:
                    descr = m.attrs['content']
                i += 1
            if title is None or descr is None or title == '' or descr == '':
                res = None
            else:
                res = {
                    'title': title.string,
                    'description': descr,
                }
        else:
            res = None
        return res

    def load_clf(self):
        # t = TweetTokeniser()
        # p = preproc()
        # TweetTokeniser.__module__ = 'preproc'
        # preproc.__module__ = 'preproc'
        setattr(sys.modules['__main__'], 'TweetTokeniser', TweetTokeniser)
        setattr(sys.modules['__main__'], 'preproc', preproc)
        self.clf_type = joblib.load('keymantics/utils/clf_type.pkl')
        self.clf_product = joblib.load('keymantics/utils/clf_product2.pkl')
        return True

    def predict(self, url):
        res = self.extract_url(url)
        if res is None:
            return None
        else:
            data = pd.Series(res)
            if self.clf_type is None or self.clf_product is None:
                _ = self.load_clf()
            y = self.clf_type.predict_proba(data)
            ind = np.argmax(y)
            type = {
                'value': self.types[ind],
                'proba': y[0][ind]
            }
            y = self.clf_product.predict_proba(data)
            ind = np.argmax(y)
            product = {
                'value': self.products[ind],
                'proba': y[0][ind]
            }
            return type, product


