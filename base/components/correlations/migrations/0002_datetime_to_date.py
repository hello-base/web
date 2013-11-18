# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Correlation.timestamp'
        db.alter_column(u'correlations_correlation', 'timestamp', self.gf('django.db.models.fields.DateField')())

    def backwards(self, orm):

        # Changing field 'Correlation.timestamp'
        db.alter_column(u'correlations_correlation', 'timestamp', self.gf('django.db.models.fields.DateTimeField')())

    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'correlations.correlation': {
            'Meta': {'ordering': "(u'-timestamp',)", 'object_name': 'Correlation'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'date_field': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'day': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2'}),
            'descrption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'julian': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '3'}),
            'month': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '2'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '4'})
        }
    }

    complete_apps = ['correlations']