from django.db import models


# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)


class Region(models.Model):
    COLORS = {
        'POSITIVE': 'GREEN',
        'NEGATIVE': 'RED',
        'NEUTRAL': 'YELLOW',
        'UNKNOWN': 'GREY'
    }
    # objects = TweetManager()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    code = models.IntegerField(db_index=True)
    name = models.CharField(max_length=60)  # sans accent en minuscule
    name2 = models.CharField(max_length=60)
    geometry_coord = models.TextField(null=True)
    geometry_type = models.CharField(max_length=20, default="MultiPolygon")
    num_tweets_pos = models.IntegerField(default=0)
    num_tweets_neg = models.IntegerField(default=0)
    num_tweets_net = models.IntegerField(default=0)
    num_tweets_pos_pred = models.IntegerField(default=0)
    num_tweets_neg_pred = models.IntegerField(default=0)
    num_tweets_net_pred = models.IntegerField(default=0)
    color = models.CharField(max_length=20, default=COLORS.get('UNKNOWN'))
    color_pred = models.CharField(max_length=20, default=COLORS.get('UNKNOWN'))

    def __str__(self):
        return self.name


# class Departement(models.Model):
#     COLORS = {
#         'POSITIVE': 'GREEN',
#         'NEGATIVE': 'RED',
#         'NEUTRAL': 'YELLOW',
#         'UNKNOWN': 'GREY'
#     }
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)
#     code = models.CharField(max_length=10)
#     region_code = models.IntegerField()
#     name = models.CharField(max_length=60, db_index=True)
#     geometry = models.TextField(null=True)
#     num_tweets_pos = models.IntegerField(null=True)
#     num_tweets_neg = models.IntegerField(null=True)
#     num_tweets_net = models.IntegerField(null=True)
#     color = models.CharField(max_length=10, default=COLORS.get('UNKNOWN'))
#
#     def __str__(self):
#         return self.name
#
#
# class City(models.Model):
#     COLORS = {
#         'POSITIVE': 'GREEN',
#         'NEGATIVE': 'RED',
#         'NEUTRAL': 'YELLOW',
#         'UNKNOWN': 'GREY'
#     }
#     # objects = TweetManager()
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)
#     region_code = models.IntegerField()
#     department_code = models.CharField(max_length=10)
#     name = models.CharField(max_length=60, db_index=True)
#     geometry = models.TextField(null=True)
#     num_tweets_pos = models.IntegerField(null=True)
#     num_tweets_neg = models.IntegerField(null=True)
#     num_tweets_net = models.IntegerField(null=True)
#     color = models.CharField(max_length=10, default=COLORS.get('UNKNOWN'))
#
#     def __str__(self):
#         return self.name
