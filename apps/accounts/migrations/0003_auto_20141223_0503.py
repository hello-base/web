# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20141003_0510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editor',
            name='active_since',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 23, 5, 3, 11, 642360), blank=True),
        ),
    ]
