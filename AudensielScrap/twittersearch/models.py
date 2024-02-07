from django.db import models
from db_connection import db


# Create your models here.
tweet_collection = db['tweets']
req_collection = db['requests']
