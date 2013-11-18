# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Correlation'
        db.create_table(u'correlations_correlation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.IntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('date_field', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('descrption', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('julian', self.gf('django.db.models.fields.PositiveSmallIntegerField')(max_length=3)),
            ('year', self.gf('django.db.models.fields.PositiveSmallIntegerField')(max_length=4)),
            ('month', self.gf('django.db.models.fields.PositiveSmallIntegerField')(max_length=2)),
            ('day', self.gf('django.db.models.fields.PositiveSmallIntegerField')(max_length=2)),
        ))
        db.send_create_signal(u'correlations', ['Correlation'])


    def backwards(self, orm):
        # Deleting model 'Correlation'
        db.delete_table(u'correlations_correlation')


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
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '4'})
        }
    }

    complete_apps = ['correlations']