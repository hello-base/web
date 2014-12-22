# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('romanized_name', models.CharField(max_length=60)),
                ('started', models.DateField(db_index=True)),
                ('ended', models.DateField(db_index=True, null=True, blank=True)),
                ('group', models.ForeignKey(related_name=b'designations', to='people.Group')),
            ],
            options={
                'get_latest_by': 'started',
            },
            bases=(models.Model,),
        ),
        migrations.AlterOrderWithRespectTo(
            name='designation',
            order_with_respect_to='group',
        ),
    ]
