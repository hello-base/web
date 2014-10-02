# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Correlation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField(verbose_name='object ID')),
                ('timestamp', models.DateField(blank=True)),
                ('identifier', models.CharField(max_length=25)),
                ('date_field', models.CharField(max_length=25)),
                ('description', models.TextField(blank=True)),
                ('classification', models.IntegerField(default=1, choices=[(0, 'Major'), (1, 'Normal'), (2, 'Minor')])),
                ('julian', models.PositiveSmallIntegerField(help_text='The day of the year (1 to 365).', max_length=3, verbose_name='julian date')),
                ('year', models.PositiveSmallIntegerField(max_length=4)),
                ('month', models.PositiveSmallIntegerField(max_length=2)),
                ('day', models.PositiveSmallIntegerField(max_length=2)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('-timestamp',),
                'get_latest_by': 'timestamp',
            },
            bases=(models.Model,),
        ),
    ]
