from django.db import models

# Create your models here.
class Suspect(models.Model):
  First_name = models.CharField(max_length=50)
  Age = models.CharField(max_length=4)
  Identifying_features = models.CharField(max_length=100)
  Criminal_History = models.CharField(max_length=100)
  Behavioral_Patterns = models.CharField(max_length=100)
  Image_url = models.CharField(max_length=100)