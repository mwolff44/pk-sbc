# Copyright 2013 Mathias WOLFF
# This file is part of pyfreebilling.
# 
# pyfreebilling is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# pyfreebilling is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with pyfreebilling.  If not, see <http://www.gnu.org/licenses/>

from django.db import models
from django.db.models import permalink
from django.core.validators import EMPTY_VALUES
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericRelation
from django.utils.translation import ugettext_lazy as _
from country_dialcode.models import Country, Prefix
from pyfreebill import fields

# Finance

class Company(models.Model):
    """Company model."""
    name = models.CharField(_(u'name'), max_length=200)
    nickname = models.CharField(_('nickname'), max_length=50, blank=True, null=True)
    slug = models.SlugField(_('slug'), max_length=50, unique=True)
    about = models.TextField(_(u'about'), blank=True, null=True)
    phone_number = GenericRelation(u'PhoneNumber')
    email_address = GenericRelation(u'EmailAddress')
    web_site = GenericRelation(u'WebSite')
    street_address = GenericRelation(u'StreetAddress')
    note = GenericRelation(Comment, object_id_field='object_pk')
    vat = models.BooleanField(_(u"VAT Applicable / Not applicable"), default=False, help_text=_(u"if checked, VAT is applicable."))
    vat_number = models.TextField(_(u"VAT number"), blank=True)
    prepaid = models.BooleanField(_(u"Prepaid / Postpaid"), default=True, help_text=_(u"If checked, this account customer is prepaid."))
    credit_limit = models.DecimalField(_(u'credit limit'), max_digits=12, decimal_places=4, default=0, help_text=_(u"Credit limit for postpaid account."))
    balance = models.DecimalField(_(u'balance'), max_digits=12, decimal_places=4, default=0, help_text=_(u"Actual balance."))
    max_calls = models.PositiveIntegerField(_(u'max simultaneous calls'), default=1, help_text=_(u"maximum simultaneous calls allowed for this customer account."))
    BILLING_CYCLE_CHOICES = (
        ('w', _(u'weekly')),
        ('m', _(u'monthly')),
    )
    billing_cycle = models.CharField(_(u'billing cycle'), max_length=10, choices=BILLING_CYCLE_CHOICES, default='m', help_text=_(u"billinng cycle for invoice generation."))
    enabled = models.BooleanField(_(u"Enabled / Disabled"), default=False)
    date_added = models.DateTimeField(_(u'date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'), auto_now=True)


    class Meta:
        db_table = 'company'
        ordering = ('name',)
        verbose_name = _(u"Company")
        verbose_name_plural = _(u"Companies")

    def __unicode__(self):
        return u"%s" % self.name

class Person(models.Model):
    """Person model."""
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=200)
    middle_name = models.CharField(_('middle name'), max_length=200, blank=True, null=True)
    suffix = models.CharField(_('suffix'), max_length=50, blank=True, null=True)
    nickname = models.CharField(_('nickname'), max_length=100, blank=True)
    slug = models.SlugField(_('slug'), max_length=50, unique=True)
    title = models.CharField(_('title'), max_length=200, blank=True)
    company = models.ForeignKey(Company, blank=True, null=True)
    about = models.TextField(_('about'), blank=True)
    user = models.OneToOneField(User, blank=True, null=True,verbose_name=_('user'))
    phone_number = GenericRelation('PhoneNumber')
    email_address = GenericRelation('EmailAddress')
    instant_messenger = GenericRelation('InstantMessenger')
    special_date = GenericRelation('SpecialDate')
    note = GenericRelation(Comment, object_id_field='object_pk')
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    class Meta:
        db_table = 'contacts_people'
        ordering = ('last_name', 'first_name')
        verbose_name = _('person')
        verbose_name_plural = _('people')

    def __unicode__(self):
        return self.fullname

    @property
    def fullname(self):
        return u"%s %s" % (self.first_name, self.last_name)

