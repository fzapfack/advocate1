from watson_developer_cloud import AlchemyLanguageV1
from django.db.models import Q
from django.db.models import F
from listener.models import Tweet


class AlchemyPredictor:
    default_url = "https://gateway-a.watsonplatform.net/calls"
    default_api_key = 'XXXX'

    def __init__(self, url=default_url, api_key=default_api_key):
        self.url = url
        self.service = AlchemyLanguageV1(api_key=api_key)
        self.tweet = None

    def sentiment_predict(self, tweet):
        sentiments_code = {
            'positive': Tweet.SENTIMENTS['POSITIVE'],
            'negative': Tweet.SENTIMENTS['NEGATIVE'],
            'neutral': Tweet.SENTIMENTS['NEUTRAL'],
        }
        txt = tweet.txt
        res = self.service.sentiment(text=txt, language='french')
        if 'status' in res and res['status'] == 'OK':
            pred = res['docSentiment']['type']
            pred = sentiments_code[pred]
        else:
            pred = None
        return pred

    def predict_tweet(self, tweet):
        if tweet.sentiment_alchemy is not None:
            return tweet.sentiment_alchemy
        else:
            try:
                pred = self.sentiment_predict(tweet)
            except Exception as e:
                print(e)
                pred = None
            if pred is None:
                return Tweet.SENTIMENTS['UNKNOWN']
            else:
                tweet.sentiment_alchemy = pred
                tweet.save()
                return pred

    def predict_next(self):
        tweet = Tweet.objects.filter(sentiment_predicted=None).first()  # by id
        return self.predict_tweet(tweet)

    def test_all_labelled(self):
        labelled = Tweet.objects.filter(~Q(sentiment_label=None))
        for l in labelled:
            self.predict_tweet(l)
        return True

    def get_accuracy(self):
        labelled = Tweet.objects.filter(~Q(sentiment_label=None))
        ratio = float(labelled.filter(sentiment_label=F('sentiment_
        ')).count())/labelled.count()
        return labelled.count(), round(ratio*100)
