from django.shortcuts import render
from django.http import HttpResponse
import random
from .models import Greeting
from listener.models import Tweet as TweetModel

REGIONS_FR = {'Corse': 'FR-H', 'Centre-Val de Loire': 'FR-F', 'Hauts-de-France': 'FR-S', 'Nouvelle-Aquitaine': 'FR-B',
              'Auvergne-Rhône-Alpes': 'FR-V', 'Auvergne-Rhône-Alpes2': 'FR-C', 'Grand-Est': 'FR-G', 'Normandie': 'FR-P', 'Île-de-France': 'FR-J',
              'Bretagne': 'FR-E', 'Bourgogne-Franche-Comté': 'FR-D', "Provence-Alpes-Côte d’Azur": 'FR-U',
              'Occitanie': 'FR-N', 'Pays de la Loire': 'FR-R', "Languedoc-Roussillon": 'FR-K'}
html_part=', '.join(["['{}',{},'{}']".format(i[1],random.choice([-1,1,0]),i[0].replace("'"," ")) for i in REGIONS_FR.items()])


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    context = {}
    context['authenticated'] = request.user.is_authenticated()
    if context['authenticated'] == True:
        context['username'] = request.user.username
        context['num_pos'] = TweetModel.objects.filter(sentiment_label=TweetModel.SENTIMENTS['POSITIVE']).count()
        context['num_neg'] = TweetModel.objects.filter(sentiment_label=TweetModel.SENTIMENTS['NEGATIVE']).count()
        context['num_net'] = TweetModel.objects.filter(sentiment_label=TweetModel.SENTIMENTS['NEUTRAL']).count()
    return render(request, 'index.html',context)

def map(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'maps_france.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

