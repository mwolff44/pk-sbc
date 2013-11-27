# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Initial data upload."
        from django.core.management import call_command
        call_command("loaddata", "0001_fixtures.json")

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'switch.voipswitch': {
            'Meta': {'ordering': "('name',)", 'object_name': 'VoipSwitch', 'db_table': "'fs_switch'"},
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
    symmetrical = True
