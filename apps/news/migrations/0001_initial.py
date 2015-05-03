# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('appearances', '0001_initial'),
        ('correlations', '0001_initial'),
        ('accounts', '0001_initial'),
        ('events', '0001_initial'),
        ('people', '0001_initial'),
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=16, choices=[('announcement', 'Announcement'), ('appearance', 'Appearance'), ('audition', 'Audition'), ('event', 'Event'), ('goods', 'Goods'), ('graduation', 'Graduation'), ('promo', 'Promo'), ('release', 'Release'), ('rumor', 'Rumor'), ('other', 'Other')])),
                ('classification', models.CharField(default='normal', max_length=16, choices=[('major', 'Major'), ('important', 'Important'), ('normal', 'Normal'), ('minor', 'Minor')])),
                ('title', models.CharField(max_length=500)),
                ('slug', models.SlugField(max_length=200)),
                ('body', models.TextField(blank=True)),
                ('published', models.DateField(default=datetime.date(2014, 10, 3))),
                ('source', models.CharField(help_text='Separate multiple sources by comma (must have accompanying URL).', max_length=200, blank=True)),
                ('source_url', models.URLField(help_text='Seperate multiple URLs with comma (must have accompanying Source).', max_length=500, verbose_name='source URL', blank=True)),
                ('via', models.CharField(max_length=200, blank=True)),
                ('via_url', models.URLField(max_length=500, verbose_name='via URL', blank=True)),
                ('albums', models.ManyToManyField(related_name='items', null=True, to='music.Album', blank=True)),
                ('author', models.ForeignKey(related_name='item_submissions', blank=True, to='accounts.Editor', null=True)),
                ('correlations', models.ManyToManyField(related_name='items', null=True, to='correlations.Correlation', blank=True)),
                ('events', models.ManyToManyField(related_name='items', null=True, to='events.Event', blank=True)),
                ('groups', models.ManyToManyField(related_name='items', null=True, to='people.Group', blank=True)),
                ('idols', models.ManyToManyField(related_name='items', null=True, to='people.Idol', blank=True)),
                ('magazines', models.ManyToManyField(related_name='items', null=True, to='appearances.Magazine', blank=True)),
                ('shows', models.ManyToManyField(related_name='items', null=True, to='appearances.Show', blank=True)),
                ('singles', models.ManyToManyField(related_name='items', null=True, to='music.Single', blank=True)),
            ],
            options={
                'ordering': ('-published',),
                'get_latest_by': 'published',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to='news/', blank=True)),
                ('caption', models.CharField(max_length=500, blank=True)),
                ('parent', models.ForeignKey(related_name='images', to='news.Item')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField(blank=True)),
                ('published', models.DateField(default=datetime.date(2014, 10, 3))),
                ('source', models.CharField(help_text='Separate multiple sources by comma (must have accompanying URL).', max_length=200, blank=True)),
                ('source_url', models.URLField(help_text='Seperate multiple URLs with comma (must have accompanying Source).', verbose_name='source URL', blank=True)),
                ('via', models.CharField(max_length=200, blank=True)),
                ('via_url', models.URLField(verbose_name='via URL', blank=True)),
                ('author', models.ForeignKey(related_name='update_submissions', blank=True, to='accounts.Editor', null=True)),
                ('parent', models.ForeignKey(related_name='updates', to='news.Item')),
            ],
            options={
                'ordering': ('parent', 'published'),
            },
            bases=(models.Model,),
        ),
    ]
