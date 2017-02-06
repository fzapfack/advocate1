from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from listener.tasks import add_tweet
from django.db.models import Q
from celery.task.control import inspect

from .forms import TweetForm
from .models import Tweet as TweetModel
import listener.config


def get_name(request):
    # On labelise en premier les tweets non retweetes
    non_labelled = TweetModel.objects.filter(retweet=None, sentiment_label=None)
    if non_labelled is None or len(non_labelled) < 1:
        non_labelled = TweetModel.objects.filter(sentiment_label=None)
    num_labels = TweetModel.objects.filter(~Q(sentiment_label=None)).count()
    if non_labelled is None or len(non_labelled) < 1:
        tweet = TweetModel()
    else:
        tweet = non_labelled.first()
    if request.method == 'POST':
        form = TweetForm(request.POST, instance=tweet)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return HttpResponseRedirect('/labeling/')
        else:
            pass
        # else:
        #     return HttpResponseRedirect('/labeling/')
    else:
        form = TweetForm(instance=tweet)
    context = {
        'tweet': tweet.txt,
        'retweet': tweet.retweet,
        'form': form,
        'num_labels': num_labels
    }
    return render(request, 'label.html', context)

# Create your views here.


def add_tweet_view(request):
    print('Enter add_tweet_view')
    if listener.config.WORKER_STARTED:
        print('\ listener worker already started')
        print(inspect().active())
        return HttpResponse('Listener worker already started, Please check logs for active celery tasks')
    else:
        print('Creating celery task')
        add_tweet.delay('Twitter listener starting')
        listener.config.WORKER_STARTED = True
        return HttpResponse('Twitter listener started')
# Create your views here.