class Group(models.Model):
    """Group model."""
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=50, unique=True)
    about = models.TextField(_('about'), blank=True)
    people = models.ManyToManyField(Person, verbose_name='people', blank=True,null=True)
    companies = models.ManyToManyField(Company, verbose_name='companies',blank=True, null=True)
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    class Meta:
        db_table = 'contacts_groups'
        ordering = ('name',)
        verbose_name = _('group')
        verbose_name_plural = _('groups')

    def __unicode__(self):
        return u"%s" % self.name

PHONE_LOCATION_CHOICES = (
    ('work', _('Work')),
    ('mobile', _('Mobile')),
    ('fax', _('Fax')),
    ('pager', _('Pager')),
    ('home', _('Home')),
    ('other', _('Other')),
)

class PhoneNumber(models.Model):
    """Phone Number model."""
    content_type = models.ForeignKey(ContentType, limit_choices_to={'app_label': 'contacts'})
    object_id = models.IntegerField(db_index=True)
    content_object = generic.GenericForeignKey()
    phone_number = models.CharField(_('number'), max_length=50)
    location = models.CharField(_('location'), max_length=6, choices=PHONE_LOCATION_CHOICES, default='work')
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.phone_number, self.location)

    class Meta:
        db_table = 'contacts_phone_numbers'
        verbose_name = 'phone number'
        verbose_name_plural = 'phone numbers'

LOCATION_CHOICES = (
    ('work', _('Work')),
    ('home', _('Home')),
    ('mobile', _('Mobile')),
    ('fax', _('Fax')),
    ('person', _('Personal')),
    ('other', _('Other'))
)

class EmailAddress(models.Model):
    content_type = models.ForeignKey(ContentType, limit_choices_to={'app_label': 'contacts'})
    object_id = models.IntegerField(db_index=True)
    content_object = generic.GenericForeignKey()
    email_address = models.EmailField(_('email address'))
    location = models.CharField(_('location'), max_length=6, choices=LOCATION_CHOICES, default='work')
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.email_address, self.location)

    class Meta:
        db_table = 'contacts_email_addresses'
        verbose_name = 'email address'
        verbose_name_plural = 'email addresses'

IM_SERVICE_CHOICES = (
    ('aim', 'AIM'),
    ('msn', 'MSN'),
    ('icq', 'ICQ'),
    ('jabber', 'Jabber'),
    ('yahoo', 'Yahoo'),
    ('skype', 'Skype'),
    ('qq', 'QQ'),
    ('sametime', 'Sametime'),
    ('gadu-gadu', 'Gadu-Gadu'),
    ('google-talk', 'Google Talk'),
    ('twitter', 'Twitter'),
    ('other', _('Other'))
)

class InstantMessenger(models.Model):
    content_type = models.ForeignKey(ContentType, limit_choices_to={'app_label': 'contacts'})
    object_id = models.IntegerField(db_index=True)
    content_object = generic.GenericForeignKey()
    im_account = models.CharField(_('im account'), max_length=100)
    location = models.CharField(_('location'), max_length=6, choices=LOCATION_CHOICES, default='work')
    service = models.CharField(_('service'), max_length=11, choices=IM_SERVICE_CHOICES, default='jabber')
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.im_account, self.location)

    class Meta:
        db_table = 'contacts_instant_messengers'
        verbose_name = 'instant messenger'
        verbose_name_plural = 'instant messengers'

class WebSite(models.Model):
    content_type = models.ForeignKey(ContentType, limit_choices_to={'app_label': 'contacts'})
    object_id = models.IntegerField(db_index=True)
    content_object = generic.GenericForeignKey()
    url = models.URLField(_('URL'))
    location = models.CharField(_('location'), max_length=6, choices=LOCATION_CHOICES, default='work')
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.url, self.location)

    class Meta:
        db_table = 'contacts_web_sites'
        verbose_name = _('web site')
        verbose_name_plural = _('web sites')

    def get_absolute_url(self):
        return u"%s?web_site=%s" % (self.content_object.get_absolute_url(), self.pk)

