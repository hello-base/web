# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appearances', '0001_initial'),
        ('accounts', '0001_initial'),
        ('events', '0001_initial'),
        ('people', '0001_initial'),
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField()),
                ('activity', models.ForeignKey(related_name='facts', blank=True, to='events.Activity', null=True)),
                ('album', models.ForeignKey(related_name='facts', blank=True, to='music.Album', null=True)),
                ('event', models.ForeignKey(related_name='facts', blank=True, to='events.Event', null=True)),
                ('group', models.ForeignKey(related_name='facts', blank=True, to='people.Group', null=True)),
                ('idol', models.ForeignKey(related_name='facts', blank=True, to='people.Idol', null=True)),
                ('single', models.ForeignKey(related_name='facts', blank=True, to='music.Single', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField(blank=True)),
                ('activity', models.ForeignKey(related_name='summaries', blank=True, to='events.Activity', null=True)),
                ('episode', models.ForeignKey(related_name='summaries', blank=True, to='appearances.Episode', null=True)),
                ('event', models.ForeignKey(related_name='summaries', blank=True, to='events.Event', null=True)),
                ('issue', models.ForeignKey(related_name='summaries', blank=True, to='appearances.Issue', null=True)),
                ('submitted_by', models.ForeignKey(related_name='summary_submissions', blank=True, to='accounts.Editor', null=True)),
            ],
            options={
                'verbose_name_plural': 'summaries',
            },
            bases=(models.Model,),
        ),
    ]
