from django.contrib import admin

from .models import Tweet
from .forms import TweetForm

class TweetAdmin(admin.ModelAdmin):
    list_display = ["updated","usr_place","retweet","lang"]
    # fields = ['sentiment_label']
    # form = TweetForm
    class Meta:
        model = Tweet

    # def upper_case_name(self, obj):
    #     return ("%s %s" % (obj.first_name, obj.last_name)).upper()
admin.site.register(Tweet, TweetAdmin)

# Register your models here.
