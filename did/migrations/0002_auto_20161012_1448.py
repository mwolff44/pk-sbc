# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pyfreebill', '0001_initial'),
        ('did', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='routesdid',
            name='trunk',
            field=models.ForeignKey(blank=True, to='pyfreebill.CustomerDirectory', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='routesdid',
            unique_together=set([('contract_did', 'order')]),
        ),
        migrations.AddField(
            model_name='providerratesdid',
            name='provider',
            field=models.ForeignKey(verbose_name='provider', to='pyfreebill.Company'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='providerratesdid',
            unique_together=set([('name', 'provider')]),
        ),
        migrations.AddField(
            model_name='did',
            name='cust_plan',
            field=models.ForeignKey(verbose_name='customer rate plan', blank=True, to='did.CustomerRatesDid', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='did',
            name='customer',
            field=models.ForeignKey(related_name='didcustomer', verbose_name='Customer', blank=True, to='pyfreebill.Company', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='did',
            name='prov_plan',
            field=models.ForeignKey(verbose_name='provider rate plan', to='did.ProviderRatesDid'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='did',
            name='provider',
            field=models.ForeignKey(related_name='didprovider', verbose_name='Provider', to='pyfreebill.Company'),
            preserve_default=True,
        ),
    ]
