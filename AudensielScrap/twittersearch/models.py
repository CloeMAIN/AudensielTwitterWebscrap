# from django.db import models
# #from db_connection import db

# # Create your models here.
# #tweet_collection = db['TestFrontEnd']

# class DonneeCollectee(models.Model):
#     text_tweet = models.TextField()
#     date_tweet = models.DateField()
#     identifiant = models.IntegerField()
#     req_id = models.CharField(max_length=200)
#     nombre_likes = models.IntegerField()
#     nombre_reposts = models.IntegerField()
#     nombre_replies = models.IntegerField()
#     nombre_views = models.IntegerField()


from mongoengine import Document, StringField, IntField, DateTimeField

class DonneeCollectee(Document):
    text_tweet = StringField()
    date_tweet = DateTimeField()
    identifiant = IntField()
    req_id = StringField(max_length=200)
    nombre_likes = IntField()
    nombre_reposts = IntField()
    nombre_replies = IntField()
    nombre_views = IntField()