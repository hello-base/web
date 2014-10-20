# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields
import django_extensions.db.fields


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
                ('uuid', django_extensions.db.fields.UUIDField(max_length=36, editable=False, blank=True)),
                ('is_graduation_good', models.BooleanField(default=False, verbose_name=b'graduation good?')),
                ('is_birthday_good', models.BooleanField(default=False, verbose_name=b'birthday good?')),
                ('is_online_exclusive', models.BooleanField(default=False, verbose_name=b'online exclusive?')),
                ('is_mailorder_exclusive', models.BooleanField(default=False, verbose_name=b'mail-order exclusive?')),
                ('online_id', models.CharField(help_text=b"The good's ID or catalog number (if available).", max_length=16, null=True, verbose_name=b'online ID', blank=True)),
                ('other_info', models.TextField(help_text=b'Any additional information about the good. Size, restrictions, etc.', null=True, blank=True)),
                ('available_from', models.DateField(help_text=b'When was the good originally released?', null=True, blank=True)),
                ('available_until', models.DateField(help_text=b'When was the good taken off the market?', null=True, blank=True)),
                ('link', models.URLField(blank=True)),
                ('image', models.ImageField(upload_to=b'/', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Good',
            fields=[
                ('base_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='goods.Base')),
                ('category', models.CharField(max_length=16, choices=[(b'Photos', [(b'2lphoto', b'2L-size Photo'), (b'A4photo', b'A4-size Photo'), (b'A5photo', b'A5-wide Photo'), (b'collectionphoto', b'Collection Photo'), (b'lmetallic', b'L-size Metallic Photo'), (b'lphoto', b'L-size Photo'), (b'photocard', b'Photo Card'), (b'postcardphoto', b'Postcard-size Photo'), (b'tradingcardphoto', b'Trading Card-size Photo')]), (b'Posters', [(b'pinup', b'Pin-up Poster'), (b'a2poster', b'A2-size Poster'), (b'b1poster', b'B1-size Poster'), (b'b2poster', b'B2-size Poster')]), (b'Merchandise', [(b'badge', b'Badge'), (b'bandana', b'Bandana'), (b'clearfile', b'Clear File'), (b'costume', b'Costume Good'), (b'dvd', b'DVD'), (b'gachagacha', b'GachaGacha Collection Item'), (b'hoodie', b'Hoodie'), (b'keyholder', b'Keyholder'), (b'microfiber', b'Microfiber Towel'), (b'muffler', b'Muffler Towel'), (b'scrunchie', b'Scrunchie'), (b'strap', b'Strap/Charm'), (b'tourbag', b'Tour Bag'), (b'tradingcard', b'Trading Card'), (b'tshirt', b'T-shirt'), (b'uchiwa', b'Uchiwa'), (b'visualbook', b'Visual Book/Pamphlet'), (b'visualscreen', b'Visual Screen'), (b'wristband', b'Wristband')]), (b'Other', [(b'collectionitem', b'Other Collection Item'), (b'poster', b'Other Poster'), (b'towel', b'Other Towel'), (b'other', b'Other')])])),
                ('is_bonus_good', models.BooleanField(default=False, verbose_name=b'bonus good?')),
                ('is_campaign_good', models.BooleanField(default=False, verbose_name=b'campaign good?')),
                ('is_lottery_good', models.BooleanField(default=False, verbose_name=b'lottery good?')),
                ('is_set_exclusive', models.BooleanField(default=False, verbose_name=b'set exclusive?')),
            ],
            options={
                'abstract': False,
            },
            bases=('goods.base',),
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('base_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='goods.Base')),
                ('category', models.CharField(max_length=18, choices=[(b'bandanaset', b'Bandana Set'), (b'clearfileset', b'Clear File Set'), (b'collectionphotoset', b'Collection Photo Set'), (b'gachagachaset', b'GachaGacha Collection Set'), (b'keyholderset', b'Keyholder Set'), (b'parkaset', b'Parka Set'), (b'pinupset', b'Pin-up Poster Set'), (b'scrunchieset', b'Scrunchie Set'), (b'strapset', b'Strap/Charm Set'), (b'tshirtset', b'T-shirt Set'), (b'collectionset', b'Other Collection Set'), (b'otherset', b'Other Set')])),
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
                ('base_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='goods.Base')),
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
            field=models.ForeignKey(blank=True, to='goods.Set', help_text=b'Is this good a part of another good? (e.g., a photo that is part of a set)', null=True, verbose_name='parent good'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='base',
            name='edited_by',
            field=models.ManyToManyField(related_name=b'bases_edits', null=True, to='accounts.Editor', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='base',
            name='event',
            field=models.ForeignKey(blank=True, to='events.Event', help_text=b'Is this good from an event?', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='base',
            name='groups',
            field=models.ManyToManyField(related_name=b'bases', null=True, to='people.Group', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='base',
            name='idols',
            field=models.ManyToManyField(related_name=b'bases', null=True, to='people.Idol', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='base',
            name='participating_groups',
            field=models.ManyToManyField(related_name=b'bases_attributed_to', null=True, to='people.Group', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='base',
            name='participating_idols',
            field=models.ManyToManyField(help_text=b'The remaining idols that are not a member of the given groups.', related_name=b'bases_attributed_to', null=True, to='people.Idol', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='base',
            name='shop',
            field=models.ForeignKey(blank=True, to='goods.Shop', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='base',
            name='submitted_by',
            field=models.ForeignKey(related_name=b'base_submissions', blank=True, to='accounts.Editor', null=True),
            preserve_default=True,
        ),
    ]
