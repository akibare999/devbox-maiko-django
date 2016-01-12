from django.db import models

# Create your models here.

class Person(models.Model):
    uin = models.CharField(max_length=9, primary_key=True)

    uiuc_netid = models.CharField(max_length=8)
    uic_netid = models.CharField(max_length=8)
    uis_netid = models.CharField(max_length=8)
    illinois_netid = models.CharField(max_length=8)
    uillinois_netid = models.CharField(max_length=8)

    i2s_firstname = models.CharField(max_length=50)
    i2s_lastname = models.CharField(max_length=50)

    banner_firstname = models.CharField(max_length=50)
    banner_lastname = models.CharField(max_length=50)

    banner_suppressed = models.BooleanField(default=False)

    def __unicode__(self):
        return ''.join(['Person[', self.uin, ']: ',
                       self.i2s_firstname, ' ',
                       self.i2s_lastname])
