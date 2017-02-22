from django.db import models
from django.contrib.auth.models import User
from hello.models import Region

class ProfileManager(models.Manager):
    def get_create_usr_profile(self,pk):
        try:
            u = User.objects.get(pk=pk)
        except Exception as e2:
            print("User don't exist")
            return None
        try:
            prof = self.get(user__pk=pk)
        except Exception as e:
            print("Creating new profile for user pk="+str(pk))
            prof = Profile(user=u)
            prof.save()
        return prof


class Profile(models.Model):
    MAX_NUM_PROFILES = 10
    STAFF = {
        'L2L': 1,
        'OTHER': 0
    }
    CODES = {
        'L2L':'test-l2l'
    }
    STAFF_CHOICES = (
        (STAFF['L2L'], 'L2L'),
        (STAFF['OTHER'], 'Normal User'),
    )
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    partner_code = models.CharField(max_length=20, default='')
    num_tests = models.IntegerField(default=0, blank=True)
    num_tweets_labelled = models.IntegerField(default=0, blank=True)
    staff = models.IntegerField(choices=STAFF_CHOICES, default=STAFF['OTHER'],
                                blank=True)
    objects = ProfileManager()

    def __str__(self):
        s = [i[0] for i in Profile.STAFF.items() if i[1]==self.staff][0]
        return str(self.user)+", "+ s

# Create your models here.


class TweetManager(models.Manager):
    def create_tweet(self, d):
        tweet = self.create(**d)
        return tweet

    def delete_all(self):
        _ = self.all().delete()
        regions = Region.objects.all()
        for r in regions:
            r.num_tweets_pos = 0
            r.num_tweets_pos_pred = 0
            r.num_tweets_neg = 0
            r.num_tweets_neg_pred = 0
            r.num_tweets_net = 0
            r.num_tweets_net_pred = 0
            r.save()
        return True


class Tweet(models.Model):
    objects = TweetManager()
    updated = models.DateTimeField(auto_now=True, db_tablespace="indexes")
    created = models.DateTimeField(auto_now_add=True, db_tablespace="indexes")
    SENTIMENTS = {
        'POSITIVE': 1,
        'NEGATIVE': -1,
        'NEUTRAL': 0,
        'UNKNOWN': 2
    }
    SENTIMENT_CHOICES = (
        (SENTIMENTS['POSITIVE'], 'Positif'),
        (SENTIMENTS['NEGATIVE'], 'Negatif'),
        (SENTIMENTS['NEUTRAL'], 'Neutre'),
        (SENTIMENTS['UNKNOWN'], 'Inconnu'),
    )
    sentiment_predicted = models.IntegerField(choices=SENTIMENT_CHOICES,
                                              db_tablespace="indexes", null=True)
    sentiment_label = models.IntegerField(choices=SENTIMENT_CHOICES,
                                          db_tablespace="indexes", null=True)

    txt = models.TextField(null=False, blank=False, db_tablespace="indexes")
    retweet = models.TextField(null=True, blank=False, db_tablespace="indexes")
    twitter_id = models.CharField(max_length=30, db_tablespace="indexes", null=True)
    retweet_twitter_id = models.CharField(max_length=30, db_tablespace="indexes", null=True)
    usr_twitter_id = models.CharField(max_length=30, db_tablespace="indexes", null=True)
    usr_screen_name = models.CharField(max_length=30, db_tablespace="indexes", null=True)
    usr_place = models.CharField(max_length=50, db_tablespace="indexes", null=True)
    usr_region = models.CharField(max_length=60, db_tablespace="indexes", null=True)
    lang = models.CharField(max_length=10, db_tablespace="indexes", null=True)
    in_reply_to = models.CharField(max_length=30, db_tablespace="indexes", null=True)
    added_map = models.BooleanField(default=False)
    added_map_pred = models.BooleanField(default=False)

    # GENERAL = 0
    # ECONOMY = 1
    # SANTE = 2
    # PS = 3
    # LR = 4
    # FN = 5
    # EM = 6  # En marche
    # TOPIC_CHOICES = (
    #     (GENERAL, 'General'),
    #     (ECONOMY, 'Economie'),
    #     (SANTE, 'Sante'),
    #     (PS, 'Parti Socialiste'),
    #     (LR, 'Les Republicains'),
    #     (FN, 'Front National'),
    #     (EM, 'En Marche')
    # )

    # topic = models.IntegerField(default=0, choices=TOPIC_CHOICES,db_tablespace="indexes")
    # topic_predicted = MultiSelectField(choices=TOPIC_CHOICES,
    #                          # default='1,5')
    #                               null=True)
    # topic_label = MultiSelectField(choices=TOPIC_CHOICES,null=True)
    def __str__(self):
        return str(self.txt)

    def __unicode__(self):
        return str(self.txt)
