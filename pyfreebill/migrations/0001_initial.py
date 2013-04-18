# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Company'
        db.create_table('company', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('about', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('vat', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('vat_number', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('prepaid', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('credit_limit', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=4)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=4)),
            ('max_calls', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('billing_cycle', self.gf('django.db.models.fields.CharField')(default='m', max_length=10)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pyfreebill', ['Company'])

        # Adding model 'Person'
        db.create_table('contacts_people', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('suffix', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pyfreebill.Company'], null=True, blank=True)),
            ('about', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pyfreebill', ['Person'])

        # Adding model 'Group'
        db.create_table('contacts_groups', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('about', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pyfreebill', ['Group'])

        # Adding M2M table for field people on 'Group'
        db.create_table('contacts_groups_people', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm[u'pyfreebill.group'], null=False)),
            ('person', models.ForeignKey(orm[u'pyfreebill.person'], null=False))
        ))
        db.create_unique('contacts_groups_people', ['group_id', 'person_id'])

        # Adding M2M table for field companies on 'Group'
        db.create_table('contacts_groups_companies', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm[u'pyfreebill.group'], null=False)),
            ('company', models.ForeignKey(orm[u'pyfreebill.company'], null=False))
        ))
        db.create_unique('contacts_groups_companies', ['group_id', 'company_id'])

        # Adding model 'PhoneNumber'
        db.create_table('contacts_phone_numbers', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('location', self.gf('django.db.models.fields.CharField')(default='work', max_length=6)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pyfreebill', ['PhoneNumber'])

        # Adding model 'EmailAddress'
        db.create_table('contacts_email_addresses', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('email_address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('location', self.gf('django.db.models.fields.CharField')(default='work', max_length=6)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pyfreebill', ['EmailAddress'])

        # Adding model 'InstantMessenger'
        db.create_table('contacts_instant_messengers', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('im_account', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('location', self.gf('django.db.models.fields.CharField')(default='work', max_length=6)),
            ('service', self.gf('django.db.models.fields.CharField')(default='jabber', max_length=11)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pyfreebill', ['InstantMessenger'])

        # Adding model 'WebSite'
        db.create_table('contacts_web_sites', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('location', self.gf('django.db.models.fields.CharField')(default='work', max_length=6)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pyfreebill', ['WebSite'])

        # Adding model 'StreetAddress'
        db.create_table('contacts_street_addresses', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('street', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('location', self.gf('django.db.models.fields.CharField')(default='work', max_length=6)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pyfreebill', ['StreetAddress'])

        # Adding model 'SpecialDate'
        db.create_table('contacts_special_dates', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('occasion', self.gf('django.db.models.fields.TextField')(max_length=200)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('every_year', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pyfreebill', ['SpecialDate'])

        # Adding model 'CompanyBalanceHistory'
        db.create_table('company_balance_history', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pyfreebill.Company'])),
            ('amount_debited', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=4)),
            ('amount_refund', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=4)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=4)),
            ('reference', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pyfreebill', ['CompanyBalanceHistory'])

        # Adding model 'CustomerDirectory'
        db.create_table('customer_directory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pyfreebill.Company'])),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('rtp_ip', self.gf('django.db.models.fields.CharField')(default='auto', max_length=100)),
            ('sip_ip', self.gf('django.db.models.fields.CharField')(default='auto', max_length=100)),
            ('sip_port', self.gf('django.db.models.fields.PositiveIntegerField')(default=5060)),
            ('log_auth_failures', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('multiple_registrations', self.gf('django.db.models.fields.CharField')(default='false', max_length=100)),
            ('outbound_caller_id_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('outbound_caller_id_number', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pyfreebill', ['CustomerDirectory'])

        # Adding model 'LCRGroup'
        db.create_table('lcr_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('lcrtype', self.gf('django.db.models.fields.CharField')(default='p', max_length=10)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pyfreebill', ['LCRGroup'])

        # Adding model 'Lcr'
        db.create_table('lcr', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['country_dialcode.Country'])),
            ('digits', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('sell_rate', self.gf('django.db.models.fields.DecimalField')(default='', max_digits=11, decimal_places=5, blank=True)),
            ('cost_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=5)),
            ('carrier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pyfreebill.Company'])),
            ('lead_strip', self.gf('django.db.models.fields.CharField')(default='', max_length=15, blank=True)),
            ('tail_strip', self.gf('django.db.models.fields.CharField')(default='', max_length=15, blank=True)),
            ('prefix', self.gf('django.db.models.fields.CharField')(default='', max_length=15, blank=True)),
            ('suffix', self.gf('django.db.models.fields.CharField')(default='', max_length=15, blank=True)),
            ('lcr_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pyfreebill.LCRGroup'])),
            ('date_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')()),
            ('quality', self.gf('django.db.models.fields.IntegerField')(default='', blank=True)),
            ('reliability', self.gf('django.db.models.fields.IntegerField')(default='', blank=True)),
            ('cid', self.gf('django.db.models.fields.CharField')(default='', max_length=25, blank=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pyfreebill', ['Lcr'])

        # Adding model 'RateCard'
        db.create_table('ratecard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('lcrgroup', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pyfreebill.LCRGroup'])),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pyfreebill', ['RateCard'])

        # Adding model 'Rates'
        db.create_table('rates', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ratecard', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pyfreebill.RateCard'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['country_dialcode.Country'])),
            ('prefix', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('rate', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=5)),
            ('block_min_duration', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('init_block', self.gf('django.db.models.fields.DecimalField')(default=1, max_digits=11, decimal_places=5)),
            ('date_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')()),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pyfreebill', ['Rates'])

        # Adding model 'CustomerRateCards'
        db.create_table('customer_ratecards', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pyfreebill.Company'])),
            ('ratecard', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pyfreebill.RateCard'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tech_prefix', self.gf('django.db.models.fields.CharField')(default='', max_length=15, blank=True)),
            ('priority', self.gf('django.db.models.fields.IntegerField')()),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pyfreebill', ['CustomerRateCards'])

        # Adding model 'AclLists'
        db.create_table('acl_lists', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('acl_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('default_policy', self.gf('django.db.models.fields.CharField')(default='deny', max_length=10)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pyfreebill', ['AclLists'])

        # Adding model 'AclNodes'
        db.create_table('acl_nodes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pyfreebill.Company'])),
            ('cidr', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('policy', self.gf('django.db.models.fields.CharField')(default='allow', max_length=10)),
            ('list', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pyfreebill.AclLists'])),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pyfreebill', ['AclNodes'])

        # Adding model 'SipProfile'
        db.create_table('sip_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('ext_rtp_ip', self.gf('django.db.models.fields.CharField')(default='auto', max_length=100)),
            ('ext_sip_ip', self.gf('django.db.models.fields.CharField')(default='auto', max_length=100)),
            ('rtp_ip', self.gf('django.db.models.fields.CharField')(default='auto', max_length=100)),
            ('sip_ip', self.gf('django.db.models.fields.CharField')(default='auto', max_length=100)),
            ('sip_port', self.gf('django.db.models.fields.PositiveIntegerField')(default=5060)),
            ('accept_blind_reg', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('auth_calls', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('log_auth_failures', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pyfreebill', ['SipProfile'])

        # Adding model 'SofiaGateway'
        db.create_table('sofia_gateway', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('sip_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pyfreebill.SipProfile'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pyfreebill.Company'])),
            ('channels', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('prefix', self.gf('django.db.models.fields.CharField')(default='', max_length=15, blank=True)),
            ('suffix', self.gf('django.db.models.fields.CharField')(default='', max_length=15, blank=True)),
            ('codec', self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(default='', max_length=35, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(default='', max_length=35, blank=True)),
            ('register', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('proxy', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('extension', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True)),
            ('realm', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True)),
            ('from_domain', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True)),
            ('expire_seconds', self.gf('django.db.models.fields.PositiveIntegerField')(default=3600, null=True)),
            ('retry_seconds', self.gf('django.db.models.fields.PositiveIntegerField')(default=30, null=True)),
            ('caller_id_in_from', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sip_cid_type', self.gf('django.db.models.fields.CharField')(default='rpid', max_length=10)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pyfreebill', ['SofiaGateway'])


    def backwards(self, orm):
        # Deleting model 'Company'
        db.delete_table('company')

        # Deleting model 'Person'
        db.delete_table('contacts_people')

        # Deleting model 'Group'
        db.delete_table('contacts_groups')

        # Removing M2M table for field people on 'Group'
        db.delete_table('contacts_groups_people')

        # Removing M2M table for field companies on 'Group'
        db.delete_table('contacts_groups_companies')

        # Deleting model 'PhoneNumber'
        db.delete_table('contacts_phone_numbers')

        # Deleting model 'EmailAddress'
        db.delete_table('contacts_email_addresses')

        # Deleting model 'InstantMessenger'
        db.delete_table('contacts_instant_messengers')

        # Deleting model 'WebSite'
        db.delete_table('contacts_web_sites')

        # Deleting model 'StreetAddress'
        db.delete_table('contacts_street_addresses')

        # Deleting model 'SpecialDate'
        db.delete_table('contacts_special_dates')

        # Deleting model 'CompanyBalanceHistory'
        db.delete_table('company_balance_history')

        # Deleting model 'CustomerDirectory'
        db.delete_table('customer_directory')

        # Deleting model 'LCRGroup'
        db.delete_table('lcr_group')

        # Deleting model 'Lcr'
        db.delete_table('lcr')

        # Deleting model 'RateCard'
        db.delete_table('ratecard')

        # Deleting model 'Rates'
        db.delete_table('rates')

        # Deleting model 'CustomerRateCards'
        db.delete_table('customer_ratecards')

        # Deleting model 'AclLists'
        db.delete_table('acl_lists')

        # Deleting model 'AclNodes'
        db.delete_table('acl_nodes')

        # Deleting model 'SipProfile'
        db.delete_table('sip_profile')

        # Deleting model 'SofiaGateway'
        db.delete_table('sofia_gateway')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'comments.comment': {
            'Meta': {'ordering': "('submit_date',)", 'object_name': 'Comment', 'db_table': "'django_comments'"},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_comment'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_pk': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comment_comments'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'country_dialcode.country': {
            'Meta': {'object_name': 'Country', 'db_table': "'dialcode_country'"},
            'countrycode': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'countryname': ('django.db.models.fields.CharField', [], {'max_length': '240'}),
            'countryprefix': ('django.db.models.fields.IntegerField', [], {'max_length': '12'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2'})
        },
        u'pyfreebill.acllists': {
            'Meta': {'ordering': "('acl_name',)", 'object_name': 'AclLists', 'db_table': "'acl_lists'"},
            'acl_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'default_policy': ('django.db.models.fields.CharField', [], {'default': "'deny'", 'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'pyfreebill.aclnodes': {
            'Meta': {'ordering': "('company', 'policy', 'cidr')", 'object_name': 'AclNodes', 'db_table': "'acl_nodes'"},
            'cidr': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pyfreebill.Company']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pyfreebill.AclLists']"}),
            'policy': ('django.db.models.fields.CharField', [], {'default': "'allow'", 'max_length': '10'})
        },
        u'pyfreebill.company': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Company', 'db_table': "'company'"},
            'about': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '4'}),
            'billing_cycle': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '10'}),
            'credit_limit': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '4'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_calls': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'prepaid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'vat': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vat_number': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'pyfreebill.companybalancehistory': {
            'Meta': {'ordering': "('company', 'date_added')", 'object_name': 'CompanyBalanceHistory', 'db_table': "'company_balance_history'"},
            'amount_debited': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'}),
            'amount_refund': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'}),
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '4'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pyfreebill.Company']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'pyfreebill.customerdirectory': {
            'Meta': {'ordering': "('company', 'name')", 'object_name': 'CustomerDirectory', 'db_table': "'customer_directory'"},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pyfreebill.Company']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_auth_failures': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'multiple_registrations': ('django.db.models.fields.CharField', [], {'default': "'false'", 'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'outbound_caller_id_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'outbound_caller_id_number': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'rtp_ip': ('django.db.models.fields.CharField', [], {'default': "'auto'", 'max_length': '100'}),
            'sip_ip': ('django.db.models.fields.CharField', [], {'default': "'auto'", 'max_length': '100'}),
            'sip_port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '5060'})
        },
        u'pyfreebill.customerratecards': {
            'Meta': {'ordering': "('company', 'priority', 'ratecard')", 'object_name': 'CustomerRateCards', 'db_table': "'customer_ratecards'"},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pyfreebill.Company']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {}),
            'ratecard': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pyfreebill.RateCard']"}),
            'tech_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'blank': 'True'})
        },
        u'pyfreebill.emailaddress': {
            'Meta': {'object_name': 'EmailAddress', 'db_table': "'contacts_email_addresses'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'email_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "'work'", 'max_length': '6'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        },
        u'pyfreebill.group': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Group', 'db_table': "'contacts_groups'"},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'companies': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pyfreebill.Company']", 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'people': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['pyfreebill.Person']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'pyfreebill.instantmessenger': {
            'Meta': {'object_name': 'InstantMessenger', 'db_table': "'contacts_instant_messengers'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'im_account': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "'work'", 'max_length': '6'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'service': ('django.db.models.fields.CharField', [], {'default': "'jabber'", 'max_length': '11'})
        },
        u'pyfreebill.lcr': {
            'Meta': {'ordering': "('enabled', 'lcr_profile', 'digits')", 'object_name': 'Lcr', 'db_table': "'lcr'"},
            'carrier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pyfreebill.Company']"}),
            'cid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25', 'blank': 'True'}),
            'cost_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '5'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['country_dialcode.Country']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {}),
            'digits': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lcr_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pyfreebill.LCRGroup']"}),
            'lead_strip': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'quality': ('django.db.models.fields.IntegerField', [], {'default': "''", 'blank': 'True'}),
            'reliability': ('django.db.models.fields.IntegerField', [], {'default': "''", 'blank': 'True'}),
            'sell_rate': ('django.db.models.fields.DecimalField', [], {'default': "''", 'max_digits': '11', 'decimal_places': '5', 'blank': 'True'}),
            'suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'tail_strip': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'blank': 'True'})
        },
        u'pyfreebill.lcrgroup': {
            'Meta': {'ordering': "('name',)", 'object_name': 'LCRGroup', 'db_table': "'lcr_group'"},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lcrtype': ('django.db.models.fields.CharField', [], {'default': "'p'", 'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'pyfreebill.person': {
            'Meta': {'ordering': "('last_name', 'first_name')", 'object_name': 'Person', 'db_table': "'contacts_people'"},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pyfreebill.Company']", 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'pyfreebill.phonenumber': {
            'Meta': {'object_name': 'PhoneNumber', 'db_table': "'contacts_phone_numbers'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "'work'", 'max_length': '6'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'pyfreebill.ratecard': {
            'Meta': {'ordering': "('name', 'enabled')", 'object_name': 'RateCard', 'db_table': "'ratecard'"},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lcrgroup': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pyfreebill.LCRGroup']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'pyfreebill.rates': {
            'Meta': {'ordering': "('ratecard', 'prefix', 'enabled')", 'object_name': 'Rates', 'db_table': "'rates'"},
            'block_min_duration': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['country_dialcode.Country']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'init_block': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '11', 'decimal_places': '5'}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '5'}),
            'ratecard': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pyfreebill.RateCard']"})
        },
        u'pyfreebill.sipprofile': {
            'Meta': {'ordering': "('name',)", 'object_name': 'SipProfile', 'db_table': "'sip_profile'"},
            'accept_blind_reg': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'auth_calls': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'ext_rtp_ip': ('django.db.models.fields.CharField', [], {'default': "'auto'", 'max_length': '100'}),
            'ext_sip_ip': ('django.db.models.fields.CharField', [], {'default': "'auto'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_auth_failures': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rtp_ip': ('django.db.models.fields.CharField', [], {'default': "'auto'", 'max_length': '100'}),
            'sip_ip': ('django.db.models.fields.CharField', [], {'default': "'auto'", 'max_length': '100'}),
            'sip_port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '5060'})
        },
        u'pyfreebill.sofiagateway': {
            'Meta': {'ordering': "('company', 'name')", 'object_name': 'SofiaGateway', 'db_table': "'sofia_gateway'"},
            'caller_id_in_from': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'channels': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'codec': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pyfreebill.Company']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'expire_seconds': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3600', 'null': 'True'}),
            'extension': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'from_domain': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '35', 'blank': 'True'}),
            'prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'proxy': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'realm': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'register': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'retry_seconds': ('django.db.models.fields.PositiveIntegerField', [], {'default': '30', 'null': 'True'}),
            'sip_cid_type': ('django.db.models.fields.CharField', [], {'default': "'rpid'", 'max_length': '10'}),
            'sip_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pyfreebill.SipProfile']"}),
            'suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '35', 'blank': 'True'})
        },
        u'pyfreebill.specialdate': {
            'Meta': {'object_name': 'SpecialDate', 'db_table': "'contacts_special_dates'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'every_year': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'occasion': ('django.db.models.fields.TextField', [], {'max_length': '200'})
        },
        u'pyfreebill.streetaddress': {
            'Meta': {'object_name': 'StreetAddress', 'db_table': "'contacts_street_addresses'"},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "'work'", 'max_length': '6'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'street': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'pyfreebill.website': {
            'Meta': {'object_name': 'WebSite', 'db_table': "'contacts_web_sites'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "'work'", 'max_length': '6'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['pyfreebill']