# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='published',
            field=models.DateField(default=datetime.date(2014, 12, 23)),
        ),
        migrations.AlterField(
            model_name='update',
            name='published',
            field=models.DateField(default=datetime.date(2014, 12, 23)),
        ),
    ]
