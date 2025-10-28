# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appearances', '0001_initial'),
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(blank=True)),
                ('album', models.ForeignKey(on_delete=models.SET_NULL, related_name='purchase_links', blank=True, to='music.Album', null=True)),
                ('issue', models.ForeignKey(on_delete=models.SET_NULL, related_name='purchase_links', blank=True, to='appearances.Issue', null=True)),
                ('single', models.ForeignKey(on_delete=models.SET_NULL, related_name='purchase_links', blank=True, to='music.Single', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('romanized_name', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200, blank=True)),
                ('url', models.URLField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='purchaselink',
            name='store',
            field=models.ForeignKey(on_delete=models.SET_NULL, to='stores.Store'),
            preserve_default=True,
        ),
    ]
