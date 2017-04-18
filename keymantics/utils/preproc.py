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
