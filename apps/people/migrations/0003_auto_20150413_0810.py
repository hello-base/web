# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_auto_20141223_0316'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupshot',
            old_name='group',
            new_name='subject',
        ),
        migrations.RenameField(
            model_name='headshot',
            old_name='idol',
            new_name='subject',
        ),
    ]
