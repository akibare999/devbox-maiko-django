from django.db import models

# Create your models here.

class Person(models.Model):
    uin = models.CharField(max_length=9, primary_key=True)

    uiuc_netid = models.CharField(max_length=8, blank=True)
    uic_netid = models.CharField(max_length=8, blank=True)
    uis_netid = models.CharField(max_length=8, blank=True)
    illinois_netid = models.CharField(max_length=8, blank=True)
    uillinois_netid = models.CharField(max_length=8, blank=True)

    i2s_firstname = models.CharField(max_length=50, blank=True)
    i2s_lastname = models.CharField(max_length=50, blank=True)

    banner_firstname = models.CharField(max_length=50, blank=True)
    banner_lastname = models.CharField(max_length=50, blank=True)

    banner_suppressed = models.BooleanField(default=False)

    def __unicode__(self):
        return ''.join(['Person[', self.uin, ']: ',
                       self.i2s_firstname, ' ',
                       self.i2s_lastname])
