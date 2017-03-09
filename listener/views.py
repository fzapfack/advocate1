from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Q
from celery.task.control import inspect

from listener.tasks import add_tweet
from .forms import TweetForm
from .models import Tweet as TweetModel
import listener.config
from listener.models import Profile
from predictor.utils.predictor import Predictor
from predictor.utils.alchemy_predictor import AlchemyPredictor


def sentiment_str(tweet):
    if tweet.sentiment_predicted is None:
        return 'Inconnu'
    else:
        return [i[1] for i in TweetModel.SENTIMENT_CHOICES if i[0] == tweet.sentiment_predicted][0]


def get_name(request):
    prof_list = Profile.objects.order_by('-num_tweets_labelled')
    if len(prof_list) > 0:
        prof_list = prof_list[:min(len(prof_list), Profile.MAX_NUM_PROFILES)]
    prof_usr = Profile.objects.get_create_usr_profile(request.user.pk)

    # non_labelled = TweetModel.objects.filter(in_reply_to=None, sentiment_label=None)
    non_labelled = TweetModel.objects.filter(Q(in_reply_to=None, sentiment_label=None) &
                                             ~Q(txt__icontains='http') & Q(lang='fr'))
    if non_labelled is None or len(non_labelled) < 1:
        non_labelled = TweetModel.objects.filter(sentiment_label=None, in_reply_to=None, lang='fr')
    num_labels = TweetModel.objects.filter(~Q(sentiment_label=None)).count()
    accuracy = 0
    if non_labelled is None or len(non_labelled) < 1:
        tweet = TweetModel()
    else:
        tweet = non_labelled.last()
        predictor = AlchemyPredictor()
        tweet.sentiment_predicted = predictor.predict_tweet(tweet)
        num_labels, accuracy = predictor.get_accuracy()
    if request.method == 'POST':
        form = TweetForm(request.POST, instance=tweet)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            prof_usr.num_tweets_labelled += 1
            prof_usr.save()
            return HttpResponseRedirect('/labeling/')
        else:
            pass
        # else:
        #     return HttpResponseRedirect('/labeling/')
    else:
        form = TweetForm(instance=tweet)
    context = {
        'tweet': tweet,
        'form': form,
        'num_labels': num_labels,
        "accuracy": accuracy,
        'prof_list': prof_list,
        'prediction': sentiment_str(tweet)
    }
    return render(request, 'label.html', context)

# Create your views here.


def add_tweet_view(request):
    print('Enter add_tweet_view')
    active_jobs = inspect().active()
    if active_jobs is not None:
        b = [i for i in active_jobs.values()]
        b = [item for sublist in b for item in sublist]
        if len(b) > 0 and any(['add_tweet' in i['name'] for i in b]):
            listener.config.WORKER_STARTED = True

    if listener.config.WORKER_STARTED:
        print('\ listener worker already started')
        print(inspect().active())
        return HttpResponse('Listener worker already started, Please check logs for active celery tasks')
    else:
        print('Creating celery task')
        add_tweet.delay('Twitter listener starting')
        print(listener.config.WORKER_STARTED)
        return HttpResponse('Twitter listener started')
# Create your views here.
