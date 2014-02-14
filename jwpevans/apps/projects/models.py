from django.db import models

class Pun(models.Model):

    text = models.CharField(max_length=1000)
    pun_target = models.CharField(max_length=100)
    url = models.UrlField()

    def make_template(self):
        pass