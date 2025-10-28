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
                ('description', models.TextField(help_text='If multiple activities took place on the same day/event, it can be specified here.', blank=True)),
                ('is_performance', models.BooleanField(default=False, verbose_name='is a performance?')),
                ('venue_known_as', models.CharField(help_text='Did the venue go by another name at the time of this activity?', max_length=200, blank=True)),
                ('edited_by', models.ManyToManyField(related_name='activitys_edits', null=True, to='accounts.Editor', blank=True)),
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
                ('category', models.CharField(default='general', max_length=16, choices=[('birthday', 'Birthday'), ('bustour', 'Bus Tour'), ('concert', 'Concert'), ('convention', 'Convention'), ('dinnershow', 'Dinner Show'), ('general', 'General'), ('hawaii', 'Hawaii'), ('live', 'Live'), ('release', 'Release'), ('promotional', 'Promotional'), ('other', 'Other')])),
                ('romanized_name', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('nickname', models.CharField(max_length=200)),
                ('slug', models.SlugField()),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('info_link_name', models.CharField(help_text='Separate multiple link names by comma (must have accompanying info link).', max_length=200, blank=True)),
                ('info_link', models.URLField(help_text='Seperate multiple links with comma (must have accompanying link name).', max_length=500, blank=True)),
                ('logo', models.ImageField(null=True, upload_to='events/events/', blank=True)),
                ('promotional_image', models.ImageField(null=True, upload_to='events/events/', blank=True)),
                ('stage', models.ImageField(null=True, upload_to='events/events/', blank=True)),
                ('has_handshake', models.BooleanField(default=False, verbose_name='has handshake?')),
                ('is_fanclu', models.BooleanField(default=False, verbose_name='fanclub?')),
                ('is_international', models.BooleanField(default=False, verbose_name='international?')),
                ('edited_by', models.ManyToManyField(related_name='events_edits', null=True, to='accounts.Editor', blank=True)),
                ('groups', models.ManyToManyField(related_name='events', null=True, to='people.Group', blank=True)),
                ('idols', models.ManyToManyField(related_name='events', null=True, to='people.Idol', blank=True)),
                ('participating_groups', models.ManyToManyField(related_name='events_attributed_to', null=True, to='people.Group', blank=True)),
                ('participating_idols', models.ManyToManyField(help_text='The remaining idols that are not a member of the given groups.', related_name='events_attributed_to', null=True, to='people.Idol', blank=True)),
                ('submitted_by', models.ForeignKey(on_delete=models.SET_NULL, related_name='event_submissions', blank=True, to='accounts.Editor', null=True)),
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
                ('url', models.URLField(verbose_name='URL', blank=True)),
                ('slug', models.SlugField()),
                ('romanized_address', models.CharField(max_length=200, null=True, blank=True)),
                ('address', models.CharField(max_length=200, null=True, blank=True)),
                ('country', models.CharField(max_length=200, null=True, blank=True)),
                ('photo', models.ImageField(null=True, upload_to='events/venues/', blank=True)),
                ('edited_by', models.ManyToManyField(related_name='venues_edits', null=True, to='accounts.Editor', blank=True)),
                ('submitted_by', models.ForeignKey(on_delete=models.SET_NULL, related_name='venue_submissions', blank=True, to='accounts.Editor', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='activity',
            name='event',
            field=models.ForeignKey(on_delete=models.SET_NULL, related_name='activities', to='events.Event'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='submitted_by',
            field=models.ForeignKey(on_delete=models.SET_NULL, related_name='activity_submissions', blank=True, to='accounts.Editor', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='venue',
            field=models.ForeignKey(on_delete=models.SET_NULL, related_name='activities', blank=True, to='events.Venue', null=True),
            preserve_default=True,
        ),
    ]
