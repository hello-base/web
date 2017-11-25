# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
        ('accounts', '0001_initial'),
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('romanized_name', models.CharField(help_text=b'This should be filled out if there is no coorresponding track or if the clip was an MC.', max_length=200, blank=True)),
                ('name', models.CharField(max_length=200, blank=True)),
                ('disc', models.PositiveSmallIntegerField(default=1)),
                ('position', models.PositiveSmallIntegerField()),
            ],
            options={
                'ordering': ('format', 'disc', 'position'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Videodisc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('romanized_name', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('released', models.DateField(db_index=True, null=True, blank=True)),
                ('price', models.IntegerField(null=True, blank=True)),
                ('uuid', models.UUIDField(max_length=36, editable=False, blank=True)),
                ('kind', models.IntegerField(default=2, choices=[(b'Performances', [(1, b'Best Shot'), (2, b'Concert'), (3, b'Movie'), (4, b'Musical'), (5, b'Stage Play'), (6, b'Visual')]), (b'Compilations', [(11, b'PV Collections'), (12, b'Television Segments')]), (99, b'Other')])),
                ('slug', models.SlugField(blank=True)),
                ('edited_by', models.ManyToManyField(related_name=b'videodiscs_edits', null=True, to='accounts.Editor', blank=True)),
                ('groups', models.ManyToManyField(related_name=b'videodiscs', null=True, to='people.Group', blank=True)),
                ('idols', models.ManyToManyField(related_name=b'videodiscs', null=True, to='people.Idol', blank=True)),
                ('participating_groups', models.ManyToManyField(related_name=b'videodiscs_attributed_to', null=True, to='people.Group', blank=True)),
                ('participating_idols', models.ManyToManyField(help_text=b'The remaining idols that are not a member of the given groups.', related_name=b'videodiscs_attributed_to', null=True, to='people.Idol', blank=True)),
                ('submitted_by', models.ForeignKey(related_name=b'videodisc_submissions', blank=True, to='accounts.Editor', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VideodiscFormat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.IntegerField(default=1, choices=[(1, b'DVD'), (2, b'Blu-ray Disc')])),
                ('released', models.DateField(db_index=True, null=True, blank=True)),
                ('catalog_number', models.CharField(max_length=25, blank=True)),
                ('art', models.ImageField(null=True, upload_to=b'merchandise/media/videos/', blank=True)),
                ('clips', models.ManyToManyField(related_name=b'videos', null=True, through='media.Clip', to='music.Track', blank=True)),
                ('parent', models.ForeignKey(related_name=b'formats', blank=True, to='media.Videodisc', null=True)),
            ],
            options={
                'ordering': ('-released',),
                'get_latest_by': 'released',
                'verbose_name': 'format',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='clip',
            name='format',
            field=models.ForeignKey(related_name=b'order', to='media.VideodiscFormat'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clip',
            name='groups',
            field=models.ManyToManyField(related_name=b'clips', null=True, to='people.Group', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clip',
            name='idols',
            field=models.ManyToManyField(related_name=b'clips', null=True, to='people.Idol', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clip',
            name='participating_groups',
            field=models.ManyToManyField(related_name=b'clips_attributed_to', null=True, to='people.Group', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clip',
            name='participating_idols',
            field=models.ManyToManyField(help_text=b'The remaining idols that are not a member of the given groups.', related_name=b'clips_attributed_to', null=True, to='people.Idol', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clip',
            name='track',
            field=models.ForeignKey(related_name=b'on_formats', blank=True, to='music.Track', null=True),
            preserve_default=True,
        ),
    ]
