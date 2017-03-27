import nltk
import re
import string
from unidecode import unidecode
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import preprocessing
from sklearn.decomposition import TruncatedSVD
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from django.db.models import Q
from django.db.models import F
from listener.models import Tweet
from hello.models import Region
from hello.utils.carte_fr import Map

nltk.data.path.append('predictor/data/nltk')


class TweetTokenizer(BaseEstimator, TransformerMixin):
    def __init__(self, rep_sub=True):
        self.rep_sub = rep_sub

    def tokenize(self, content):
        if content is None:
            return None
        else:
            # remove http links
            content = re.sub(r'http\S+', '', content)
            # remove pic
            content = re.sub(r'[^\s]*twitter.com[^\s]*', '', content)
            # remove formatting
            content = re.sub("\s+", " ", content)
            # convert to lower case
            content = content.lower()
            # Remove accent
            content = unidecode(content)
            # Remove number
            content = re.sub("[0-9]\w+", "", content)
            # remove punctuation (preserving intra-word dashes)
            # content = "".join(letter for letter in content if letter not in punct)
            punct = string.punctuation.replace("-", "")
            regex = re.compile('[%s]' % re.escape(punct))
            content = regex.sub(' ', content)
            #         content = re.sub("[^0-9a-zA-Z]", " ", content)
            # remove dashes attached to words but that are not intra-word
            #         content = re.sub("[^[:alnum:]['-]", " ", content)
            #         content = re.sub("[^[:alnum:][-']", " ", content)

            # remove extra white space
            content = re.sub(" +", " ", content)
            # remove leading and trailing white space
            content = content.strip()
            # tokenize
            tokens = content.split(" ")
            # remove stopwords
            stpwds = nltk.corpus.stopwords.words("french")
            others = ['le', 'les', 'la', 'etait', 'cette']
            _ = [stpwds.append(i) for i in others if i not in stpwds]
            tokens = [token for token in tokens if token not in stpwds and len(token) > 2]
            return tokens

    def replace_subject(self, txt, sign='XXXX'):
        clean = txt
        clean = re.sub('[#@][mM][aA][cC][rR][oO][nN]\w*', sign, clean)
        clean = re.sub('[mM][aA][cC][rR][oO][nN]\w*', sign, clean)
        return clean

    def fit(self, X, y=None):
        pass
        return self

    def transform(self, X, y=None):
        tokens = []
        l = X
        if isinstance(l, str):
            l = [l]
        for txt in l:
            #             txt = d.txt
            if self.rep_sub:
                txt = self.replace_subject(txt)
            tokens.append(self.tokenize(txt))
        join_tokens = [" ".join(i) for i in tokens]
        return join_tokens


class Preprocessor(BaseEstimator, TransformerMixin):

    def __init__(self, normalize=False, dim_reduc=None, k=0.5):
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


class BowPredictor:
    predictor = None

    def __init__(self):
        self.stpwds = nltk.corpus.stopwords.words("french")
        self.vectorizer = None
        self.tfidf = None
        self.clf = None
        self.train_id = None
        self.test_id = None

    def train(self, update_predictor=True):
        labelled = Tweet.objects.filter(~Q(sentiment_label=None) & Q(lang='fr') & ~Q(sentiment_label=2))
        tokens = []
        y_train = []
        for l in labelled:
            tokens.append(l.txt)
            y_train.append(l.sentiment_label)
            l.training_tweet = True
            l.save()

        self.clf = Pipeline([('tokenizer', TweetTokenizer()),
                         ('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('preproc', Preprocessor()),
                         ('clf', LogisticRegression(solver='lbfgs',
                                                    multi_class='multinomial'))
                         ])
        params = {'clf__C': 10,
                  'clf__class_weight': 'balanced',
                  'clf__fit_intercept': False,
                  'tfidf__smooth_idf': False,
                  'tfidf__use_idf': True,
                  'tokenizer__rep_sub': False,
                  'vect__ngram_range': (1, 2)
                  }
        self.clf.set_params(**params)
        self.clf.fit(tokens, y_train)

        print("\n\n >>>>results training dataset")
        y_pred = self.clf.predict(tokens)
        labels = list(set(y_train))
        print(classification_report(y_true=y_train, y_pred=y_pred, labels=labels,
                                    target_names=['neg', 'net', 'pos']))
        print("Accuracy: ", np.sum(np.array(y_train) == np.array(y_pred)) / len(np.array(y_train)))
        if update_predictor:
            BowPredictor.predictor = self
        return True

    def predict_tweet(self, tweet):
        y_pred = self.clf.predict(tweet.txt)
        if ~isinstance(y_pred, int):
            y_pred = int(y_pred[0])
        return y_pred

    @staticmethod
    def predict_tweet_static(tweet, predictor=None, save=True):
        if predictor is None:
            if BowPredictor.predictor is None:
                predictor = BowPredictor()
                predictor.train(update_predictor=True, use_idf=True, smooth_idf=True, sublinear_tf=False)
            else:
                predictor = BowPredictor.predictor

        y = predictor.predict_tweet(tweet)
        if save:
            tweet.sentiment_predicted = y
            tweet.save()
        return y

    @staticmethod
    def predict_all(new=True):
        if BowPredictor.predictor is None:
            predictor = BowPredictor()
            predictor.train(update_predictor=True, use_idf=True, smooth_idf=True, sublinear_tf=False)
        else:
            _ = BowPredictor.predictor
        if new:
            Y = [BowPredictor.predict_tweet_static(t) for t in Tweet.objects.filter(sentiment_predicted=None)]
        else:
            Y = [BowPredictor.predict_tweet_static(t) for t in Tweet.objects.all()]
        return Y

    @staticmethod
    def reset_predictions():
        for r in Region.objects.all():
            r.num_tweets_pos_pred = 0
            r.num_tweets_neg_pred = 0
            r.num_tweets_net_pred = 0
            r.save()
        m = Map()

        for t in Tweet.objects.all():
            t.added_map_pred = False
            t.save()

        clf = BowPredictor()
        clf.train(update_predictor=True)
        BowPredictor.predict_all()

        _ = m.add_all_tweets(labeled_data=False)

        return True
