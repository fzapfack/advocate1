from django.shortcuts import render
import json
from .models import Greeting
from listener.models import Tweet as TweetModel
from hello.models import Region
from hello.utils.carte_fr import Map

from hello.models import Region
regions = Region.objects.all()
for r in regions:
    r.num_tweets_pos = 0
    r.num_tweets_neg = 0
    r.num_tweets_net = 0
    r.save()

from listener.models import Tweet as TweetModel
res = TweetModel.objects.all()
for t in res:
    t.added_map = False
    t.usr_region = None
    t.save()

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
    regions = Region.objects.all()
    features = []
    for r in regions:
        pos = []
        coord = json.loads(r.geometry_coord)
        flat_list(coord,pos)
        f = {
            "type": "Feature",
            "properties": {
                "name": r.name,
                "color": r.color,
                "position": {"lng": float(sum(pos[::2]))/len(pos[::2]), "lat": float(sum(pos[1::2]))/len(pos[1::2])},
                "num_pos": r.num_tweets_pos,
                "num_neg": r.num_tweets_neg,
                "num_net": r.num_tweets_net,
                "num_tweets": r.num_tweets_pos + r.num_tweets_neg + r.num_tweets_net
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
    m = Map()
    m.add_all_tweets()
    context = {}
    context['authenticated'] = request.user.is_authenticated()
    if context['authenticated'] == True:
        context['username'] = request.user.username
    context['num_pos'] = TweetModel.objects.filter(sentiment_label=TweetModel.SENTIMENTS['POSITIVE']).count()
    context['num_neg'] = TweetModel.objects.filter(sentiment_label=TweetModel.SENTIMENTS['NEGATIVE']).count()
    context['num_net'] = TweetModel.objects.filter(sentiment_label=TweetModel.SENTIMENTS['NEUTRAL']).count()
    context['num_net'] = TweetModel.objects.filter(sentiment_label=TweetModel.SENTIMENTS['NEUTRAL']).count()
    context['geojson'] = json.dumps(geojson)

    return render(request, 'index.html', context)



