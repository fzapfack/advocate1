from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from listener.tasks import add_tweet

from .forms import TweetForm
from .models import Tweet as TweetModel


def get_name(request):
    non_labelled = TweetModel.objects.filter(sentiment_label=None)
    if non_labelled is None or len(non_labelled) < 1:
        tweet = TweetModel()
    else:
        tweet = non_labelled.last()
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
        'form': form
    }
    return render(request, 'label.html', context)

# Create your views here.


def add_tweet_view(request):
    print('Enter add_tweet_view')
    add_tweet.delay('Enter add_tweet')
    return HttpResponse('Tweet added')
# Create your views here.
