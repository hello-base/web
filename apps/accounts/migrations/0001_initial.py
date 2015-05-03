# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime
import ohashi.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Editor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('base_id', models.IntegerField(unique=True, verbose_name=b'Hello! Base ID', db_index=True)),
                ('username', ohashi.db.models.fields.CharField(db_index=True, unique=True, blank=True)),
                ('name', ohashi.db.models.fields.CharField(blank=True)),
                ('email', ohashi.db.models.fields.EmailField(unique=True, db_index=True)),
                ('started', models.DateTimeField(default=datetime.datetime.now)),
                ('active_since', models.DateTimeField(default=datetime.datetime(2014, 10, 3, 5, 10, 27, 745927), blank=True)),
                ('access_token', ohashi.db.models.fields.CharField(blank=True)),
                ('refresh_token', ohashi.db.models.fields.CharField(blank=True)),
                ('token_expiration', models.IntegerField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
