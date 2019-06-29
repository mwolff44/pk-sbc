# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-27 17:53
from __future__ import unicode_literals

from django.db import migrations
import migrate_sql.operations


class Migration(migrations.Migration):

    dependencies = [
        ('switch', '0024_auto_20170109_1944'),
    ]

    operations = [
        migrate_sql.operations.ReverseAlterSQL(
            name=b'dispatcher_view',
            sql=b'DROP VIEW IF EXISTS dispatcher CASCADE; ',
            reverse_sql=b"DROP VIEW IF EXISTS dispatcher CASCADE; CREATE OR REPLACE VIEW dispatcher AS  SELECT row_number() OVER () AS id,  CAST(fsp.direction AS VARCHAR) AS setid,  CONCAT('sip:', fsp.ip, ':', sp.sip_port) AS destination,  0 AS flags,  fsp.priority,  '' AS attrs,  fsp.description FROM fs_switch_profile fsp LEFT JOIN fs_switch f  ON fsp.fsswitch_id = f.id AND fsp.direction = 1 AND f.setid=10 AND f.enabled=TRUE LEFT JOIN sip_profile sp  ON sp.enabled = TRUE AND sp.id = fsp.sipprofile_id; ",
        ),
        migrate_sql.operations.AlterSQL(
            name=b'dispatcher_view',
            sql=b"DROP VIEW IF EXISTS dispatcher CASCADE; CREATE OR REPLACE VIEW dispatcher AS  SELECT row_number() OVER () AS id,  CAST(fsp.direction AS INTEGER) AS setid,  CAST((CONCAT('sip:', fsp.ip, ':', sp.sip_port)) AS VARCHAR) AS destination,  0 AS flags,  fsp.priority,  CAST('' AS VARCHAR) AS attrs,  fsp.description FROM fs_switch_profile fsp LEFT JOIN fs_switch f  ON fsp.fsswitch_id = f.id AND fsp.direction = 1 AND f.setid=10 AND f.enabled=TRUE LEFT JOIN sip_profile sp  ON sp.enabled = TRUE AND sp.id = fsp.sipprofile_id; ",
            reverse_sql=b'DROP VIEW IF EXISTS dispatcher CASCADE; ',
        ),
    ]