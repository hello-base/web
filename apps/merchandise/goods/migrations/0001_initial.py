# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('events', '0001_initial'),
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Base',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('romanized_name', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('released', models.DateField(db_index=True, null=True, blank=True)),
                ('price', models.IntegerField(null=True, blank=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('is_graduation_good', models.BooleanField(default=False, verbose_name='graduation good?')),
                ('is_birthday_good', models.BooleanField(default=False, verbose_name='birthday good?')),
                ('is_online_exclusive', models.BooleanField(default=False, verbose_name='online exclusive?')),
                ('is_mailorder_exclusive', models.BooleanField(default=False, verbose_name='mail-order exclusive?')),
                ('online_id', models.CharField(help_text=b"The good's ID or catalog number (if available).", max_length=16, null=True, verbose_name='online ID', blank=True)),
                ('other_info', models.TextField(help_text='Any additional information about the good. Size, restrictions, etc.', null=True, blank=True)),
                ('available_from', models.DateField(help_text='When was the good originally released?', null=True, blank=True)),
                ('available_until', models.DateField(help_text='When was the good taken off the market?', null=True, blank=True)),
                ('link', models.URLField(blank=True)),
                ('image', models.ImageField(upload_to='/', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Good',
            fields=[
                ('base_ptr', models.OneToOneField(on_delete=models.CASCADE, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='goods.Base')),
                ('category', models.CharField(max_length=16, choices=[('Photos', [('2lphoto', '2L-size Photo'), ('A4photo', 'A4-size Photo'), ('A5photo', 'A5-wide Photo'), ('collectionphoto', 'Collection Photo'), ('lmetallic', 'L-size Metallic Photo'), ('lphoto', 'L-size Photo'), ('photocard', 'Photo Card'), ('postcardphoto', 'Postcard-size Photo'), ('tradingcardphoto', 'Trading Card-size Photo')]), ('Posters', [('pinup', 'Pin-up Poster'), ('a2poster', 'A2-size Poster'), ('b1poster', 'B1-size Poster'), ('b2poster', 'B2-size Poster')]), ('Merchandise', [('badge', 'Badge'), ('bandana', 'Bandana'), ('clearfile', 'Clear File'), ('costume', 'Costume Good'), ('dvd', 'DVD'), ('gachagacha', 'GachaGacha Collection Item'), ('hoodie', 'Hoodie'), ('keyholder', 'Keyholder'), ('microfiber', 'Microfiber Towel'), ('muffler', 'Muffler Towel'), ('scrunchie', 'Scrunchie'), ('strap', 'Strap/Charm'), ('tourbag', 'Tour Bag'), ('tradingcard', 'Trading Card'), ('tshirt', 'T-shirt'), ('uchiwa', 'Uchiwa'), ('visualbook', 'Visual Book/Pamphlet'), ('visualscreen', 'Visual Screen'), ('wristband', 'Wristband')]), ('Other', [('collectionitem', 'Other Collection Item'), ('poster', 'Other Poster'), ('towel', 'Other Towel'), ('other', 'Other')])])),
                ('is_bonus_good', models.BooleanField(default=False, verbose_name='bonus good?')),
                ('is_campaign_good', models.BooleanField(default=False, verbose_name='campaign good?')),
                ('is_lottery_good', models.BooleanField(default=False, verbose_name='lottery good?')),
                ('is_set_exclusive', models.BooleanField(default=False, verbose_name='set exclusive?')),
            ],
            options={
                'abstract': False,
            },
            bases=('goods.base',),
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('base_ptr', models.OneToOneField(on_delete=models.CASCADE, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='goods.Base')),
                ('category', models.CharField(max_length=18, choices=[('bandanaset', 'Bandana Set'), ('clearfileset', 'Clear File Set'), ('collectionphotoset', 'Collection Photo Set'), ('gachagachaset', 'GachaGacha Collection Set'), ('keyholderset', 'Keyholder Set'), ('parkaset', 'Parka Set'), ('pinupset', 'Pin-up Poster Set'), ('scrunchieset', 'Scrunchie Set'), ('strapset', 'Strap/Charm Set'), ('tshirtset', 'T-shirt Set'), ('collectionset', 'Other Collection Set'), ('otherset', 'Other Set')])),
            ],
            options={
                'abstract': False,
            },
            bases=('goods.base',),
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('romanized_name', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200, blank=True)),
                ('website_link', models.URLField(blank=True)),
                ('slug', models.SlugField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SuperSet',
            fields=[
                ('base_ptr', models.OneToOneField(on_delete=models.CASCADE, parent_link=True, auto_created=True, primary_key=True, serialize=False, to='goods.Base')),
                ('goods', models.ManyToManyField(to='goods.Good')),
                ('sets', models.ManyToManyField(to='goods.Set')),
            ],
            options={
                'verbose_name': 'superset',
            },
            bases=('goods.base',),
        ),
        migrations.AddField(
            model_name='good',
            name='parent',
            field=models.ForeignKey(on_delete=models.SET_NULL, blank=True, to='goods.Set', help_text='Is this good a part of another good? (e.g., a photo that is part of a set)', null=True, verbose_name='parent good'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='base',
            name='edited_by',
            field=models.ManyToManyField(related_name='bases_edits', null=True, to='accounts.Editor', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='base',
            name='event',
            field=models.ForeignKey(on_delete=models.SET_NULL, blank=True, to='events.Event', help_text='Is this good from an event?', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='base',
            name='groups',
            field=models.ManyToManyField(related_name='bases', null=True, to='people.Group', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='base',
            name='idols',
            field=models.ManyToManyField(related_name='bases', null=True, to='people.Idol', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='base',
            name='participating_groups',
            field=models.ManyToManyField(related_name='bases_attributed_to', null=True, to='people.Group', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='base',
            name='participating_idols',
            field=models.ManyToManyField(help_text='The remaining idols that are not a member of the given groups.', related_name='bases_attributed_to', null=True, to='people.Idol', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='base',
            name='shop',
            field=models.ForeignKey(on_delete=models.SET_NULL, blank=True, to='goods.Shop', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='base',
            name='submitted_by',
            field=models.ForeignKey(on_delete=models.SET_NULL, related_name='base_submissions', blank=True, to='accounts.Editor', null=True),
            preserve_default=True,
        ),
    ]