class StreetAddress(models.Model):
    content_type = models.ForeignKey(ContentType, limit_choices_to={'app_label': 'contacts'})
    object_id = models.IntegerField(db_index=True)
    content_object = generic.GenericForeignKey()
    street = models.TextField(_('street'), blank=True)
    city = models.CharField(_('city'), max_length=200, blank=True)
    province = models.CharField(_('province'), max_length=200, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=10, blank=True)
    country = models.CharField(_('country'), max_length=100)
    location = models.CharField(_('location'), max_length=6, choices=LOCATION_CHOICES, default='work')
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.city, self.location)

    class Meta:
        db_table = 'contacts_street_addresses'
        verbose_name = _('street address')
        verbose_name_plural = _('street addresses')

class SpecialDate(models.Model):
    content_type = models.ForeignKey(ContentType,
    limit_choices_to={'app_label': 'contacts'})
    object_id = models.IntegerField(db_index=True)
    content_object = generic.GenericForeignKey()
    occasion = models.TextField(_('occasion'), max_length=200)
    date = models.DateField(_('date'))
    every_year = models.BooleanField(_('every year'), default=True)
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    def __unicode__(self):
        return u"%s: %s" % (self.occasion, self.date)

    class Meta:
        db_table = 'contacts_special_dates'
        verbose_name = _('special date')
        verbose_name_plural = _('special dates')

class CompanyBalanceHistory(models.Model):
    """ Company balance history Model """
    company = models.ForeignKey(Company, verbose_name=_(u"company"))
    amount_debited = models.DecimalField(_(u'amount debited'), max_digits=12, decimal_places=4)
    amount_refund = models.DecimalField(_(u'amount refund'), max_digits=12, decimal_places=4)
    balance = models.DecimalField(_(u'balance'), max_digits=12, decimal_places=4, default=0, help_text=_(u"Resulting balance."))
    reference = models.TextField(_(u'reference'), blank=True)
    description = models.TextField(_(u'description'), blank=True)
    date_added = models.DateTimeField(_(u'date added'), auto_now_add=True) 
    date_modified = models.DateTimeField(_(u'date modified'), auto_now=True)

    class Meta:
        db_table = 'company_balance_history'
        ordering = ('company', 'date_added')
        verbose_name = _(u'Company balance history')
        verbose_name_plural = _(u'Company balance history')

    def __unicode__(self):
        return u"%s %s %s %s" % (self.company, self.amount_debited, self.amount_refund, self.balance)

class CustomerDirectory(models.Model):
    """ Customer Directory Model """
    company = models.ForeignKey(Company, verbose_name=_(u"company"))
    name = models.CharField(_('name'), max_length=200)
    password = models.CharField(_(u"password"), max_length=100, blank=True, help_text=_(u"It's recomended to use strong passwords for the endpoint."))
    description = models.TextField(_(u'description'), blank=True)
    name = models.CharField(_(u"SIP profile name"), max_length=50, help_text=_(u"E.g.: external, internal, etc..."))
    rtp_ip = models.CharField(_(u"RTP IP"), max_length=100, default="auto", help_text=_(u"Internal IP address to bind to for RTP."))
    sip_ip = models.CharField(_(u"SIP IP"), max_length=100, default="auto", help_text=_(u"Internal IP address to bind to for SIP."))
    sip_port = models.PositiveIntegerField(_(u"SIP port"), default=5060)
    log_auth_failures = models.BooleanField(_(u"log auth failures"), default=False, help_text=_(u"It true, log authentication failures. Required for Fail2ban."))
    MULTIPLE_REGISTRATIONS_CHOICES = (
        ("call-id", _(u"Call-id")), ("contact", _(u"Contact")),
        ("false", _(u"False")), ("true", _(u"True")))
    multiple_registrations = models.CharField(_(u"multiple registrations"), max_length=100, default="false", choices=MULTIPLE_REGISTRATIONS_CHOICES, help_text=_(u"Used to allow to call one extension and ring several phones."))
    outbound_caller_id_name = models.CharField(_(u"outbound CallerID name"), max_length=50, blank=True, help_text=_(u"Caller ID name sent to provider on outbound calls."))
    outbound_caller_id_number = models.CharField(_(u"outbound CallerID number"), max_length=80, blank=True, help_text=_(u"Caller ID number sent to provider on outbound calls."))
    enabled = models.BooleanField(_(u"Enabled / Disabled"), default=True)
    date_added = models.DateTimeField(_(u'date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'), auto_now=True)

    class Meta:
        db_table = 'customer_directory'
        ordering = ('company', 'name')
        verbose_name = _(u'Customer sip account')
        verbose_name_plural = _(u'Customer sip accounts')

    def __unicode__(self):
        return "%s (%s:%s)" % (self.name, self.sip_ip, self.sip_port)


