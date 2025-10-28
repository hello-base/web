# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=60)),
                ('ytid', models.CharField(max_length=60, verbose_name='YouTube ID', blank=True)),
                ('group', models.OneToOneField(related_name='channel', on_delete=models.SET_NULL, null=True, blank=True, to='people.Group')),
                ('idol', models.OneToOneField(related_name='channel', on_delete=models.SET_NULL, null=True, blank=True, to='people.Idol')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quality', models.CharField(default='default', max_length=10)),
                ('url', models.URLField(verbose_name='URL')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('ytid', models.CharField(max_length=200, unique=True, serialize=False, verbose_name='YouTube ID', primary_key=True)),
                ('title', models.CharField(max_length=200, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('published', models.DateTimeField(null=True, blank=True)),
                ('duration', models.CharField(max_length=10, null=True, blank=True)),
                ('channel', models.ForeignKey(on_delete=models.SET_NULL, related_name='videos', to='youtube.Channel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='thumbnail',
            name='video',
            field=models.ForeignKey(on_delete=models.SET_NULL, related_name='thumbnails', to='youtube.Video', null=True),
            preserve_default=True,
        ),
    ]
