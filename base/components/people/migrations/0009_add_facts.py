# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Trivia'
        db.delete_table(u'people_trivia')

        # Adding model 'Fact'
        db.create_table(u'people_fact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('idol', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='facts', null=True, to=orm['people.Idol'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='facts', null=True, to=orm['people.Group'])),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'people', ['Fact'])


    def backwards(self, orm):
        # Adding model 'Trivia'
        db.create_table(u'people_trivia', (
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Group'], null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('idol', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Idol'], null=True, blank=True)),
        ))
        db.send_create_signal(u'people', ['Trivia'])

        # Deleting model 'Fact'
        db.delete_table(u'people_fact')


    models = {
        u'accounts.editor': {
            'Meta': {'object_name': 'Editor'},
            'access_token': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'active_since': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 27, 0, 0)', 'blank': 'True'}),
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
        u'people.fact': {
            'Meta': {'object_name': 'Fact'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'facts'", 'null': 'True', 'to': u"orm['people.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idol': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'facts'", 'null': 'True', 'to': u"orm['people.Idol']"})
        },
        u'people.group': {
            'Meta': {'object_name': 'Group'},
            'classification': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'edited_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'groups_edits'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['accounts.Editor']"}),
            'ended': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'former_names': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'member_groups'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'groups'", 'symmetrical': 'False', 'through': u"orm['people.Membership']", 'to': u"orm['people.Idol']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('ohashi.db.models.fields.CharField', [], {}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'note_processed': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subgroups'", 'null': 'True', 'to': u"orm['people.Group']"}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'photo_thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'romanized_name': ('ohashi.db.models.fields.CharField', [], {}),
            'scope': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'slug': ('ohashi.db.models.fields.SlugField', [], {'db_index': 'True'}),
            'started': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'submitted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'group_submissions'", 'null': 'True', 'to': u"orm['accounts.Editor']"})
        },
        u'people.groupshot': {
            'Meta': {'ordering': "('-taken',)", 'object_name': 'Groupshot'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'to': u"orm['people.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'photo_thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'taken': ('django.db.models.fields.DateField', [], {})
        },
        u'people.headshot': {
            'Meta': {'ordering': "('-taken',)", 'object_name': 'Headshot'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idol': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'to': u"orm['people.Idol']"}),
            'kind': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'photo_thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'taken': ('django.db.models.fields.DateField', [], {})
        },
        u'people.idol': {
            'Meta': {'ordering': "('birthdate',)", 'object_name': 'Idol'},
            'alias': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'birthdate': ('ohashi.db.models.fields.birthdays.BirthdayField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'birthdate_dayofyear': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': 'None', 'null': 'True'}),
            'birthplace': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'birthplace_latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'birthplace_longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'birthplace_romanized': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'bloodtype': ('ohashi.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '2', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'edited_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'idols_edits'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['accounts.Editor']"}),
            'family_name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'given_name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'graduated': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '1', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('ohashi.db.models.fields.CharField', [], {}),
            'nicknames': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'note_processed': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'photo_thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'primary_membership': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'primary'", 'null': 'True', 'to': u"orm['people.Membership']"}),
            'retired': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'romanized_alias': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'romanized_family_name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'romanized_given_name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'romanized_name': ('ohashi.db.models.fields.CharField', [], {}),
            'scope': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'slug': ('ohashi.db.models.fields.SlugField', [], {'db_index': 'True'}),
            'started': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_index': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'submitted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'idol_submissions'", 'null': 'True', 'to': u"orm['accounts.Editor']"})
        },
        u'people.membership': {
            'Meta': {'ordering': "('-is_primary', '-started', '-idol__birthdate')", 'unique_together': "(('idol', 'group'),)", 'object_name': 'Membership'},
            'ended': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'generation': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'group': ('ohashi.db.models.fields.CustomManagerForeignKey', [], {'blank': 'True', 'related_name': "'memberships'", 'null': 'True', 'to': u"orm['people.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idol': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'memberships'", 'to': u"orm['people.Idol']"}),
            'is_leader': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'leadership_ended': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'leadership_started': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'started': ('django.db.models.fields.DateField', [], {'db_index': 'True'})
        },
        u'people.staff': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Staff'},
            'alias': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'edited_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'staffs_edits'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['accounts.Editor']"}),
            'family_name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'given_name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('ohashi.db.models.fields.CharField', [], {}),
            'nicknames': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'romanized_alias': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'romanized_family_name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'romanized_given_name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'romanized_name': ('ohashi.db.models.fields.CharField', [], {}),
            'slug': ('ohashi.db.models.fields.SlugField', [], {'db_index': 'True'}),
            'submitted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'staff_submissions'", 'null': 'True', 'to': u"orm['accounts.Editor']"})
        }
    }

    complete_apps = ['people']