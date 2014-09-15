# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Venue.romanized_address'
        db.alter_column(u'events_venue', 'romanized_address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Venue.country'
        db.alter_column(u'events_venue', 'country', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Venue.address'
        db.alter_column(u'events_venue', 'address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Event.info_link'
        db.alter_column(u'events_event', 'info_link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))

        # Changing field 'Event.nickname'
        db.alter_column(u'events_event', 'nickname', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))
        # Adding field 'Performance.romanized_name'
        db.add_column(u'events_performance', 'romanized_name',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Performance.name'
        db.add_column(u'events_performance', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):

        # Changing field 'Venue.romanized_address'
        db.alter_column(u'events_venue', 'romanized_address', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

        # Changing field 'Venue.country'
        db.alter_column(u'events_venue', 'country', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

        # Changing field 'Venue.address'
        db.alter_column(u'events_venue', 'address', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

        # Changing field 'Event.info_link'
        db.alter_column(u'events_event', 'info_link', self.gf('django.db.models.fields.URLField')(default='', max_length=200))

        # Changing field 'Event.nickname'
        db.alter_column(u'events_event', 'nickname', self.gf('django.db.models.fields.CharField')(default='', max_length=30))
        # Deleting field 'Performance.romanized_name'
        db.delete_column(u'events_performance', 'romanized_name')

        # Deleting field 'Performance.name'
        db.delete_column(u'events_performance', 'name')


    models = {
        u'events.event': {
            'Meta': {'object_name': 'Event'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'events.performance': {
            'Meta': {'object_name': 'Performance'},
            'day': ('django.db.models.fields.DateField', [], {}),
            'end_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'schedule'", 'to': u"orm['events.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'performances'", 'null': 'True', 'to': u"orm['events.Venue']"})
        },
        u'events.venue': {
            'Meta': {'object_name': 'Venue'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'romanized_address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['events']