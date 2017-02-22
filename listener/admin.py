from django.contrib import admin

from .models import Tweet
from .models import Profile


class TweetAdmin(admin.ModelAdmin):
    list_display = ["txt","usr_screen_name","in_reply_to","usr_region","created","lang",'sentiment_label','sentiment_predicted']
    class Meta:
        model = Tweet


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "num_tests", "num_tweets_labelled", "staff"]

    class Meta:
        model = Profile

    # def upper_case_name(self, obj):
    #     return ("%s %s" % (obj.first_name, obj.last_name)).upper()
admin.site.register(Tweet, TweetAdmin)
admin.site.register(Profile, ProfileAdmin)
# Register your models here.
