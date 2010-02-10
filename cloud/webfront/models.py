from appengine_django.models import BaseModel
from google.appengine.ext import db

# Create your models here.
class Photo(BaseModel):
  id = db.IntegerProperty('F-Spot ID')
  time = db.DateTimeProperty('photo date')
  jpeg = db.BlobProperty('jpeg data')
