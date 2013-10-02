# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Venue.created'
        db.add_column(u'events_venue', 'created',
                      self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Venue.modified'
        db.add_column(u'events_venue', 'modified',
                      self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Venue.submitted_by'
        db.add_column(u'events_venue', 'submitted_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='venue_submissions', null=True, to=orm['accounts.Editor']),
                      keep_default=False)

        # Adding M2M table for field edited_by on 'Venue'
        m2m_table_name = db.shorten_name(u'events_venue_edited_by')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('venue', models.ForeignKey(orm[u'events.venue'], null=False)),
            ('editor', models.ForeignKey(orm[u'accounts.editor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['venue_id', 'editor_id'])

        # Adding field 'Event.created'
        db.add_column(u'events_event', 'created',
                      self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Event.modified'
        db.add_column(u'events_event', 'modified',
                      self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Event.submitted_by'
        db.add_column(u'events_event', 'submitted_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='event_submissions', null=True, to=orm['accounts.Editor']),
                      keep_default=False)

        # Adding M2M table for field edited_by on 'Event'
        m2m_table_name = db.shorten_name(u'events_event_edited_by')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'events.event'], null=False)),
            ('editor', models.ForeignKey(orm[u'accounts.editor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'editor_id'])

        # Adding field 'Performance.created'
        db.add_column(u'events_performance', 'created',
                      self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Performance.modified'
        db.add_column(u'events_performance', 'modified',
                      self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Performance.submitted_by'
        db.add_column(u'events_performance', 'submitted_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='performance_submissions', null=True, to=orm['accounts.Editor']),
                      keep_default=False)

        # Adding M2M table for field edited_by on 'Performance'
        m2m_table_name = db.shorten_name(u'events_performance_edited_by')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('performance', models.ForeignKey(orm[u'events.performance'], null=False)),
            ('editor', models.ForeignKey(orm[u'accounts.editor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['performance_id', 'editor_id'])


    def backwards(self, orm):
        # Deleting field 'Venue.created'
        db.delete_column(u'events_venue', 'created')

        # Deleting field 'Venue.modified'
        db.delete_column(u'events_venue', 'modified')

        # Deleting field 'Venue.submitted_by'
        db.delete_column(u'events_venue', 'submitted_by_id')

        # Removing M2M table for field edited_by on 'Venue'
        db.delete_table(db.shorten_name(u'events_venue_edited_by'))

        # Deleting field 'Event.created'
        db.delete_column(u'events_event', 'created')

        # Deleting field 'Event.modified'
        db.delete_column(u'events_event', 'modified')

        # Deleting field 'Event.submitted_by'
        db.delete_column(u'events_event', 'submitted_by_id')

        # Removing M2M table for field edited_by on 'Event'
        db.delete_table(db.shorten_name(u'events_event_edited_by'))

        # Deleting field 'Performance.created'
        db.delete_column(u'events_performance', 'created')

        # Deleting field 'Performance.modified'
        db.delete_column(u'events_performance', 'modified')

        # Deleting field 'Performance.submitted_by'
        db.delete_column(u'events_performance', 'submitted_by_id')

        # Removing M2M table for field edited_by on 'Performance'
        db.delete_table(db.shorten_name(u'events_performance_edited_by'))


    models = {
        u'accounts.editor': {
            'Meta': {'object_name': 'Editor'},
            'access_token': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'active_since': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 1, 0, 0)', 'blank': 'True'}),
            'base_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'email': ('ohashi.db.models.fields.EmailField', [], {'unique': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'refresh_token': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'started': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'token_expiration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'username': ('ohashi.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True'})
        },
        u'events.event': {
            'Meta': {'object_name': 'Event'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'edited_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'events_edits'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['accounts.Editor']"}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'secondary_info_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'submitted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'event_submissions'", 'null': 'True', 'to': u"orm['accounts.Editor']"})
        },
        u'events.performance': {
            'Meta': {'ordering': "('day', 'start_time')", 'object_name': 'Performance'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'day': ('django.db.models.fields.DateField', [], {}),
            'edited_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'performances_edits'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['accounts.Editor']"}),
            'end_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'schedule'", 'to': u"orm['events.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'submitted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'performance_submissions'", 'null': 'True', 'to': u"orm['accounts.Editor']"}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'performances'", 'null': 'True', 'to': u"orm['events.Venue']"})
        },
        u'events.venue': {
            'Meta': {'object_name': 'Venue'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'edited_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'venues_edits'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['accounts.Editor']"}),
            'former_names': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'romanized_address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'submitted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'venue_submissions'", 'null': 'True', 'to': u"orm['accounts.Editor']"})
        }
    }

    complete_apps = ['events']