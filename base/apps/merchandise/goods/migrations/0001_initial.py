# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Shop'
        db.create_table(u'goods_shop', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('romanized_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('website_link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal(u'goods', ['Shop'])

        # Adding model 'Base'
        db.create_table(u'goods_base', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('submitted_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='base_submissions', null=True, to=orm['accounts.Editor'])),
            ('romanized_name', self.gf('ohashi.db.models.fields.CharField')()),
            ('name', self.gf('ohashi.db.models.fields.CharField')()),
            ('released', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(1, 1, 1, 0, 0), null=True, db_index=True, blank=True)),
            ('price', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('uuid', self.gf('ohashi.db.models.fields.uuids.UUIDField')()),
            ('is_graduation_good', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_birthday_good', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_online_exclusive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_mailorder_exclusive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'], null=True, blank=True)),
            ('shop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['goods.Shop'], null=True, blank=True)),
            ('online_id', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('other_info', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('available_from', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('available_until', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'goods', ['Base'])

        # Adding M2M table for field edited_by on 'Base'
        m2m_table_name = db.shorten_name(u'goods_base_edited_by')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('base', models.ForeignKey(orm[u'goods.base'], null=False)),
            ('editor', models.ForeignKey(orm[u'accounts.editor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['base_id', 'editor_id'])

        # Adding M2M table for field idols on 'Base'
        m2m_table_name = db.shorten_name(u'goods_base_idols')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('base', models.ForeignKey(orm[u'goods.base'], null=False)),
            ('idol', models.ForeignKey(orm[u'people.idol'], null=False))
        ))
        db.create_unique(m2m_table_name, ['base_id', 'idol_id'])

        # Adding M2M table for field groups on 'Base'
        m2m_table_name = db.shorten_name(u'goods_base_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('base', models.ForeignKey(orm[u'goods.base'], null=False)),
            ('group', models.ForeignKey(orm[u'people.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['base_id', 'group_id'])

        # Adding M2M table for field participating_idols on 'Base'
        m2m_table_name = db.shorten_name(u'goods_base_participating_idols')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('base', models.ForeignKey(orm[u'goods.base'], null=False)),
            ('idol', models.ForeignKey(orm[u'people.idol'], null=False))
        ))
        db.create_unique(m2m_table_name, ['base_id', 'idol_id'])

        # Adding M2M table for field participating_groups on 'Base'
        m2m_table_name = db.shorten_name(u'goods_base_participating_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('base', models.ForeignKey(orm[u'goods.base'], null=False)),
            ('group', models.ForeignKey(orm[u'people.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['base_id', 'group_id'])

        # Adding model 'Good'
        db.create_table(u'goods_good', (
            (u'base_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['goods.Base'], unique=True, primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['goods.Set'], null=True, blank=True)),
            ('is_bonus_good', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_campaign_good', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_lottery_good', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_set_exclusive', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'goods', ['Good'])

        # Adding model 'Set'
        db.create_table(u'goods_set', (
            (u'base_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['goods.Base'], unique=True, primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=18)),
        ))
        db.send_create_signal(u'goods', ['Set'])

        # Adding model 'SuperSet'
        db.create_table(u'goods_superset', (
            (u'base_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['goods.Base'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'goods', ['SuperSet'])

        # Adding M2M table for field goods on 'SuperSet'
        m2m_table_name = db.shorten_name(u'goods_superset_goods')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('superset', models.ForeignKey(orm[u'goods.superset'], null=False)),
            ('good', models.ForeignKey(orm[u'goods.good'], null=False))
        ))
        db.create_unique(m2m_table_name, ['superset_id', 'good_id'])

        # Adding M2M table for field sets on 'SuperSet'
        m2m_table_name = db.shorten_name(u'goods_superset_sets')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('superset', models.ForeignKey(orm[u'goods.superset'], null=False)),
            ('set', models.ForeignKey(orm[u'goods.set'], null=False))
        ))
        db.create_unique(m2m_table_name, ['superset_id', 'set_id'])


    def backwards(self, orm):
        # Deleting model 'Shop'
        db.delete_table(u'goods_shop')

        # Deleting model 'Base'
        db.delete_table(u'goods_base')

        # Removing M2M table for field edited_by on 'Base'
        db.delete_table(db.shorten_name(u'goods_base_edited_by'))

        # Removing M2M table for field idols on 'Base'
        db.delete_table(db.shorten_name(u'goods_base_idols'))

        # Removing M2M table for field groups on 'Base'
        db.delete_table(db.shorten_name(u'goods_base_groups'))

        # Removing M2M table for field participating_idols on 'Base'
        db.delete_table(db.shorten_name(u'goods_base_participating_idols'))

        # Removing M2M table for field participating_groups on 'Base'
        db.delete_table(db.shorten_name(u'goods_base_participating_groups'))

        # Deleting model 'Good'
        db.delete_table(u'goods_good')

        # Deleting model 'Set'
        db.delete_table(u'goods_set')

        # Deleting model 'SuperSet'
        db.delete_table(u'goods_superset')

        # Removing M2M table for field goods on 'SuperSet'
        db.delete_table(db.shorten_name(u'goods_superset_goods'))

        # Removing M2M table for field sets on 'SuperSet'
        db.delete_table(db.shorten_name(u'goods_superset_sets'))


    models = {
        u'accounts.editor': {
            'Meta': {'object_name': 'Editor'},
            'access_token': ('ohashi.db.models.fields.CharField', [], {'blank': 'True'}),
            'active_since': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 10, 3, 0, 0)', 'blank': 'True'}),
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'events'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'events'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'info_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'participating_groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'events_attributed_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            'participating_idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'events_attributed_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'poster': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'secondary_info_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'stage': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'submitted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'event_submissions'", 'null': 'True', 'to': u"orm['accounts.Editor']"})
        },
        u'goods.base': {
            'Meta': {'object_name': 'Base'},
            'available_from': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'available_until': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'edited_by': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'bases_edits'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['accounts.Editor']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']", 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'bases'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'bases'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'is_birthday_good': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_graduation_good': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_mailorder_exclusive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_online_exclusive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('ohashi.db.models.fields.CharField', [], {}),
            'online_id': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'other_info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'participating_groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'bases_attributed_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Group']"}),
            'participating_idols': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'bases_attributed_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['people.Idol']"}),
            'price': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'released': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(1, 1, 1, 0, 0)', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'romanized_name': ('ohashi.db.models.fields.CharField', [], {}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['goods.Shop']", 'null': 'True', 'blank': 'True'}),
            'submitted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'base_submissions'", 'null': 'True', 'to': u"orm['accounts.Editor']"}),
            'uuid': ('ohashi.db.models.fields.uuids.UUIDField', [], {})
        },
        u'goods.good': {
            'Meta': {'object_name': 'Good', '_ormbases': [u'goods.Base']},
            u'base_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['goods.Base']", 'unique': 'True', 'primary_key': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'is_bonus_good': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_campaign_good': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_lottery_good': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_set_exclusive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['goods.Set']", 'null': 'True', 'blank': 'True'})
        },
        u'goods.set': {
            'Meta': {'object_name': 'Set', '_ormbases': [u'goods.Base']},
            u'base_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['goods.Base']", 'unique': 'True', 'primary_key': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '18'})
        },
        u'goods.shop': {
            'Meta': {'object_name': 'Shop'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'romanized_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'website_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'goods.superset': {
            'Meta': {'object_name': 'SuperSet', '_ormbases': [u'goods.Base']},
            u'base_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['goods.Base']", 'unique': 'True', 'primary_key': 'True'}),
            'goods': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['goods.Good']", 'symmetrical': 'False'}),
            'sets': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['goods.Set']", 'symmetrical': 'False'})
        },
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
            'primary_membership': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'primary'", 'null': 'True', 'to': u"orm['people.Membership']"}),
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
        }
    }

    complete_apps = ['goods']