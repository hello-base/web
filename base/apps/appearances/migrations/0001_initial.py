# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Show'
        db.create_table(u'appearances_show', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('romanized_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('aired_from', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('aired_until', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'appearances', ['Show'])

        # Adding model 'TimeSlot'
        db.create_table(u'appearances_timeslot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('show', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['appearances.Show'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'appearances', ['TimeSlot'])

        # Adding model 'Episode'
        db.create_table(u'appearances_episode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('show', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['appearances.Show'])),
            ('air_date', self.gf('django.db.models.fields.DateField')()),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='continuation', null=True, to=orm['appearances.Episode'])),
            ('record_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('romanized_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('video_link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'appearances', ['Episode'])

        # Adding model 'Synopsis'
        db.create_table(u'appearances_synopsis', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['appearances.Episode'])),
            ('body', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'appearances', ['Synopsis'])

        # Adding model 'Magazine'
        db.create_table(u'appearances_magazine', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('romanized_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('price', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal(u'appearances', ['Magazine'])

        # Adding model 'Issue'
        db.create_table(u'appearances_issue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('magazine', self.gf('django.db.models.fields.related.ForeignKey')(related_name='issues', to=orm['appearances.Magazine'])),
            ('volume_number', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('release_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('catalog_number', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('isbn_number', self.gf('django.db.models.fields.CharField')(max_length=19)),
            ('cover', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'appearances', ['Issue'])

        # Adding model 'IssueImage'
        db.create_table(u'appearances_issueimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gallery', to=orm['appearances.Issue'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'appearances', ['IssueImage'])

        # Adding model 'CardSet'
        db.create_table(u'appearances_cardset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sets', to=orm['appearances.Issue'])),
            ('romanized_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'appearances', ['CardSet'])

        # Adding model 'Card'
        db.create_table(u'appearances_card', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cards', to=orm['appearances.Issue'])),
            ('cardset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['appearances.CardSet'], null=True, blank=True)),
            ('hp_model', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='cards', null=True, to=orm['people.Idol'])),
            ('member_of', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='idol', null=True, to=orm['people.Group'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='cards', null=True, to=orm['people.Group'])),
            ('number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('other_model_romanized_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('other_model_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('other_member_of_romanized_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('other_member_of_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('other_group_romanized_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('other_group_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'appearances', ['Card'])


    def backwards(self, orm):
        # Deleting model 'Show'
        db.delete_table(u'appearances_show')

        # Deleting model 'TimeSlot'
        db.delete_table(u'appearances_timeslot')

        # Deleting model 'Episode'
        db.delete_table(u'appearances_episode')

        # Deleting model 'Synopsis'
        db.delete_table(u'appearances_synopsis')

        # Deleting model 'Magazine'
        db.delete_table(u'appearances_magazine')

        # Deleting model 'Issue'
        db.delete_table(u'appearances_issue')

        # Deleting model 'IssueImage'
        db.delete_table(u'appearances_issueimage')

        # Deleting model 'CardSet'
        db.delete_table(u'appearances_cardset')

        # Deleting model 'Card'
        db.delete_table(u'appearances_card')


    models = {
        u'accounts.editor': {
            'Meta': {'object_name': 'Editor'},
            'access_token': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'active_since': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 6, 0, 0)', 'blank': 'True'}),
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
        u'appearances.card': {
            'Meta': {'object_name': 'Card'},
            'cardset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['appearances.CardSet']", 'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cards'", 'null': 'True', 'to': u"orm['people.Group']"}),
            'hp_model': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cards'", 'null': 'True', 'to': u"orm['people.Idol']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cards'", 'to': u"orm['appearances.Issue']"}),
            'member_of': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'idol'", 'null': 'True', 'to': u"orm['people.Group']"}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'other_group_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'other_group_romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'other_member_of_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'other_member_of_romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'other_model_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'other_model_romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'appearances.cardset': {
            'Meta': {'object_name': 'CardSet'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sets'", 'to': u"orm['appearances.Issue']"}),
            'romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'appearances.episode': {
            'Meta': {'object_name': 'Episode'},
            'air_date': ('django.db.models.fields.DateField', [], {}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'continuation'", 'null': 'True', 'to': u"orm['appearances.Episode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'record_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'show': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['appearances.Show']"}),
            'video_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'appearances.issue': {
            'Meta': {'object_name': 'Issue'},
            'catalog_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn_number': ('django.db.models.fields.CharField', [], {'max_length': '19'}),
            'magazine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issues'", 'to': u"orm['appearances.Magazine']"}),
            'release_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'volume_number': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        u'appearances.issueimage': {
            'Meta': {'object_name': 'IssueImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gallery'", 'to': u"orm['appearances.Issue']"})
        },
        u'appearances.magazine': {
            'Meta': {'object_name': 'Magazine'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'price': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'appearances.show': {
            'Meta': {'object_name': 'Show'},
            'aired_from': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'aired_until': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'appearances.synopsis': {
            'Meta': {'object_name': 'Synopsis'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['appearances.Episode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'appearances.timeslot': {
            'Meta': {'object_name': 'TimeSlot'},
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'show': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['appearances.Show']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'people.group': {
            'Meta': {'ordering': "('started',)", 'object_name': 'Group'},
            'classification': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'edited_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'groups_edits'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['accounts.Editor']"}),
            'ended': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'former_names': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'supergroups'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'groups'", 'symmetrical': 'False', 'through': u"orm['people.Membership']", 'to': u"orm['people.Idol']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subgroups'", 'null': 'True', 'to': u"orm['people.Group']"}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'photo_thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'scope': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'started': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'submitted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'group_submissions'", 'null': 'True', 'to': u"orm['accounts.Editor']"})
        },
        u'people.idol': {
            'Meta': {'ordering': "('birthdate',)", 'object_name': 'Idol'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'birthdate': ('ohashi.db.models.fields.birthdays.BirthdayField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'birthdate_dayofyear': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': 'None', 'null': 'True'}),
            'birthplace': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'birthplace_latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'birthplace_longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'birthplace_romanized': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'bloodtype': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '2', 'blank': 'True'}),
            'color': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '7', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'edited_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'idols_edits'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['accounts.Editor']"}),
            'family_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'given_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'graduated': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '1', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'nicknames': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'photo_thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'primary_membership': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'primary'", 'null': 'True', 'to': u"orm['people.Membership']"}),
            'retired': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'romanized_alias': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'romanized_family_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'romanized_given_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'scope': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
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
        }
    }

    complete_apps = ['appearances']