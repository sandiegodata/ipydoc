from django.db import models

from django.db import models

class User(models.Model):
    username = models.CharField(max_length=200)
    state = models.CharField(max_length=10)
    

class GithubAccount(models.Model):
    user = models.ForeignKey(User)
    username = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
