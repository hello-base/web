# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editor',
            name='active_since',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 3, 5, 10, 46, 993270), blank=True),
        ),
    ]
