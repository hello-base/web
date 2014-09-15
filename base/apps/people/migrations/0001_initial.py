# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Idol'
        db.create_table(u'people_idol', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('birthdate_dayofyear', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=None, null=True)),
            ('name', self.gf('ohashi.db.models.fields.CharField')()),
            ('romanized_name', self.gf('ohashi.db.models.fields.CharField')()),
            ('family_name', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('given_name', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('romanized_family_name', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('romanized_given_name', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('alias', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('romanized_alias', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('nicknames', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('slug', self.gf('ohashi.db.models.fields.SlugField')(db_index=True)),
            ('status', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1, db_index=True)),
            ('scope', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1, db_index=True)),
            ('bloodtype', self.gf('ohashi.db.models.fields.CharField')(default='A', max_length=2, blank=True)),
            ('height', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=1, blank=True)),
            ('birthdate', self.gf('ohashi.db.models.fields.birthdays.BirthdayField')(db_index=True, null=True, blank=True)),
            ('birthplace', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('birthplace_romanized', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('birthplace_latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('birthplace_longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('has_discussions', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('note_processed', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'people', ['Idol'])

        # Adding model 'Staff'
        db.create_table(u'people_staff', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('ohashi.db.models.fields.CharField')()),
            ('romanized_name', self.gf('ohashi.db.models.fields.CharField')()),
            ('family_name', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('given_name', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('romanized_family_name', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('romanized_given_name', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('alias', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('romanized_alias', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('nicknames', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('slug', self.gf('ohashi.db.models.fields.SlugField')(db_index=True)),
        ))
        db.send_create_signal(u'people', ['Staff'])

        # Adding model 'Group'
        db.create_table(u'people_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('ohashi.db.models.fields.CharField')()),
            ('romanized_name', self.gf('ohashi.db.models.fields.CharField')()),
            ('slug', self.gf('ohashi.db.models.fields.SlugField')(db_index=True)),
            ('classification', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1, db_index=True)),
            ('status', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1, db_index=True)),
            ('scope', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1, db_index=True)),
            ('started', self.gf('django.db.models.fields.DateField')(db_index=True)),
            ('ended', self.gf('django.db.models.fields.DateField')(db_index=True, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='subgroups', null=True, to=orm['people.Group'])),
            ('has_discussions', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('former_names', self.gf('ohashi.db.models.fields.CharField')(blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('note_processed', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'people', ['Group'])

        # Adding M2M table for field groups on 'Group'
        m2m_table_name = db.shorten_name(u'people_group_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_group', models.ForeignKey(orm[u'people.group'], null=False)),
            ('to_group', models.ForeignKey(orm[u'people.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_group_id', 'to_group_id'])

        # Adding model 'Membership'
        db.create_table(u'people_membership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('idol', self.gf('django.db.models.fields.related.ForeignKey')(related_name='memberships', to=orm['people.Idol'])),
            ('group', self.gf('ohashi.db.models.fields.CustomManagerForeignKey')(blank=True, related_name='memberships', null=True, to=orm['people.Group'])),
            ('is_primary', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('started', self.gf('django.db.models.fields.DateField')(db_index=True)),
            ('ended', self.gf('django.db.models.fields.DateField')(db_index=True, null=True, blank=True)),
            ('is_leader', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('leadership_started', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('leadership_ended', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'people', ['Membership'])

        # Adding unique constraint on 'Membership', fields ['idol', 'group']
        db.create_unique(u'people_membership', ['idol_id', 'group_id'])

        # Adding model 'Trivia'
        db.create_table(u'people_trivia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('idol', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Idol'], null=True, blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Group'], null=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'people', ['Trivia'])


    def backwards(self, orm):
        # Removing unique constraint on 'Membership', fields ['idol', 'group']
        db.delete_unique(u'people_membership', ['idol_id', 'group_id'])

        # Deleting model 'Idol'
        db.delete_table(u'people_idol')

        # Deleting model 'Staff'
        db.delete_table(u'people_staff')

        # Deleting model 'Group'
        db.delete_table(u'people_group')

        # Removing M2M table for field groups on 'Group'
        db.delete_table(db.shorten_name(u'people_group_groups'))

        # Deleting model 'Membership'
        db.delete_table(u'people_membership')

        # Deleting model 'Trivia'
        db.delete_table(u'people_trivia')


    models = {
        u'people.group': {
            'Meta': {'object_name': 'Group'},
            'classification': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'ended': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'former_names': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'member_groups'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            'has_discussions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'groups'", 'symmetrical': 'False', 'through': u"orm['people.Membership']", 'to': u"orm['people.Idol']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('ohashi.db.models.fields.CharField', [], {}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'note_processed': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subgroups'", 'null': 'True', 'to': u"orm['people.Group']"}),
            'romanized_name': ('ohashi.db.models.fields.CharField', [], {}),
            'scope': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'slug': ('ohashi.db.models.fields.SlugField', [], {'db_index': 'True'}),
            'started': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'})
        },
        u'people.idol': {
            'Meta': {'object_name': 'Idol'},
            'alias': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'birthdate': ('ohashi.db.models.fields.birthdays.BirthdayField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'birthdate_dayofyear': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': 'None', 'null': 'True'}),
            'birthplace': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'birthplace_latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'birthplace_longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'birthplace_romanized': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'bloodtype': ('ohashi.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '2', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'family_name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'given_name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'has_discussions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '1', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('ohashi.db.models.fields.CharField', [], {}),
            'nicknames': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'note_processed': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'romanized_alias': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'romanized_family_name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'romanized_given_name': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'romanized_name': ('ohashi.db.models.fields.CharField', [], {}),
            'scope': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'slug': ('ohashi.db.models.fields.SlugField', [], {'db_index': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'})
        },
        u'people.membership': {
            'Meta': {'ordering': "('-is_primary', '-started', '-idol__birthdate')", 'unique_together': "(('idol', 'group'),)", 'object_name': 'Membership'},
            'ended': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
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
            'slug': ('ohashi.db.models.fields.SlugField', [], {'db_index': 'True'})
        },
        u'people.trivia': {
            'Meta': {'object_name': 'Trivia'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Group']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idol': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Idol']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['people']