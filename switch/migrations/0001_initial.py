# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'VoipSwitch'
        db.create_table('fs_switch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('ip', self.gf('django.db.models.fields.CharField')(default='auto', max_length=100)),
            ('esl_listen_ip', self.gf('django.db.models.fields.CharField')(default='127.0.0.1', max_length=100)),
            ('esl_listen_port', self.gf('django.db.models.fields.PositiveIntegerField')(default='8021')),
            ('esl_password', self.gf('django.db.models.fields.CharField')(default='ClueCon', max_length=30)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('switch', ['VoipSwitch'])


    def backwards(self, orm):
        # Deleting model 'VoipSwitch'
        db.delete_table('fs_switch')


    models = {
        'switch.voipswitch': {
            'Meta': {'ordering': "('name',)", 'object_name': 'VoipSwitch', 'db_table': "'voip_switch'"},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'esl_listen_ip': ('django.db.models.fields.CharField', [], {'default': "'127.0.0.1'", 'max_length': '100'}),
            'esl_listen_port': ('django.db.models.fields.PositiveIntegerField', [], {'default': "'8021'"}),
            'esl_password': ('django.db.models.fields.CharField', [], {'default': "'ClueCon'", 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'default': "'auto'", 'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['switch']