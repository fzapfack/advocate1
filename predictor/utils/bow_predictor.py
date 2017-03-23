import nltk
import re
import string
from unidecode import unidecode
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from django.db.models import Q
from django.db.models import F
from listener.models import Tweet
from hello.models import Region
from hello.utils.carte_fr import Map

nltk.data.path.append('predictor/data/nltk')

class BowPredictor:
    predictor = None

    def __init__(self):
        self.stpwds = nltk.corpus.stopwords.words("french")
        self.vectorizer = None
        self.tfidf = None
        self.clf = None
        self.train_id = None
        self.test_id = None


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
            tokens = [token for token in tokens if token not in stpwds and len(token) > 2]
            return tokens

    # def replace_subject(txt, sign='XXXX'):
    #     clean = txt
    #     clean = re.sub('[#@][mM][aA][cC][rR][oO][nN]\w*', sign, clean)
    #     clean = re.sub('[mM][aA][cC][rR][oO][nN]\w*', sign, clean)
    #     return clean

    # def tweet_to_token(self, tweet, replace_subject=True):
    #     txt = tweet.txt
    #     if replace_subject:
    #         txt = self.replace_subject(txt, sign='XXXX')
    #     tokens = self.tokenize(txt)
    #     return tokens

    def train(self, update_predictor=True):
        labelled = Tweet.objects.filter(~Q(sentiment_label=None))
        tokens = []
        y_train = []
        for l in labelled:
            tokens.append(self.tokenize(l.txt))
            y_train.append(l.sentiment_label)
            l.training_tweet = True
            l.save()

        voc = list(set([i for sublist in tokens if sublist is not None for i in sublist]))
        self.vectorizer = CountVectorizer(vocabulary=voc, ngram_range=(1,2))
        join_tokens = [" ".join(i) for i in tokens]
        dtm = self.vectorizer.fit_transform(join_tokens)
        self.tfidf = TfidfTransformer(use_idf=True, smooth_idf=True).fit(dtm)
        X_train = self.tfidf.transform(dtm)
        self.clf = LogisticRegression(class_weight='balanced', fit_intercept=False, C=10).fit(X_train, y_train)
        if update_predictor:
            BowPredictor.predictor = self
        return True

    def predict_tweet(self, tweet):
        tokens = self.tokenize(tweet.txt)
        join_tokens = " ".join(tokens)
        vect = self.vectorizer.transform([join_tokens])
        x_pred = self.tfidf.transform(vect)
        pred = self.clf.predict(x_pred)
        pred = pred[0]
        return pred

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