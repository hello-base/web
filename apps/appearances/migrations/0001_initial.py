# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(null=True, blank=True)),
                ('image', models.ImageField(upload_to='appearances/cards/', blank=True)),
                ('other_model_romanized_name', models.CharField(max_length=200, verbose_name='model (romanized name)', blank=True)),
                ('other_model_name', models.CharField(max_length=200, verbose_name='model (name)', blank=True)),
                ('other_member_of_romanized_name', models.CharField(max_length=200, verbose_name='member of (romanized name)', blank=True)),
                ('other_member_of_name', models.CharField(max_length=200, verbose_name='member of (name)', blank=True)),
                ('other_group_romanized_name', models.CharField(max_length=200, verbose_name='group (romanized name)', blank=True)),
                ('other_group_name', models.CharField(max_length=200, verbose_name='group (name)', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CardSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('romanized_name', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200, blank=True)),
                ('image', models.ImageField(upload_to='appearances/cards/', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('air_date', models.DateField()),
                ('is_coverage', models.BooleanField(default=False, verbose_name='is coverage?')),
                ('record_date', models.DateField(null=True, blank=True)),
                ('romanized_name', models.CharField(max_length=200, blank=True)),
                ('name', models.CharField(max_length=200, blank=True)),
                ('number', models.IntegerField(null=True, blank=True)),
                ('video_link', models.URLField(max_length=500, blank=True)),
                ('episode', models.ForeignKey(on_delete=models.SET_NULL, related_name='continuation', blank=True, to='appearances.Episode', null=True)),
                ('groups', models.ManyToManyField(related_name='episodes', null=True, to='people.Group', blank=True)),
                ('idols', models.ManyToManyField(related_name='episodes', null=True, to='people.Idol', blank=True)),
                ('participating_groups', models.ManyToManyField(related_name='episodes_attributed_to', null=True, to='people.Group', blank=True)),
                ('participating_idols', models.ManyToManyField(help_text='The remaining idols that are not a member of the given groups.', related_name='episodes_attributed_to', null=True, to='people.Idol', blank=True)),
            ],
            options={
                'ordering': ('show', 'air_date'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.IntegerField(help_text='If different from magazine price.', null=True, blank=True)),
                ('volume', models.CharField(help_text='Leave blank if no volume number (but fill out month or week).', max_length=10, blank=True)),
                ('volume_month', models.DateField(help_text='1st day of the month. Leave blank for weekly magazines.', null=True, blank=True)),
                ('volume_week', models.DateField(help_text='Leave blank for monthly magazines.', null=True, blank=True)),
                ('release_date', models.DateField(null=True, blank=True)),
                ('catalog_number', models.CharField(help_text='Most magazines dont have this, NEOBK is just a Neowing ID.', max_length=30, blank=True)),
                ('isbn_number', models.CharField(help_text='JAN number works too, its like a Japanese ISBN.', max_length=20, blank=True)),
                ('cover', models.ImageField(upload_to='appearances/issues/', blank=True)),
                ('groups', models.ManyToManyField(related_name='issues', null=True, to='people.Group', blank=True)),
                ('idols', models.ManyToManyField(related_name='issues', null=True, to='people.Idol', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IssueImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to='appearances/issues/', blank=True)),
                ('issue', models.ForeignKey(on_delete=models.SET_NULL, related_name='gallery', to='appearances.Issue')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Magazine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('romanized_name', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('price', models.IntegerField(null=True, blank=True)),
                ('slug', models.SlugField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('romanized_name', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('slug', models.SlugField()),
                ('aired_from', models.DateField(null=True, blank=True)),
                ('aired_until', models.DateField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(null=True, blank=True)),
                ('end_time', models.DateTimeField(null=True, blank=True)),
                ('show', models.ForeignKey(on_delete=models.SET_NULL, to='appearances.Show')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='issue',
            name='magazine',
            field=models.ForeignKey(on_delete=models.SET_NULL, related_name='issues', to='appearances.Magazine'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='participating_groups',
            field=models.ManyToManyField(related_name='issues_attributed_to', null=True, to='people.Group', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='participating_idols',
            field=models.ManyToManyField(help_text='The remaining idols that are not a member of the given groups.', related_name='issues_attributed_to', null=True, to='people.Idol', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='episode',
            name='show',
            field=models.ForeignKey(on_delete=models.SET_NULL, to='appearances.Show'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cardset',
            name='issue',
            field=models.ForeignKey(on_delete=models.SET_NULL, related_name='sets', to='appearances.Issue'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='cardset',
            field=models.ForeignKey(on_delete=models.SET_NULL, blank=True, to='appearances.CardSet', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='group',
            field=models.ForeignKey(on_delete=models.SET_NULL, related_name='cards', blank=True, to='people.Group', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='hp_model',
            field=models.ForeignKey(on_delete=models.SET_NULL, related_name='cards', verbose_name='H!P model', blank=True, to='people.Idol', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='issue',
            field=models.ForeignKey(on_delete=models.SET_NULL, related_name='cards', to='appearances.Issue'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='member_of',
            field=models.ForeignKey(on_delete=models.SET_NULL, related_name='idol', blank=True, to='people.Group', null=True),
            preserve_default=True,
        ),
    ]
