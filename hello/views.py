from django.shortcuts import render
import json
from django.db.models import Q
from .models import Greeting
from listener.models import Tweet as TweetModel
from hello.models import Region
from hello.utils.carte_fr import Map


# Create your views here.
def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, 'db.html', {'greetings': greetings})


def flat_list(l):
    res = []
    if isinstance(l,list):
        for i in l:
            if isinstance(i,list):
                if len(i)==1:
                    res.append(flat_list(i[0]))
                else:
                    res.append(flat_list(i))
            else:
                res = l
    else:
        res = l
    return res


def flat_list(l,res=[]):
    if isinstance(l, list):
        if isinstance(l[0], list):
            l2 = [i for l1 in l for i in l1]
            return flat_list(l2,res)
        else:
            return res.extend(l)
    else:
        return res.append(l)


def index(request):
    m = Map()
    labeled_data = False  # Map based on prediction
    m.add_all_tweets(labeled_data)

    regions = Region.objects.all()
    features = []
    for r in regions:
        if labeled_data:
            num_tweets = [r.num_tweets_pos, r.num_tweets_neg, r.num_tweets_net]
        else:
            num_tweets = [r.num_tweets_pos_pred, r.num_tweets_neg_pred, r.num_tweets_net_pred]
        pos = []
        coord = json.loads(r.geometry_coord)
        flat_list(coord,pos)
        f = {
            "type": "Feature",
            "properties": {
                "name": r.name,
                "color": r.color,
                "position": {"lng": float(sum(pos[::2]))/len(pos[::2]), "lat": float(sum(pos[1::2]))/len(pos[1::2])},
                "reg_num_pos": num_tweets[0],
                "reg_num_neg": num_tweets[1],
                "reg_num_net": num_tweets[2],
                "num_tweets": sum(num_tweets)
            },
            "geometry": {
                "type": r.geometry_type,
                "coordinates":json.loads(r.geometry_coord)
            }
        }
        features.append(f)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    context = {}
    context['authenticated'] = request.user.is_authenticated()
    context['geojson'] = json.dumps(geojson)
    if context['authenticated'] == True:
        context['username'] = request.user.username
    if labeled_data:
        context['num_pos'] = TweetModel.objects.filter(sentiment_label=TweetModel.SENTIMENTS['POSITIVE']).count()
        context['num_neg'] = TweetModel.objects.filter(sentiment_label=TweetModel.SENTIMENTS['NEGATIVE']).count()
        context['num_net'] = TweetModel.objects.filter(sentiment_label=TweetModel.SENTIMENTS['NEUTRAL']).count()
        context['num_local'] = TweetModel.objects.filter(~Q(sentiment_label=None) & ~Q(usr_region='UNKNOWN')).count()
    else:
        context['num_pos'] = TweetModel.objects.filter(sentiment_predicted=TweetModel.SENTIMENTS['POSITIVE']).count()
        context['num_neg'] = TweetModel.objects.filter(sentiment_predicted=TweetModel.SENTIMENTS['NEGATIVE']).count()
        context['num_net'] = TweetModel.objects.filter(sentiment_predicted=TweetModel.SENTIMENTS['NEUTRAL']).count()
        context['num_local'] = TweetModel.objects.filter(~Q(sentiment_predicted=None) & ~Q(usr_region='UNKNOWN')).count()


    return render(request, 'index.html', context)



