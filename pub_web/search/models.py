from django.db import models
from django.contrib.auth.models import User


class Pub(models.Model):

    pubid = models.IntegerField(primary_key=True)
    pub_year = models.IntegerField()
    title = models.CharField(max_length=200)
    abstract = models.TextField()

    def __unicode__(self):
        return self.title