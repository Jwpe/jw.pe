from django.db import models

class Pun(models.Model):

    text = models.CharField(max_length=1000)
    pun_target = models.CharField(max_length=100)
    url = models.URLField()

    def make_template(self):
        pun_tag = "<span class='valentines'>{}</span>".format(self.pun_target)
        html = self.text.replace(self.pun_target, pun_tag)
        return html