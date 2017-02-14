from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from django.conf import settings
from listener.models import Tweet
from geopy.geocoders import Nominatim # to remove

# from time import gmtime, strftime
# import time


class Listener(StreamListener):

    def on_data(self, data): #on_data
        decoded = json.loads(data)
        user_lang = decoded['user']['lang']
        lang = decoded['lang']
        if ~bool(lang):
            if ~bool(user_lang):
                lang = 'NULL'
            else:
                lang = user_lang

        txt = str(decoded['text'])
        user_id = None
        if 'user' in decoded and decoded['user'] is not None:
            user_id = decoded['user']['id_str']
        retweet = None
        retweet_twitter_id = None
        if 'retweeted_status' in decoded and decoded['retweeted_status'] is not None:
            retweet = str(decoded['retweeted_status']['text'])
            retweet_twitter_id = decoded['retweeted_status']['id_str']

        d = {}
        d['txt'] = txt
        d['retweet'] = retweet
        d['twitter_id'] = decoded['id_str']
        d['retweet_twitter_id'] = retweet_twitter_id
        d['usr_twitter_id'] = user_id
        d['usr_place'] = str(decoded['user']['location'])
        d['lang'] = lang

        _ = Tweet.objects.create_tweet(d)
        return(True)

    def on_error(self, status_code):
        print (status_code)
        if (status_code == 420):
            return False

class Twitter_stream():
    def __init__(self, credentials):
        self.listener = Listener()
        self.credentials = credentials
        self.auth = None

    def authentificate(self):
        self.auth = OAuthHandler(self.credentials['ckey'], self.credentials['csecret'])
        self.auth.set_access_token(self.credentials['atoken'], self.credentials['asecret'])

    def start_stream(self, tracks):
        twitterStream = Stream(self.auth, self.listener)
        twitterStream.filter(track=tracks)


def start_listening(keywords):
    stream = Twitter_stream(settings.TWITTER_CREDENTIALS)
    stream.authentificate()
    stream.start_stream(keywords)

    # while True:
    #     print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    #     print('work')
    #     time.sleep(10)