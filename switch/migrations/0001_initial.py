# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VoipSwitch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Switch name', max_length=50, verbose_name='Switch name')),
                ('ip', models.CharField(default=b'auto', help_text='Switch IP.', max_length=100, verbose_name='switch IP')),
                ('esl_listen_ip', models.CharField(default=b'127.0.0.1', help_text='Event socket switch IP.', max_length=100, verbose_name='event socket switch IP')),
                ('esl_listen_port', models.PositiveIntegerField(default=b'8021', help_text='Event socket switch port.', verbose_name='event socket switch port')),
                ('esl_password', models.CharField(default=b'ClueCon', help_text='Event socket switch password.', max_length=30, verbose_name='event socket switch password')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date added')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
            ],
            options={
                'ordering': ('name',),
                'db_table': 'fs_switch',
                'verbose_name': 'VoIP Switch',
                'verbose_name_plural': 'VoIP Switches',
            },
            bases=(models.Model,),
        ),
    ]
