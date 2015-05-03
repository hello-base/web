# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('day', models.DateField()),
                ('romanized_name', models.CharField(max_length=200, blank=True)),
                ('name', models.CharField(max_length=200, blank=True)),
                ('start_time', models.TimeField(null=True, blank=True)),
                ('description', models.TextField(help_text=b'If multiple activities took place on the same day/event, it can be specified here.', blank=True)),
                ('is_performance', models.BooleanField(default=False, verbose_name=b'is a performance?')),
                ('venue_known_as', models.CharField(help_text=b'Did the venue go by another name at the time of this activity?', max_length=200, blank=True)),
                ('edited_by', models.ManyToManyField(related_name=b'activitys_edits', null=True, to='accounts.Editor', blank=True)),
            ],
            options={
                'ordering': ('day', 'start_time'),
                'get_latest_by': 'day',
                'verbose_name_plural': 'activities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('category', models.CharField(default=b'general', max_length=16, choices=[(b'birthday', b'Birthday'), (b'bustour', b'Bus Tour'), (b'concert', b'Concert'), (b'convention', b'Convention'), (b'dinnershow', b'Dinner Show'), (b'general', b'General'), (b'hawaii', b'Hawaii'), (b'live', b'Live'), (b'release', b'Release'), (b'promotional', b'Promotional'), (b'other', b'Other')])),
                ('romanized_name', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('nickname', models.CharField(max_length=200)),
                ('slug', models.SlugField()),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('info_link_name', models.CharField(help_text=b'Separate multiple link names by comma (must have accompanying info link).', max_length=200, blank=True)),
                ('info_link', models.URLField(help_text=b'Seperate multiple links with comma (must have accompanying link name).', max_length=500, blank=True)),
                ('logo', models.ImageField(null=True, upload_to=b'events/events/', blank=True)),
                ('promotional_image', models.ImageField(null=True, upload_to=b'events/events/', blank=True)),
                ('stage', models.ImageField(null=True, upload_to=b'events/events/', blank=True)),
                ('has_handshake', models.BooleanField(default=False, verbose_name=b'has handshake?')),
                ('is_fanclub', models.BooleanField(default=False, verbose_name=b'fanclub?')),
                ('is_international', models.BooleanField(default=False, verbose_name=b'international?')),
                ('edited_by', models.ManyToManyField(related_name=b'events_edits', null=True, to='accounts.Editor', blank=True)),
                ('groups', models.ManyToManyField(related_name=b'events', null=True, to='people.Group', blank=True)),
                ('idols', models.ManyToManyField(related_name=b'events', null=True, to='people.Idol', blank=True)),
                ('participating_groups', models.ManyToManyField(related_name=b'events_attributed_to', null=True, to='people.Group', blank=True)),
                ('participating_idols', models.ManyToManyField(help_text=b'The remaining idols that are not a member of the given groups.', related_name=b'events_attributed_to', null=True, to='people.Idol', blank=True)),
                ('submitted_by', models.ForeignKey(related_name=b'event_submissions', blank=True, to='accounts.Editor', null=True)),
            ],
            options={
                'get_latest_by': 'start_date',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('romanized_name', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('other_names', models.CharField(max_length=200, null=True, blank=True)),
                ('capacity', models.IntegerField(null=True, blank=True)),
                ('url', models.URLField(verbose_name=b'URL', blank=True)),
                ('slug', models.SlugField()),
                ('romanized_address', models.CharField(max_length=200, null=True, blank=True)),
                ('address', models.CharField(max_length=200, null=True, blank=True)),
                ('country', models.CharField(max_length=200, null=True, blank=True)),
                ('photo', models.ImageField(null=True, upload_to=b'events/venues/', blank=True)),
                ('edited_by', models.ManyToManyField(related_name=b'venues_edits', null=True, to='accounts.Editor', blank=True)),
                ('submitted_by', models.ForeignKey(related_name=b'venue_submissions', blank=True, to='accounts.Editor', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='activity',
            name='event',
            field=models.ForeignKey(related_name=b'activities', to='events.Event'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='submitted_by',
            field=models.ForeignKey(related_name=b'activity_submissions', blank=True, to='accounts.Editor', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='venue',
            field=models.ForeignKey(related_name=b'activities', blank=True, to='events.Venue', null=True),
            preserve_default=True,
        ),
    ]
