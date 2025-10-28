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
                ('classification', models.PositiveSmallIntegerField(default=1, db_index=True, choices=[(1, b'Major Unit'), (2, b'Minor Unit'), (4, b'Temporary Unit'), (5, b'Sub-Unit'), (7, b'Supergroup'), (b'Special Units', [(3, b'Shuffle Unit'), (6, b'Revival Unit'), (8, b'Satoyama Unit'), (9, b'Satoumi Unit')]), (99, b'Other')])),
                ('status', models.PositiveSmallIntegerField(default=1, db_index=True, choices=[(1, b'Active'), (2, b'Former'), (99, b'Other')])),
                ('scope', models.PositiveSmallIntegerField(default=1, db_index=True, choices=[(1, b'Hello! Project'), (b'Up-Front', [(11, b'Up-Front Create'), (12, b'Just Production'), (13, b'J.P ROOM')]), (99, b'Other')])),
                ('started', models.DateField(db_index=True)),
                ('ended', models.DateField(db_index=True, null=True, blank=True)),
                ('former_names', models.CharField(max_length=200, blank=True)),
                ('note', models.TextField(blank=True)),
                ('photo', models.ImageField(upload_to=b'people/%(class)ss/', blank=True)),
                ('photo_thumbnail', models.ImageField(upload_to=b'people/%(class)ss/', blank=True)),
                ('edited_by', models.ManyToManyField(related_name=b'groups_edits', null=True, to='accounts.Editor', blank=True)),
                ('groups', models.ManyToManyField(related_name=b'supergroups', null=True, to='people.Group', blank=True)),
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
                ('kind', models.PositiveSmallIntegerField(default=1, choices=[(1, b'Promotional Photo'), (2, b'Blog Photo'), (99, b'Other')])),
                ('photo', models.ImageField(upload_to=b'people/groups/', blank=True)),
                ('photo_thumbnail', models.ImageField(upload_to=b'people/groups/', blank=True)),
                ('taken', models.DateField()),
                ('group', models.ForeignKey(related_name=b'photos', to='people.Group')),
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
                ('kind', models.PositiveSmallIntegerField(default=1, choices=[(1, b'Promotional Photo'), (2, b'Blog Photo'), (99, b'Other')])),
                ('photo', models.ImageField(upload_to=b'people/idols/', blank=True)),
                ('photo_thumbnail', models.ImageField(upload_to=b'people/idols/', blank=True)),
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
                ('birthdate_dayofyear', models.PositiveSmallIntegerField(default=None, null=True, editable=False)),
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
                ('status', models.PositiveSmallIntegerField(default=1, db_index=True, choices=[(1, b'Active'), (2, b'Former'), (99, b'Other')])),
                ('scope', models.PositiveSmallIntegerField(default=1, db_index=True, choices=[(1, b'Hello! Project'), (b'Up-Front', [(11, b'Up-Front Create'), (12, b'Just Production'), (13, b'J.P ROOM')]), (99, b'Other')])),
                ('bloodtype', models.CharField(default=b'A', max_length=2, blank=True, choices=[(b'A', b'A'), (b'B', b'B'), (b'O', b'O'), (b'AB', b'AB')])),
                ('height', models.DecimalField(null=True, max_digits=4, decimal_places=1, blank=True)),
                ('color', models.CharField(default=b'', help_text=b"An idol's color. Use a hex value (i.e. #000000).", max_length=7, blank=True)),
                ('started', models.DateField(help_text=b'The date this idol joined Hello! Project/became an idol.', null=True, db_index=True, blank=True)),
                ('graduated', models.DateField(help_text=b'The date this idol graduated from Hello! Project.', null=True, db_index=True, blank=True)),
                ('retired', models.DateField(help_text=b'The date this idol retired.', null=True, db_index=True, blank=True)),
                ('birthdate', apps.ohashi.db.models.fields.birthdays.BirthdayField(db_index=True, null=True, blank=True)),
                ('birthplace', models.CharField(max_length=200, blank=True)),
                ('birthplace_romanized', models.CharField(max_length=200, blank=True)),
                ('birthplace_latitude', models.FloatField(null=True, blank=True)),
                ('birthplace_longitude', models.FloatField(null=True, blank=True)),
                ('note', models.TextField(blank=True)),
                ('photo', models.ImageField(upload_to=b'people/%(class)ss/', blank=True)),
                ('photo_thumbnail', models.ImageField(upload_to=b'people/%(class)ss/', blank=True)),
                ('edited_by', models.ManyToManyField(related_name=b'idols_edits', null=True, to='accounts.Editor', blank=True)),
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
                ('is_primary', models.BooleanField(default=False, db_index=True, verbose_name=b'Primary?')),
                ('started', models.DateField(db_index=True)),
                ('ended', models.DateField(db_index=True, null=True, blank=True)),
                ('generation', models.PositiveSmallIntegerField(db_index=True, null=True, blank=True)),
                ('is_leader', models.BooleanField(default=False, verbose_name=b'Leader?')),
                ('leadership_started', models.DateField(null=True, blank=True)),
                ('leadership_ended', models.DateField(null=True, blank=True)),
                ('group', apps.ohashi.db.models.fields.CustomManagerForeignKey(related_name=b'memberships', blank=True, to='people.Group', null=True)),
                ('idol', models.ForeignKey(related_name=b'memberships', to='people.Idol')),
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
                ('edited_by', models.ManyToManyField(related_name=b'staffs_edits', null=True, to='accounts.Editor', blank=True)),
                ('submitted_by', models.ForeignKey(related_name=b'staff_submissions', blank=True, to='accounts.Editor', null=True)),
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
            field=models.ForeignKey(related_name=b'primary', blank=True, to='people.Membership', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='idol',
            name='submitted_by',
            field=models.ForeignKey(related_name=b'idol_submissions', blank=True, to='accounts.Editor', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='headshot',
            name='idol',
            field=models.ForeignKey(related_name=b'photos', to='people.Idol'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(related_name=b'groups', through='people.Membership', to='people.Idol'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='parent',
            field=models.ForeignKey(related_name=b'subgroups', blank=True, to='people.Group', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='submitted_by',
            field=models.ForeignKey(related_name=b'group_submissions', blank=True, to='accounts.Editor', null=True),
            preserve_default=True,
        ),
    ]
