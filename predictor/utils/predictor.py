import random
from listener.models import Tweet as TweetModel

class Predictor():
    # def __init__(self):
    #     self.tweet = None

    def sentiment_predict(self, tweet):
        s = TweetModel.POSITIVE,TweetModel.NEGATIVE,TweetModel.NEUTRAL
        return random.choice(s)

    def topic_predict(self, tweet):
        t = TweetModel.GENERAL,TweetModel.ECONOMY,TweetModel.SANTE,TweetModel.PS,TweetModel.LR,TweetModel.FN,TweetModel.EM
        topics = [str(random.choice(t)) for _ in range(random.randint(1,round(len(t)/2)))]
        return ','.join(topics)

    def predict_tweet(self,tweet):
        try:
            self.tweet.sentiment_predicted = self.sentiment_predict(self, tweet)
            self.tweet.topic_predicted = self.topic_predicted(self, tweet)
            return True
        except:
            return False

    def predict_next(self):
        tweet = TweetModel.objects.filter(sentiment_predicted=None).first()  # by id
        return self.predict_tweet(tweet)

