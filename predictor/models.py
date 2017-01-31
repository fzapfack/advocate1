from django.db import models
# Create your models here.


class TestManager(models.Manager):
    def create_tweet(self,d):
        tweet = self.create(**d)
        return tweet


class TestModel(models.Model):
    objects = TestManager()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    number_labels = models.IntegerField(default=0)
    number_labels_correct = models.IntegerField(default=0)
    number_labels_incorrect = models.IntegerField(default=0)
    user_email = models.EmailField(null=True)
    user_id = models.IntegerField(default=0)


    def __str__(self):
        return 'id='+str(self.pk)+' created=str(self.created)'

    def __unicode__(self):
        return 'id='+str(self.pk)+' created=str(self.created)'
