import random
from listener.models import Tweet as TweetModel

class Predictor():
    def __init__(self):
        self.tweet = None

    def sentiment_predict(self, tweet):
        s = [TweetModel.SENTIMENTS[i] for i in ['POSITIVE','NEGATIVE','NEUTRAL']]
        pred = random.choice(s)
        tweet.sentiment_predicted = pred
        tweet.save()
        return pred

    def predict_tweet(self,tweet):
        try:
            self.tweet.sentiment_predicted = self.sentiment_predict(tweet)
            return True
        except:
            return False

    def predict_next(self):
        tweet = TweetModel.objects.filter(sentiment_predicted=None).first()  # by id
        return self.predict_tweet(tweet)

