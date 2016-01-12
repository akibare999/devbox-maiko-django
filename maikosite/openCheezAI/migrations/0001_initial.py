# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('uin', models.CharField(max_length=9, serialize=False, primary_key=True)),
                ('uiuc_netid', models.CharField(max_length=8)),
                ('uic_netid', models.CharField(max_length=8)),
                ('uis_netid', models.CharField(max_length=8)),
                ('illinois_netid', models.CharField(max_length=8)),
                ('uillinois_netid', models.CharField(max_length=8)),
                ('i2s_firstname', models.CharField(max_length=50)),
                ('i2s_lastname', models.CharField(max_length=50)),
                ('banner_firstname', models.CharField(max_length=50)),
                ('banner_lastname', models.CharField(max_length=50)),
                ('banner_suppressed', models.BooleanField(default=False)),
            ],
        ),
    ]
