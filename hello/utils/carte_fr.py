import csv
from unidecode import unidecode
import json
import colorsys
# import numpy as np
from django.db.models import Q
from hello.models import Region
from listener.models import Tweet
# from hello.models import Departement,City
# import time


class Map:
    def __init__(self):
        self.country = 'France'
        self.intialized = False
        self.cities = []
        self.cities2 = []
        self.cities_reg = []
        self.cities_dept = []
        self.dept = []
        self.dept_code = []
        self.dept_reg = []
        self.reg = []
        self.reg_code = []

    def import_regions(self):
        with open('hello/data/regions.geojson') as f:
            data = json.loads(f.read())
            d = {int(i['properties']['code']): i for i in data['features']}

        with open('hello/data/reg2016.txt', encoding='latin_1') as f:
            rd = csv.reader(f, delimiter='\t')
            next(rd)
            for i in rd:
                code = int(i[0])
                name = unidecode(i[3]).lower().strip()
                name2 = unidecode(d[code]['properties']['nom']).lower().strip()
                geometry_coord = str(d[code]['geometry']['coordinates'])
                geometry_type = str(d[code]['geometry']['type'])
                created = False
                try:
                    r = Region.objects.get(code=code)
                except Exception as e:
                    print(e)
                    r = Region(code=code)
                    created = True

                if created:
                    r.name = name
                    r.name2 = name2
                    r.geometry_coord = geometry_coord
                    r.geometry_type = geometry_type
                    r.save()

        return True

    def import_departments(self):
        with open('hello/data/depts2016.txt', encoding='latin_1') as f:
            rd = csv.reader(f, delimiter='\t')
            next(rd)
            for i in rd:
                code = i[1]
                region_code = int(i[0])
                name = unidecode(i[4]).lower().strip()
                # created = False
                # try:
                #     d = Departement.objects.get(name=name)
                # except Exception as e:
                #     print(e)
                #     d = Departement(name=name)
                #     created = True
                #
                # if created:
                #     d.region_code = region_code
                #     d.code = code
                #     d.save()
                self.dept.append(name)
                self.dept_code.append(code)
                self.dept_reg.append(region_code)
        return True

    def import_cities(self):
        with open('hello/data/comsimp2016.txt', encoding='latin_1') as f:
            rd = csv.reader(f, delimiter='\t')
            next(rd)
            for i in rd:
                region_code = int(i[2])
                department_code = i[3]
                name = unidecode(i[9]).lower()
                name_complete = unidecode(i[8]).lower().strip() + ' ' + unidecode(i[9]).lower().strip()
                self.cities.append(name)
                self.cities2.append(name_complete)
                self.cities_reg.append(region_code)
                self.cities_dept.append(department_code)
        return True

    def initialize(self):
        if not self.intialized:
            if self.import_regions() and self.import_departments() and self.import_cities():
                self.intialized = True
            else:
                print("Error when initializing")

    def lookup_region(self, words):
        found = False
        res = None
        for w in words:
            res = Region.objects.filter(Q(name__contains=w) | Q(name2__contains=w))
            if len(res) > 0:
                found = True
                break
        return found, res

    def lookup_department(self, words):
        found = False
        res = None
        for w in words:
            pos = [ind for ind, name in enumerate(self.dept) if w in name]
            if len(pos) > 0:
                res = Region.objects.filter(code=self.dept_reg[pos[0]])
                found = True
                break
        return found, res

    def lookup_city(self, words):
        found = False
        res = None
        for w in words:
            pos = [ind for ind, name in enumerate(zip(self.cities, self.cities2)) if w in ','.join(name)]
            if len(pos) > 0:
                res = Region.objects.filter(code=self.cities_reg[pos[0]])
                found = True
                break
        return found, res

    def extract_region(self, s):
        if s is None or s == '' or s == 'None':
            return 'UNKNOWN'
        else:
            res = None
            if not self.intialized:
                self.initialize()
            words = [unidecode(w).lower().strip() for w in s.split(',')]
            words = [w for w in words if w != 'france' and w != '' and w is not None and w != 'NULL' and w != 'None']
            found = False
            for func in [self.lookup_region, self.lookup_department, self.lookup_city]:
                res = func(words)
                if res[0]:
                    found = True
                    break
            if found:
                return res[1][0].name
            else:
                return 'UNKNOWN'

    def tweet_region(self, tweet):
        region = tweet.usr_region
        if ~bool(region):
            if tweet.usr_place:
                region = self.extract_region(tweet.usr_place)
            else:
                region = 'UNKNOWN'
            tweet.usr_region = region
            tweet.save()
        return region

    def added_or_reg_unknown(self, tweet, labeled_data=True):
        if labeled_data:
            added = tweet.added_map
        else:
            added = tweet.added_map_pred
        if not added:
            region = self.tweet_region(tweet)
            if labeled_data:
                if region == 'UNKNOWN':
                    tweet.added_map = True
                    tweet.save()
                added = tweet.added_map
            else:
                if region == 'UNKNOWN':
                    tweet.added_map_pred = True
                    tweet.save()
                added = tweet.added_map_pred
        return added

    def add_tweet(self, tweet, labeled_data=True):
        added = self.added_or_reg_unknown(tweet, labeled_data=True)
        if added:
            print("Tweet already added")
        else:
            region = tweet.usr_region
            try:
                reg = Region.objects.get(Q(name__contains=region) | Q(name2__contains=region))
            except Exception as e:
                print('>>>>> Error while adding tweet')
                print(e)
                return False
            if labeled_data and tweet.sentiment_label != Tweet.SENTIMENTS['UNKNOWN']:
                if tweet.sentiment_label == Tweet.SENTIMENTS['POSITIVE']:
                    reg.num_tweets_pos += 1
                elif tweet.sentiment_label == Tweet.SENTIMENTS['NEGATIVE']:
                    reg.num_tweets_neg += 1
                else:
                    reg.num_tweets_net += 1
                reg.save()
                tweet.added_map = True
                tweet.save()
            elif ~labeled_data and tweet.sentiment_predicted != Tweet.SENTIMENTS['UNKNOWN']:
                if tweet.sentiment_predicted == Tweet.SENTIMENTS['POSITIVE']:
                    reg.num_tweets_pos_pred += 1
                elif tweet.sentiment_predicted == Tweet.SENTIMENTS['NEGATIVE']:
                    reg.num_tweets_neg_pred += 1
                else:
                    reg.num_tweets_net_pred += 1
                reg.save()
                tweet.added_map_pred = True
                tweet.save()
        return True

    def update_regions_color(self):
        if not self.intialized:
            self.initialize()
        res = Region.objects.all()
        for r in res:
            num_tweets = [r.num_tweets_pos, r.num_tweets_neg, r.num_tweets_net]
            # ind = np.argmax(num_tweets)
            if r.num_tweets_pos==0 and r.num_tweets_neg==0 and r.num_tweets_net==0:
                r.color = Region.COLORS['UNKNOWN']
            else:
                ground_hue = [120,0,60  ]
                hue = sum([ground_hue[i] * h / sum(num_tweets) for i, h in enumerate(num_tweets)])/360
                rgb = [round(i*255) for i in colorsys.hsv_to_rgb(hue,1,1)]
                r.color = '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])
            # elif ind==0:
            #     r.color = Region.COLORS['POSITIVE']
            # elif ind==1:
            #     r.color = Region.COLORS['NEGATIVE']
            # else:
            #     r.color = Region.COLORS['NEUTRAL']
            r.save()
        return True

    def add_all_tweets(self, labeled_data=True):
        if not self.intialized:
            self.initialize()
        if labeled_data:
            res = Tweet.objects.filter(~Q(sentiment_label=None) & Q(added_map=False))
        else:
            res = Tweet.objects.filter(~Q(sentiment_predicted=None) & Q(added_map_pred=False))
        if len(res)>0:
            for tweet in res:
                self.add_tweet(tweet)
        else:
            print('No tweet to update map')
        self.update_regions_color()
        return True


