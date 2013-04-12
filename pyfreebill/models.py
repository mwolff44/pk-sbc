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


# LCR

class LCRGroup(models.Model):
    """ LCR group model """
    name = models.CharField(_(u"name"), max_length=128)
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
        verbose_name = _(u'LCR group')
        verbose_name_plural = _(u'LCR groups')

    def __unicode__(self):
        return u"%s %s" % (self.name, self.lcrtype)

class Lcr(models.Model):
    """ LCR Model """
    country = models.ForeignKey(Country, verbose_name=_(u"country"))
    digits = models.CharField(_(u'Country Code'), max_length=15)
    sell_rate = models.DecimalField(_(u'Sell rate'), blank=True, default='', max_digits=11, decimal_places=5)
    cost_rate = models.DecimalField(_(u'Cost rate'), max_digits=11, decimal_places=5)
    carrier = models.ForeignKey(Company)
    lead_strip = models.CharField(_(u'lead strip'), blank=True, default='', max_length=15)
    tail_strip = models.CharField(_(u'tail strip'), blank=True, default='', max_length=15)
    prefix = models.CharField(_(u'prefix'), blank=True, default='', max_length=15)
    suffix = models.CharField(_(u'suffix'), blank=True, default='', max_length=15)
    lcr_profile = models.ForeignKey(LCRGroup, verbose_name=_(u"lcr groupe"))
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    quality = models.IntegerField(_(u'quality'), blank=True, default='', help_text=_(u"Alternate field to order by."))
    reliability = models.IntegerField(_(u'reliability'), blank=True, default='', help_text=_(u"Alternate field to order by."))
    cid = models.CharField(_(u'cid'), blank=True, default='', max_length=25, help_text=_(u"Regex to modify CallerID number."))
    enabled = models.BooleanField(_(u"Enabled / Disabled"), default=True)
    date_added = models.DateTimeField(_(u'date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'), auto_now=True)

    class Meta:
        db_table = 'lcr'
        ordering = ('enabled', 'lcr_profile', 'digits')
        verbose_name = _(u'LCR')
        verbose_name_plural = _(u'LCRs')

    def __unicode__(self):
        return u"%s %s %s %s %s " % (self.country, self.digits, self.cost_rate, self.lcr_profile, self.enabled)

# Ratecard

class RateCard(models.Model):
    """ RateCard Model """
    name = models.CharField(_(u'name'), max_length=128)
    description = models.TextField(_(u'description'), blank=True)
    lcrgroup = models.ForeignKey(LCRGroup, verbose_name=_(u"lcr group"))
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

class Rates(models.Model):
    """ Rates Model """
    ratecard = models.ForeignKey(RateCard, verbose_name=_(u"ratecard"))
    country = models.ForeignKey(Country, verbose_name=_(u"country"))
    prefix = models.CharField(_(u'Regex or numeric prefix'), max_length=30)
    rate = models.DecimalField(_(u'sell rate'), max_digits=11, decimal_places=5)
    block_min_duration = models.IntegerField(_(u'block min duration'), default=1)
    init_block = models.DecimalField(_(u'Init block rate'), max_digits=11, decimal_places=5, default=1)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    enabled = models.BooleanField(_(u"Enabled"), default=True)
    date_added = models.DateTimeField(_(u'date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'), auto_now=True)

    class Meta:
        db_table = 'rates'
        ordering = ('ratecard', 'prefix', 'enabled')
        verbose_name = _(u'Rate')
        verbose_name_plural = _(u'Rates')

    def __unicode__(self):
        return u"%s" % self.ratecard

class CustomerRateCards(models.Model):
    """ Customer rates Cards Model """
    company = models.ForeignKey(Company, verbose_name=_(u"company"))
    ratecard = models.ForeignKey(RateCard, verbose_name=_(u"ratecard"))
    description = models.TextField(_(u'description'), blank=True)
    tech_prefix = models.CharField(_(u"technical prefix"), blank=True, default='', max_length=15)
    priority = models.IntegerField(_(u'priority'), help_text=_(u"Priority order."))
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
    cidr = fields.FSIPAddressField(_(u"ip/cidr Address"), help_text=_(u"Customer IP or cidr address."))
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

# SOFIA 

class SipProfile(models.Model):
    """ Sofia Sip profile """
    name = models.CharField(_(u"SIP profile name"), max_length=50, help_text=_(u"E.g.: external, internal, etc..."))
    ext_rtp_ip = models.CharField(_(u"external RTP IP"), max_length=100, default="auto", help_text=_(u"External/public IP address to bind to for RTP."))
    ext_sip_ip = models.CharField(_(u"external SIP IP"), max_length=100, default="auto", help_text=_(u"External/public IP address to bind to for SIP."))
    rtp_ip = models.CharField(_(u"RTP IP"), max_length=100, default="auto", help_text=_(u"Internal IP address to bind to for RTP."))
    sip_ip = models.CharField(_(u"SIP IP"), max_length=100, default="auto", help_text=_(u"Internal IP address to bind to for SIP."))
    sip_port = models.PositiveIntegerField(_(u"SIP port"), default=5060)
    accept_blind_reg = models.BooleanField(_(u"accept blind registration"), default=False, help_text=_(u"If true, anyone can register to server and will not be challenged for username/password information."))
    auth_calls = models.BooleanField(_(u"authenticate calls"), default=True, help_text=_(u"If true, FreeeSWITCH will authorize all calls "
            "on this profile, i.e. challenge the other side for "
            "username/password information."))
    log_auth_failures = models.BooleanField(_(u"log auth failures"), default=False, help_text=_(u"It true, log authentication failures. Required for Fail2ban."))
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
