# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.ohashi.db.models.fields
import django.utils.timezone
import model_utils.fields
import apps.ohashi.db.models.fields.birthdays


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=60)),
                ('romanized_name', models.CharField(max_length=60)),
                ('slug', models.SlugField()),
                ('classification', models.PositiveSmallIntegerField(default=1, db_index=True, choices=[(1, 'Major Unit'), (2, 'Minor Unit'), (4, 'Temporary Unit'), (5, 'Sub-Unit'), (7, 'Supergroup'), ('Special Units', [(3, 'Shuffle Unit'), (6, 'Revival Unit'), (8, 'Satoyama Unit'), (9, 'Satoumi Unit')]), (99, 'Other')])),
                ('status', models.PositiveSmallIntegerField(default=1, db_index=True, choices=[(1, 'Active'), (2, 'Former'), (99, 'Other')])),
                ('scope', models.PositiveSmallIntegerField(default=1, db_index=True, choices=[(1, 'Hello! Project'), ('Up-Front', [(11, 'Up-Front Create'), (12, 'Just Production'), (13, 'J.P ROOM')]), (99, 'Other')])),
                ('started', models.DateField(db_index=True)),
                ('ended', models.DateField(db_index=True, null=True, blank=True)),
                ('former_names', models.CharField(max_length=200, blank=True)),
                ('note', models.TextField(blank=True)),
                ('photo', models.ImageField(upload_to='people/%(class)ss/', blank=True)),
                ('photo_thumbnail', models.ImageField(upload_to='people/%(class)ss/', blank=True)),
                ('edited_by', models.ManyToManyField(related_name='groups_edits', null=True, to='accounts.Editor', blank=True)),
                ('groups', models.ManyToManyField(related_name='supergroups', null=True, to='people.Group', blank=True)),
            ],
            options={
                'ordering': ('started',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Groupshot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.PositiveSmallIntegerField(default=1, choices=[(1, 'Promotional Photo'), (2, 'Blog Photo'), (99, 'Other')])),
                ('photo', models.ImageField(upload_to='people/groups/', blank=True)),
                ('photo_thumbnail', models.ImageField(upload_to='people/groups/', blank=True)),
                ('taken', models.DateField()),
                ('group', models.ForeignKey(on_delete=models.SET_NULL, related_name='photos', to='people.Group')),
            ],
            options={
                'ordering': ('-taken',),
                'get_latest_by': 'taken',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Headshot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.PositiveSmallIntegerField(default=1, choices=[(1, 'Promotional Photo'), (2, 'Blog Photo'), (99, 'Other')])),
                ('photo', models.ImageField(upload_to='people/idols/', blank=True)),
                ('photo_thumbnail', models.ImageField(upload_to='people/idols/', blank=True)),
                ('taken', models.DateField()),
            ],
            options={
                'ordering': ('-taken',),
                'get_latest_by': 'taken',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Idol',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=60, editable=False)),
                ('family_name', models.CharField(max_length=30, blank=True)),
                ('given_name', models.CharField(max_length=30, blank=True)),
                ('alias', models.CharField(max_length=60, blank=True)),
                ('romanized_name', models.CharField(max_length=60, editable=False)),
                ('romanized_family_name', models.CharField(max_length=30, blank=True)),
                ('romanized_given_name', models.CharField(max_length=30, blank=True)),
                ('romanized_alias', models.CharField(max_length=60, blank=True)),
                ('nicknames', models.CharField(max_length=200, blank=True)),
                ('slug', models.SlugField()),
                ('status', models.PositiveSmallIntegerField(default=1, db_index=True, choices=[(1, 'Active'), (2, 'Former'), (99, 'Other')])),
                ('scope', models.PositiveSmallIntegerField(default=1, db_index=True, choices=[(1, 'Hello! Project'), ('Up-Front', [(11, 'Up-Front Create'), (12, 'Just Production'), (13, 'J.P ROOM')]), (99, 'Other')])),
                ('bloodtype', models.CharField(default='A', max_length=2, blank=True, choices=[('A', 'A'), ('B', 'B'), ('O', 'O'), ('AB', 'AB')])),
                ('height', models.DecimalField(null=True, max_digits=4, decimal_places=1, blank=True)),
                ('color', models.CharField(default='', help_text=b"An idol's color. Use a hex value (i.e. #000000).", max_length=7, blank=True)),
                ('started', models.DateField(help_text='The date this idol joined Hello! Project/became an idol.', null=True, db_index=True, blank=True)),
                ('graduated', models.DateField(help_text='The date this idol graduated from Hello! Project.', null=True, db_index=True, blank=True)),
                ('retired', models.DateField(help_text='The date this idol retired.', null=True, db_index=True, blank=True)),
                ('birthdate', apps.ohashi.db.models.fields.birthdays.BirthdayField(db_index=True, null=True, blank=True)),
                ('birthplace', models.CharField(max_length=200, blank=True)),
                ('birthplace_romanized', models.CharField(max_length=200, blank=True)),
                ('birthplace_latitude', models.FloatField(null=True, blank=True)),
                ('birthplace_longitude', models.FloatField(null=True, blank=True)),
                ('note', models.TextField(blank=True)),
                ('photo', models.ImageField(upload_to='people/%(class)ss/', blank=True)),
                ('photo_thumbnail', models.ImageField(upload_to='people/%(class)ss/', blank=True)),
                ('edited_by', models.ManyToManyField(related_name='idols_edits', null=True, to='accounts.Editor', blank=True)),
            ],
            options={
                'ordering': ('birthdate',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_primary', models.BooleanField(default=False, db_index=True, verbose_name='Primary?')),
                ('started', models.DateField(db_index=True)),
                ('ended', models.DateField(db_index=True, null=True, blank=True)),
                ('generation', models.PositiveSmallIntegerField(db_index=True, null=True, blank=True)),
                ('is_leader', models.BooleanField(default=False, verbose_name='Leader?')),
                ('leadership_started', models.DateField(null=True, blank=True)),
                ('leadership_ended', models.DateField(null=True, blank=True)),
                ('group', apps.ohashi.db.models.fields.CustomManagerForeignKey(on_delete=models.SET_NULL, related_name='memberships', blank=True, to='people.Group', null=True)),
                ('idol', models.ForeignKey(on_delete=models.SET_NULL, related_name='memberships', to='people.Idol')),
            ],
            options={
                'ordering': ('-is_primary', '-started', '-idol__birthdate'),
                'get_latest_by': 'started',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=60, editable=False)),
                ('family_name', models.CharField(max_length=30, blank=True)),
                ('given_name', models.CharField(max_length=30, blank=True)),
                ('alias', models.CharField(max_length=60, blank=True)),
                ('romanized_name', models.CharField(max_length=60, editable=False)),
                ('romanized_family_name', models.CharField(max_length=30, blank=True)),
                ('romanized_given_name', models.CharField(max_length=30, blank=True)),
                ('romanized_alias', models.CharField(max_length=60, blank=True)),
                ('nicknames', models.CharField(max_length=200, blank=True)),
                ('slug', models.SlugField()),
                ('edited_by', models.ManyToManyField(related_name='staffs_edits', null=True, to='accounts.Editor', blank=True)),
                ('submitted_by', models.ForeignKey(on_delete=models.SET_NULL, related_name='staff_submissions', blank=True, to='accounts.Editor', null=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'staff',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('idol', 'group')]),
        ),
        migrations.AddField(
            model_name='idol',
            name='primary_membership',
            field=models.ForeignKey(on_delete=models.SET_NULL, related_name='primary', blank=True, to='people.Membership', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='idol',
            name='submitted_by',
            field=models.ForeignKey(on_delete=models.SET_NULL, related_name='idol_submissions', blank=True, to='accounts.Editor', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='headshot',
            name='idol',
            field=models.ForeignKey(on_delete=models.SET_NULL, related_name='photos', to='people.Idol'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(related_name='groups', through='people.Membership', to='people.Idol'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='parent',
            field=models.ForeignKey(on_delete=models.SET_NULL, related_name='subgroups', blank=True, to='people.Group', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='submitted_by',
            field=models.ForeignKey(on_delete=models.SET_NULL, related_name='group_submissions', blank=True, to='accounts.Editor', null=True),
            preserve_default=True,
        ),
    ]
