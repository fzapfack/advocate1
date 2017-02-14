from django.db import models
# from multiselectfield import MultiSelectField
# Create your models here.


class TweetManager(models.Manager):
    def create_tweet(self, d):
        tweet = self.create(**d)
        return tweet


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
    usr_place = models.CharField(max_length=50, db_tablespace="indexes", null=True)
    usr_region = models.CharField(max_length=60, db_tablespace="indexes", null=True)
    lang = models.CharField(max_length=10, db_tablespace="indexes", null=True)
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