# Provider Rates

class ProviderTariff(models.Model):
    """ Provider tariff """
    name = models.CharField(_(u"name"), max_length=128)
    carrier = models.ForeignKey(Company)
    lead_strip = models.CharField(_(u'lead strip'), blank=True, default='', max_length=15)
    tail_strip = models.CharField(_(u'tail strip'), blank=True, default='', max_length=15)
    prefix = models.CharField(_(u'prefix'), blank=True, default='', max_length=15)
    suffix = models.CharField(_(u'suffix'), blank=True, default='', max_length=15)
    description = models.TextField(_(u'description'), blank=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    quality = models.IntegerField(_(u'quality'), blank=True, default='100', help_text=_(u"Alternate field to order by."))
    reliability = models.IntegerField(_(u'reliability'), blank=True, default='100', help_text=_(u"Alternate field to order by."))
    cid = models.CharField(_(u'cid'), blank=True, default='', max_length=25, help_text=_(u"Regex to modify CallerID number."))
    enabled = models.BooleanField(_(u"Enabled / Disabled"), default=True)
    date_added = models.DateTimeField(_(u'date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'), auto_now=True)

    class Meta:
        db_table = 'provider_tariff'
        ordering = ('enabled', 'quality', 'reliability')
        verbose_name = _(u'provider tariff')
        verbose_name_plural = _(u'provider tariffs')

    def __unicode__(self):  
        return u"%s" % self.name

class ProviderRates(models.Model):
    """ Provider Rates Model """
    digits = models.CharField(_(u'numeric prefix'), max_length=30)
    cost_rate = models.DecimalField(_(u'Cost rate'), max_digits=11, decimal_places=5)
    block_min_duration = models.IntegerField(_(u'block min duration'), default=1)
    init_block = models.DecimalField(_(u'Init block rate'), max_digits=11, decimal_places=5, default=1)
    provider_tariff = models.ForeignKey(ProviderTariff)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    enabled = models.BooleanField(_(u"Enabled / Disabled"), default=True)
    date_added = models.DateTimeField(_(u'date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'), auto_now=True)

    class Meta:
        db_table = 'provider_rates'
        ordering = ('enabled', 'provider_tariff', 'digits')
        index_together = [
            ["provider_tariff" ,"digits", "enabled"],
        ]
        verbose_name = _(u'provider rate')
        verbose_name_plural = _(u'provider rates')

    def __unicode__(self):
        return u"%s %s %s " % (self.digits, self.cost_rate, self.provider_tariff)

# LCR

class LCRGroup(models.Model):
    """ LCR group model """
    name = models.CharField(_(u"name"), max_length=128, unique=True)
    description = models.TextField(_(u'description'), blank=True)
    LCR_TYPE_CHOICES = (
        ('p', _(u"lower price")),
        ('q', _(u"best quality")),
        ('r',_(u"best reliability")),
    )
    lcrtype = models.CharField(_(u"lcr type"), max_length=10, choices=LCR_TYPE_CHOICES, default='p')
    date_added = models.DateTimeField(_(u'date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'), auto_now=True)

    class Meta:
        db_table = 'lcr_group'
        ordering = ('name',) 
        verbose_name = _(u'LCR')
        verbose_name_plural = _(u'LCRs')

    def __unicode__(self):   
        return u"%s %s " % (self.name, self.lcrtype)

class LCRProviders(models.Model):
    """ LCR group model """
    lcr = models.ForeignKey(LCRGroup, verbose_name=_(u"LCR"))
    provider_tariff = models.ForeignKey(ProviderTariff, verbose_name=_(u"Provider tariff"))
    date_added = models.DateTimeField(_(u'date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'), auto_now=True)

    class Meta:
        db_table = 'lcr_providers'
        verbose_name = _(u'LCR provider')
        verbose_name_plural = _(u'LCR providers')

    def __unicode__(self):
        return u"%s - %s " % (self.lcr, self.provider_tariff)


# Ratecard

class RateCard(models.Model):
    """ RateCard Model """
    name = models.CharField(_(u'name'), max_length=128, unique=True)
    description = models.TextField(_(u'description'), blank=True)
    lcrgroup = models.ForeignKey(LCRGroup, verbose_name=_(u"lcr"))
    enabled = models.BooleanField(_(u"Enabled / Disabled"), default=False)
    date_added = models.DateTimeField(_(u'date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'), auto_now=True)

    class Meta:
        db_table = 'ratecard'
        ordering = ('name', 'enabled')
        verbose_name = _(u'RateCard')
        verbose_name_plural = _(u'RateCards')

    def __unicode__(self):
        return u"%s" % self.name

class CustomerRates(models.Model):
    """ Customer Rates Model """
    ratecard = models.ForeignKey(RateCard, verbose_name=_(u"ratecard"))
    prefix = models.CharField(_(u'numeric prefix'), max_length=30)
    rate = models.DecimalField(_(u'sell rate'), max_digits=11, decimal_places=5)
    block_min_duration = models.IntegerField(_(u'block min duration'), default=1)
    init_block = models.DecimalField(_(u'Init block rate'), max_digits=11, decimal_places=5, default=1)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    enabled = models.BooleanField(_(u"Enabled"), default=True)
    date_added = models.DateTimeField(_(u'date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'), auto_now=True)

    class Meta:
        db_table = 'customer_rates'
        ordering = ('ratecard', 'prefix', 'enabled')
        verbose_name = _(u'customer rate')
        verbose_name_plural = _(u'customer rates')

    def __unicode__(self):
        return u"%s" % self.ratecard

class CustomerRateCards(models.Model):
    """ Customer rates Cards Model """
    company = models.ForeignKey(Company, verbose_name=_(u"company"))
    ratecard = models.ForeignKey(RateCard, verbose_name=_(u"ratecard"))
    description = models.TextField(_(u'description'), blank=True)
    tech_prefix = models.CharField(_(u"technical prefix"), blank=True, default='', max_length=15)
    priority = models.IntegerField(_(u'priority'), help_text=_(u"Priority order, 1 is the higher priority and 3 the lower one. Correct values are : 1, 2 or 3 !."))
    discount = models.DecimalField(_(u'discount'), max_digits=3, decimal_places=2, default=0, help_text=_(u"ratecard discount. For 10% discount, enter 10 !"))
    date_added = models.DateTimeField(_(u'date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'), auto_now=True)

    class Meta:
        db_table = 'customer_ratecards'
        ordering = ('company', 'priority', 'ratecard')
        verbose_name = _(u'Customer Ratecard')
        verbose_name_plural = _(u'Customer ratecards')

    def __unicode__(self):
        return u"%s %s %s" % (self.company, self.ratecard, self.tech_prefix)

# ACL

class AclLists(models.Model):
    """ ACL list model """
    acl_name = models.CharField(_(u'name'), max_length=128)
    DEFAULT_POLICY_CHOICES = (
        ('deny', _(u'deny')),
        ('allow', _(u'allow')),
    )
    default_policy = models.CharField(_(u'default policy'), max_length=10, choices=DEFAULT_POLICY_CHOICES, default='deny')
    date_added = models.DateTimeField(_(u'date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'), auto_now=True)

    class Meta:
        db_table = 'acl_lists'
        ordering = ('acl_name',)
        verbose_name = _(u'ACL list')
        verbose_name_plural = _(u'ACL lists')

    def __unicode__(self):
        return u"%s" % self.acl_name


class AclNodes(models.Model):
    """ ACL NODES model """
    company = models.ForeignKey(Company, verbose_name=_(u"company"))
    cidr = models.CharField(_(u"ip/cidr Address"), max_length=100, help_text=_(u"Customer IP or cidr address."))
    POLICY_CHOICES = (
        ('deny', _('deny')),
        ('allow', _('allow')),
    )
    policy = models.CharField(_(u"policy"), max_length=10, choices=POLICY_CHOICES, default='allow')
    list = models.ForeignKey(AclLists, verbose_name=_(u"acl list"))
    date_added = models.DateTimeField(_(u'date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'), auto_now=True)

    class Meta:
        db_table = 'acl_nodes'
        ordering = ('company', 'policy', 'cidr')
        verbose_name = _(u'ACL node')
        verbose_name_plural = _(u'ACL nodes')

    def __unicode__(self):
        return u"%s %s" % (self.company, self.cidr)

# VOIP SWITCH

class VoipSwitch(models.Model):
    """ VoipSwitch Profile """
    name = models.CharField(_(u"SIP profile name"), max_length=50, help_text=_(u"E.g.: external, internal, etc..."))
    ip = models.CharField(_(u"switch IP"), max_length=100, default="auto", help_text=_(u"Switch IP."))
    date_added = models.DateTimeField(_(u'date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'), auto_now=True)

    class Meta:
        db_table = 'voip_switch'
        ordering = ('name', )
        verbose_name = _(u'VoIP Switch')
        verbose_name_plural = _(u'VoIP Switches')

    def __unicode__(self):
        return u"%s (:%s)" % (self.name, self.ip)

# SOFIA 

class SipProfile(models.Model):
    """ Sofia Sip profile """
    name = models.CharField(_(u"SIP profile name"), max_length=50, help_text=_(u"E.g.: the name you want ..."))
    ext_rtp_ip = models.CharField(_(u"external RTP IP"), max_length=100, default="auto", help_text=_(u"External/public IP address to bind to for RTP."))
    ext_sip_ip = models.CharField(_(u"external SIP IP"), max_length=100, default="auto", help_text=_(u"External/public IP address to bind to for SIP."))
    rtp_ip = models.CharField(_(u"RTP IP"), max_length=100, default="auto", help_text=_(u"Internal IP address to bind to for RTP."))
    sip_ip = models.CharField(_(u"SIP IP"), max_length=100, default="auto", help_text=_(u"Internal IP address to bind to for SIP."))
    sip_port = models.PositiveIntegerField(_(u"SIP port"), default=5060)
    disable_transcoding = models.BooleanField(_(u"disable transcoding"), default=True, help_text=_(u"If true, you can not use transcoding."))
    accept_blind_reg = models.BooleanField(_(u"accept blind registration"), default=False, help_text=_(u"If true, anyone can register to server and will not be challenged for username/password information."))
    auth_calls = models.BooleanField(_(u"authenticate calls"), default=True, help_text=_(u"If true, FreeeSWITCH will authorize all calls "
            "on this profile, i.e. challenge the other side for "
            "username/password information."))
    log_auth_failures = models.BooleanField(_(u"log auth failures"), default=False, help_text=_(u"It true, log authentication failures. Required for Fail2ban."))
    inbound_codec_prefs = models.CharField(_(u"inbound codec prefs"), max_length=100, default="G729,PCMU,PCMA", help_text=_(u"Define allowed preferred codecs for inbound calls."))
    outbound_codec_prefs = models.CharField(_(u"outbound codec prefs"), max_length=100, default="G729,PCMU,PCMA", help_text=_(u"Define allowed preferred codecs for outbound calls."))
    date_added = models.DateTimeField(_(u'date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'), auto_now=True)

    class Meta:
        db_table = 'sip_profile'
        ordering = ('name', )
        verbose_name = _(u'SIP profile')
        verbose_name_plural = _(u'SIP profiles')

    def __unicode__(self):
        return u"%s (%s:%s)" % (self.name, self.sip_ip, self.sip_port)

    def get_gateways(self):
        """Get all gateways in the system assigned to this sip profile."""
        retval = []  
        accounts = Company.objects.filter(enabled=True)
        for account in accounts:
            for gateway in account.sofiagateway_set.all():
                if gateway.sip_profile.id == self.id:
                    retval.append(gateway)
        return retval

class SofiaGateway(models.Model):
    name = models.CharField(_(u"name"), max_length=100, unique=True)
    sip_profile = models.ForeignKey('SipProfile', verbose_name=_(u"SIP profile"), help_text=_(u"Which Sip Profile communication with this gateway will take place"
            " on."))
    company = models.ForeignKey(Company, verbose_name=_(u"company"))
    channels = models.PositiveIntegerField(_(u"channels number"), default=1, help_text=_(u"maximum simultaneous calls allowed for this gateway."))
    prefix = models.CharField(_(u'prefix'), blank=True, default='', max_length=15)
    suffix = models.CharField(_(u'suffix'), blank=True, default='', max_length=15)
    codec = models.CharField(_(u'codec'), blank=True, default='', max_length=30)
    username = models.CharField(_(u"username"), blank=True, default='', max_length=35)
    password = models.CharField(_(u"password"), blank=True, default='', max_length=35)
    register = models.BooleanField(_(u"register"), default=False)
    proxy = models.CharField(_(u"proxy"), max_length=48,  help_text=_(u"IP if register is False."))
    extension = models.CharField(_(u"extension number"), max_length=50, blank=True, default="", help_text=_(u"Extension for inbound calls. Same as username, if "
                    "blank."))
    realm = models.CharField(_(u"realm"), max_length=50, blank=True, default="", help_text=_(u"Authentication realm. Same as gateway name, if blank."))
    from_domain = models.CharField(_(u"from domain"), max_length=50, blank=True, default="", help_text=_(u"Domain to use in from field. Same as realm if blank."))
    expire_seconds = models.PositiveIntegerField(_(u"expire seconds"), default=3600, null=True)
    retry_seconds = models.PositiveIntegerField(_(u"retry seconds"), default=30, null=True, help_text=_(u"How many seconds before a retry when a failure or timeout "
            "occurs"))
    caller_id_in_from = models.BooleanField(_(u"caller ID in From field"), default=False, help_text=_(u"Use the callerid of an inbound call in the from field on "
            "outbound calls via this gateway."))
    SIP_CID_TYPE_CHOICES = (
        ('none', _(u'deny')),
        ('default', _(u'allow')),
        ('pid', _(u'pid')),
        ('rpid', _(u'rpid')),
    )
    sip_cid_type = models.CharField(_(u'SIP CID type'), max_length=10, choices=SIP_CID_TYPE_CHOICES, default='rpid', help_text=_(u"Modify callerID in SDP Headers."))
    date_added = models.DateTimeField(_(u'date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'), auto_now=True)

    class Meta:
        db_table = 'sofia_gateway'
        ordering = ('company', 'name')
        verbose_name = _(u"Sofia gateway")
        verbose_name_plural = _(u"Sofia gateways")

    def __unicode__(self):
        return u"%s" % self.name

# Hangup Cause

class HangupCause(models.Model):
    """ Hangup Cause Model """
    code = models.PositiveIntegerField(_(u"Hangup code"), unique=True, help_text=_(u"ITU-T Q.850 Code."))
    enumeration = models.CharField(_(u"enumeration"), max_length=100, null=True, blank=True, help_text=_(u"enumeration."))
    cause = models.CharField(_(u"cause"), max_length=100, null=True, blank=True, help_text=_(u"Cause."))
    description = models.TextField(_(u'description'), blank=True)
    date_added = models.DateTimeField(_(u'date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'), auto_now=True)

    class Meta:
        db_table = 'hangup_cause'
        ordering = ('code',)
        verbose_name = _(u"hangupcause")
        verbose_name_plural = _(u"hangupcauses")

    def __unicode__(self):
        return u"[%s] %s" % (self.code, self.enumeration)

# CDR

class CDR(models.Model):
    """ CDR Model    """
    customer = models.ForeignKey(Company, verbose_name=_(u"customer"), related_name="customer_related")
    customer_ip = models.CharField(_(u"customer IP address"), max_length=100, help_text=_(u"Customer IP address."))
    uuid = models.CharField(_(u"UUID"), max_length=100)
    bleg_uuid = models.CharField(_(u"b leg UUID"), null=True, default="", max_length=100)
    caller_id_number = models.CharField(_(u"caller ID num"), max_length=100)
    destination_number = models.CharField(_(u"Dest. number"), max_length=100)
    chan_name = models.CharField(_(u"channel name"), max_length=100)
    start_stamp = models.DateTimeField(_(u"start time"))
    answered_stamp = models.DateTimeField(_(u"answered time"), null=True)
    end_stamp = models.DateTimeField(_(u"hangup time"))
    duration = models.IntegerField(_(u"duration"))
    billsec = models.IntegerField(_(u"billsec"))
    read_codec = models.CharField(_(u"read codec"), max_length=20)
    write_codec = models.CharField(_(u"write codec"), max_length=20)
    hangup_cause = models.CharField(_(u"hangup cause"), max_length=50)
    hangup_cause_q850 = models.IntegerField(_(u"q.850"))
    gateway = models.ForeignKey(SofiaGateway, verbose_name=_(u"gateway"))
    cost_rate = models.DecimalField(_(u'buy rate'), max_digits=11, decimal_places=5, default="", null=True)
    prefix = models.CharField(_(u'Prefix'), max_length=30)
    country = models.CharField(_(u'Country'), max_length=100)
    rate = models.DecimalField(_(u'sell rate'), max_digits=11, decimal_places=5)
    init_block = models.DecimalField(_(u'Init block rate'), max_digits=11, decimal_places=5)
    block_min_duration = models.IntegerField(_(u'block min duration'))
    lcr_carrier_id = models.ForeignKey(Company, verbose_name=_(u"carrier"), related_name="carrier_related")
    ratecard_id = models.ForeignKey(RateCard, verbose_name=_(u"ratecard"))
    lcr_group_id = models.ForeignKey(LCRGroup, verbose_name=_(u"lcr group"))
    sip_user_agent = models.CharField(_(u'sip user agent'), max_length=100)
    sip_rtp_rxstat = models.CharField(_(u'sip rtp rx stat'), max_length=30)
    sip_rtp_txstat = models.CharField(_(u'sip rtp tx stat'), max_length=30)
    switchname = models.CharField(_(u"switchname"), null=True, default="", max_length=100)
    switch_ipv4 = models.CharField(_(u"switch ipv4"), null=True, default="", max_length=100)
    hangup_disposition = models.CharField(_(u"hangup disposition"), null=True, default="", max_length=100)

    class Meta:
        db_table = 'cdr'
        ordering = ('start_stamp', 'customer')
        verbose_name = _(u"CDR")
        verbose_name_plural = _(u"CDRs")

    def __unicode__(self):
        return u"%s" % self.uuid

