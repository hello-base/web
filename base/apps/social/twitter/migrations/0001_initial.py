# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tweet_id', models.BigIntegerField(null=True, blank=True)),
                ('tweet_id_str', models.CharField(max_length=200, blank=True)),
                ('created_at', models.DateTimeField(null=True, blank=True)),
                ('text', models.TextField(blank=True)),
                ('source', models.CharField(max_length=200, blank=True)),
                ('in_reply_to_user_id', models.BigIntegerField(null=True, blank=True)),
                ('in_reply_to_user_id_str', models.CharField(max_length=200, null=True, blank=True)),
                ('in_reply_to_status_id', models.BigIntegerField(null=True, blank=True)),
                ('in_reply_to_status_id_str', models.CharField(max_length=200, null=True, blank=True)),
                ('retweeted', models.BooleanField(default=False)),
                ('retweeter_profile_image_url', models.URLField(blank=True)),
                ('retweeter_screen_name', models.CharField(max_length=200, blank=True)),
                ('retweeter_name', models.CharField(max_length=200, blank=True)),
                ('retweeted_status_id', models.BigIntegerField(null=True, blank=True)),
                ('retweeted_status_id_str', models.CharField(max_length=200, blank=True)),
                ('retweeted_status_created_at', models.DateTimeField(null=True, blank=True)),
                ('retweeted_status_text', models.TextField(blank=True)),
                ('retweeted_status_source', models.CharField(max_length=200, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TwitterUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('twitter_id', models.PositiveIntegerField(null=True, blank=True)),
                ('screen_name', models.CharField(max_length=200, blank=True)),
                ('name', models.CharField(max_length=200, blank=True)),
                ('description', models.TextField(blank=True)),
                ('location', models.CharField(max_length=200, blank=True)),
                ('profile_image_url', models.URLField(blank=True)),
                ('url', models.URLField(blank=True)),
                ('groups', models.OneToOneField(related_name=b'twitteruser', null=True, blank=True, to='people.Group')),
                ('idols', models.OneToOneField(related_name=b'twitteruser', null=True, blank=True, to='people.Idol')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tweet',
            name='user',
            field=models.ForeignKey(related_name=b'tweets', to='twitter.TwitterUser'),
            preserve_default=True,
        ),
    ]
