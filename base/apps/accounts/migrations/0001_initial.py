# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Editor'
        db.create_table(u'accounts_editor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('base_id', self.gf('django.db.models.fields.IntegerField')(unique=True, db_index=True)),
            ('username', self.gf('ohashi.db.models.fields.CharField')(db_index=True, blank=True)),
            ('name', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('email', self.gf('ohashi.db.models.fields.EmailField')(unique=True, db_index=True)),
            ('started', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('active_since', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 9, 19, 0, 0), blank=True)),
            ('access_token', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('refresh_token', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('token_expiration', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'accounts', ['Editor'])


    def backwards(self, orm):
        # Deleting model 'Editor'
        db.delete_table(u'accounts_editor')


    models = {
        u'accounts.editor': {
            'Meta': {'object_name': 'Editor'},
            'access_token': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'active_since': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 9, 19, 0, 0)', 'blank': 'True'}),
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
            'token_expiration': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'username': ('ohashi.db.models.fields.CharField', [], {'db_index': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['accounts']