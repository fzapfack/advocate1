from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from django.conf import settings
from listener.models import Tweet
from geopy.geocoders import Nominatim
from time import gmtime, strftime
import time

class Listener(StreamListener):

    def on_data(self, data): #on_data
        # decoded['truncated'],
        # decoded['coordinates'])
        # decoded['user']['screen_name'],
        # decoded['user']['name'],
        # favorite_count number of likes
        decoded = json.loads(data)
        user_lang = decoded['user']['lang']
        replied_to = decoded['in_reply_to_status_id']
        if replied_to is None:
            replied_to = 0
        else:
            replied_to = int(replied_to)
        lang = decoded['lang']
        if lang is None:
            if user_lang is None:
                lang = 'NULL'
            else:
                lang = str(user_lang)
        place = decoded['place']
        if place is None:
            place = str('NULL')

        txt = str(decoded['text'])
        user_id = decoded['user']['id']
        if user_id is None:
            user_id = -1
        else:
            user_id = int(user_id)
        coord = decoded['coordinates']
        if coord is not None and coord["type"]=="Point":
            coordinates = ', '.join(coord['coordinates'])
            geolocator = Nominatim()
            location = geolocator.reverse(coordinates)
        else:
            coordinates = ''
        retweet = None
        if 'retweeted_status' in decoded and decoded['retweeted_status'] is not None:
            retweet = str(decoded['retweeted_status']['text'])

        d = {}
        d['txt'] = txt
        d['usr_twitter_id'] = user_id
        d['replied_to'] = replied_to
        d['lang'] = lang
        d['replied_to'] = replied_to
        d['place'] = place
        d['coordinates'] = str(decoded['coordinates'])
        d['usr_place'] = str(decoded['user']['location'])
        d['retweet'] = retweet
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