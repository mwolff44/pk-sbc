# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerRatesDid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('rate', models.DecimalField(verbose_name='Rate', max_digits=11, decimal_places=5)),
                ('block_min_duration', models.IntegerField(default=1, verbose_name='block min duration')),
                ('interval_duration', models.IntegerField(default=1, verbose_name='Interval duration')),
                ('enabled', models.BooleanField(default=True, verbose_name='Enabled / Disabled')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date added')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
            ],
            options={
                'ordering': ('name',),
                'db_table': 'customer_rates_did',
                'verbose_name': 'DID customer rate',
                'verbose_name_plural': 'DID customer rates',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Did',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(unique=True, max_length=30, verbose_name='DID number', db_index=True)),
                ('prov_max_channels', models.PositiveIntegerField(default=1, help_text='maximum\n                    simultaneous calls allowed for this did.', verbose_name='provider channels')),
                ('cust_max_channels', models.PositiveIntegerField(default=1, help_text='maximum\n                    simultaneous calls allowed for this did.', null=True, verbose_name='customer channels', blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date added')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
            ],
            options={
                'ordering': ('number',),
                'db_table': 'did',
                'verbose_name': 'DID',
                'verbose_name_plural': 'DIDs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProviderRatesDid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('rate', models.DecimalField(verbose_name='Rate', max_digits=11, decimal_places=5)),
                ('block_min_duration', models.IntegerField(default=1, verbose_name='block min duration')),
                ('interval_duration', models.IntegerField(default=1, verbose_name='Interval duration')),
                ('enabled', models.BooleanField(default=True, verbose_name='Enabled / Disabled')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date added')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
            ],
            options={
                'ordering': ('provider', 'name'),
                'db_table': 'provider_rates_did',
                'verbose_name': 'DID provider rate',
                'verbose_name_plural': 'DID provider rates',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RoutesDid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=1)),
                ('type', models.CharField(default=b'm', help_text='Routing type : trunk or\n                                external number.', max_length=2, verbose_name='Route type', choices=[(b's', 'SIP Trunk'), (b'e', 'External number')])),
                ('number', models.CharField(default=b'', max_length=30, null=True, verbose_name='destination number', blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date added')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('contract_did', models.ForeignKey(to='did.Did')),
            ],
            options={
                'ordering': ('contract_did',),
                'db_table': 'did_routes',
                'verbose_name': 'DID route',
                'verbose_name_plural': 'DID routes',
            },
            bases=(models.Model,),
        ),
    ]
