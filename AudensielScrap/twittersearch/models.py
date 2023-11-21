from django.db import models
from djongo import models as djongomodels

class TweetModele(models.Model):
    id = djongomodels.IntegerField(primary_key=True)
    tweet = djongomodels.TextField()
