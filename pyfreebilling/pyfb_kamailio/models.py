# -*- coding: utf-8 -*-
from django.urls import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Dialog(models.Model):

    # Fields
    hash_entry = models.IntegerField(help_text=_(u"Number of the hash entry in the dialog hash table"))
    hash_id = models.IntegerField(help_text=_(u"The ID on the hash entry"))
    callid = models.CharField(max_length=255, help_text=_(u"Call-ID of the dialog"))
    from_uri = models.CharField(max_length=128, help_text=_(u"The URI of the FROM header (as per INVITE)"))
    from_tag = models.CharField(max_length=64, help_text=_(u"The tag parameter serves as a general mechanism to identify a dialog, which is the combination of the Call-ID along with two tags, one from participant in the dialog."))
    to_uri = models.CharField(max_length=128, help_text=_(u"The URI of the TO header (as per INVITE)"))
    to_tag = models.CharField(max_length=64, help_text=_(u"The tag parameter serves as a general mechanism to identify a dialog, which is the combination of the Call-ID along with two tags, one from participant in the dialog."))
    caller_cseq = models.CharField(max_length=20, help_text=_(u"Last Cseq number on the caller side."))
    callee_cseq = models.CharField(max_length=20, help_text=_(u"Last Cseq number on the callee side."))
    caller_route_set = models.CharField(max_length=512, null=True, blank=True, help_text=_(u"Route set on the caller side."))
    callee_route_set = models.CharField(max_length=512, null=True, blank=True, help_text=_(u"Route set on the callee side."))
    caller_contact = models.CharField(max_length=128, help_text=_(u"Caller's contact uri."))
    callee_contact = models.CharField(max_length=128, help_text=_(u"Callee's contact uri."))
    caller_sock = models.CharField(max_length=64, help_text=_(u"Local socket used to communicate with caller"))
    callee_sock = models.CharField(max_length=64, help_text=_(u"Local socket used to communicate with callee"))
    state = models.IntegerField(help_text=_(u"The state of the dialog."))
    start_time = models.IntegerField(help_text=_(u"The timestamp (unix time) when the dialog was confirmed."))
    timeout = models.IntegerField(help_text=_(u"The timestamp (unix time) when the dialog will expire."))
    sflags = models.IntegerField(help_text=_(u"The flags to set for dialog and accesible from config file."))
    iflags = models.IntegerField(help_text=_(u"The internal flags for dialog."))
    toroute_name = models.CharField(max_length=32, null=True, blank=True, help_text=_(u"The name of route to be executed at dialog timeout."))
    req_uri = models.CharField(max_length=128, help_text=_(u"The URI of initial request in dialog"))
    xdata = models.CharField(max_length=512, blank=True, null=True, help_text=_(u"Extra data associated to the dialog (e.g., serialized profiles)."))


    class Meta:
        db_table = 'dialog'
        ordering = ('-pk',)
        verbose_name = _(u"SIP dialog")
        verbose_name_plural = _(u"SIP dialogs")
        indexes = [
            models.Index(fields=['hash_entry', 'hash_id']),
        ]

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_dialog_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_dialog_update', args=(self.pk,))


class DialogVar(models.Model):

    # Fields
    hash_entry = models.IntegerField(help_text=_(u"Number of the hash entry in the dialog hash table"))
    hash_id = models.IntegerField(help_text=_(u"The ID on the hash entry"))
    dialog_key = models.CharField(max_length=128, help_text=_(u"The key of the dialog variable"))
    dialog_value = models.TextField(help_text=_(u"The value of the dialog variable"))


    class Meta:
        db_table = 'dialog_vars'
        ordering = ('-pk',)
        verbose_name = _(u"SIP dialog vars")
        verbose_name_plural = _(u"SIP dialog vars")
        indexes = [
            models.Index(fields=['hash_entry', 'hash_id']),
        ]

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_dialogvar_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_dialogvar_update', args=(self.pk,))


class Acc(models.Model):

    # Fields
    method = models.CharField(max_length=16, default='', help_text=_(u"A method is the primary function that a request is meant to invoke on a server."))
    from_tag = models.CharField(max_length=64, default='', help_text=_(u"The tag parameter serves as a general mechanism to identify a dialog, which is the combination of the Call-ID along with two tags, one from participant in the dialog."))
    to_tag = models.CharField(max_length=64, default='', help_text=_(u"The tag parameter serves as a general mechanism to identify a dialog, which is the combination of the Call-ID along with two tags, one from participant in the dialog."))
    callid = models.CharField(max_length=255, default='', db_index=True, help_text=_(u"Call-ID header field uniquely identifies a particular invitation or all registrations of a particular client."))
    sip_code = models.CharField(max_length=3, default='', help_text=_(u"SIP reply code."))
    sip_reason = models.CharField(max_length=128, default='', help_text=_(u"SIP reply reason"))
    time = models.DateTimeField(help_text=_(u"Date and time when this record was written."))
    time_attr = models.IntegerField(help_text=_(u"Unix timestamp"))
    time_exten = models.IntegerField(help_text=_(u"extended value related to the time of event"))
    from_user = models.CharField(max_length=128, default='', help_text=_(u"FROM user field"))
    from_domain = models.CharField(max_length=128, default='', help_text=_(u"FROM domain field"))
    src_ip = models.CharField(max_length=128, default='', help_text=_(u"source IP"))
    ruri_user = models.CharField(max_length=128, default='', help_text=_(u"RURI user field"))
    ruri_domain = models.CharField(max_length=128, default='', help_text=_(u"RURI domain field"))
    cseq = models.CharField(max_length=128, default='', help_text=_(u"cseq field"))
    orig_customer = models.IntegerField(null=True, blank=True)
    term_customer = models.IntegerField(null=True, blank=True)
    orig_provider = models.IntegerField(null=True, blank=True)
    term_provider = models.IntegerField(null=True, blank=True)
    call_direction = models.CharField(max_length=128, default='', help_text=_(u"inbound / outbound"))
    called_did = models.CharField(max_length=128, default='')
    e164_caller = models.CharField(max_length=128, default='')
    e164_called = models.CharField(max_length=128, default='')
    called_did = models.CharField(max_length=128, default='')
    caller_destination = models.IntegerField(null=True, blank=True)
    called_destination = models.IntegerField(null=True, blank=True)
    did_destination = models.IntegerField(null=True, blank=True)
    leg_a_class = models.CharField(max_length=128, default='', help_text=_(u"on-net / off-net"))
    leg_b_class = models.CharField(max_length=128, default='', help_text=_(u"on-net / off-net"))
    o_c_rate_id = models.IntegerField(null=True, blank=True)
    o_c_rate_type = models.IntegerField(null=True, blank=True)
    t_c_rate_id = models.IntegerField(null=True, blank=True)
    t_c_rate_type = models.IntegerField(null=True, blank=True)
    o_p_rate_id = models.IntegerField(null=True, blank=True)
    o_p_rate_type = models.IntegerField(null=True, blank=True)
    t_p_rate_id = models.IntegerField(null=True, blank=True)
    t_p_rate_type = models.IntegerField(null=True, blank=True)


    class Meta:
        db_table = 'acc'
        ordering = ('-time',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_acc_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_acc_update', args=(self.pk,))


class AccCdr(models.Model):

    # Fields
    start_time = models.DateTimeField(db_index=True, help_text=_(u"Start date and time"))
    answered_time = models.DateTimeField(_(u"answered time"), null=True)
    end_time = models.DateTimeField(help_text=_(u"End date and time"))
    duration = models.DecimalField(max_digits=10, decimal_places=3, default=0, help_text=_(u"Duration"))
    caller = models.CharField(max_length=128, default='')
    callee = models.CharField(max_length=128, default='')
    callid = models.CharField(_(u"a leg call-ID"), max_length=128, default='')
    direction = models.CharField(max_length=128, default='', help_text=_(u"inbound / outbound"))
    sip_code = models.CharField(_(u"hangup SIP code"), max_length=3, null=True, db_index=True)
    sip_reason = models.TextField(_(u"hangup SIP reason"), max_length=255, null=True)
    orig_customer = models.IntegerField(
        _(u'originator customer'),
        null=True,
        blank=True
    )
    term_customer = models.IntegerField(
        _(u'terminator customer'),
        null=True,
        blank=True
    )
    orig_provider = models.IntegerField(
        _(u'originator provider'),
        null=True,
        blank=True
    )
    term_provider = models.IntegerField(
        _(u'terminator provider'),
        null=True,
        blank=True
    )
    called_did = models.CharField(max_length=128, default='')
    e164_caller = models.CharField(max_length=128, default='')
    e164_called = models.CharField(max_length=128, default='')
    caller_destination = models.IntegerField(null=True, blank=True)
    called_destination = models.IntegerField(null=True, blank=True)
    did_destination = models.IntegerField(null=True, blank=True)
    leg_a_class = models.CharField(max_length=128, default='', help_text=_(u"on-net / off-net"))
    leg_b_class = models.CharField(max_length=128, default='', help_text=_(u"on-net / off-net"))
    o_c_rate_id = models.IntegerField(
        _(u'originator customer rate Id'),
        null=True,
        blank=True
    )
    o_c_rate_type = models.IntegerField(
        _(u'originator customer rate type'),
        null=True,
        blank=True
    )
    t_c_rate_id = models.IntegerField(
        _(u'terminator customer rate Id'),
        null=True,
        blank=True
    )
    t_c_rate_type = models.IntegerField(
        _(u'terminator customer rate type'),
        null=True,
        blank=True
    )
    o_p_rate_id = models.IntegerField(
        _(u'originator provider rate Id'),
        null=True,
        blank=True
    )
    o_p_rate_type = models.IntegerField(
        _(u'originator provider rate type'),
        null=True,
        blank=True
    )
    t_p_rate_id = models.IntegerField(
        _(u'terminator provider rate Id'),
        null=True,
        blank=True
    )
    t_p_rate_type = models.IntegerField(
        _(u'terminator provider rate type'),
        null=True,
        blank=True
    )
    sip_charge_info = models.CharField(
        _(u'charge info'),
        null=True,
        max_length=100,
        help_text=_(u"Contents of the P-Charge-Info header for billing purpose."))
    sip_user_agent = models.CharField(_(u'sip user agent'), null=True, max_length=100)
    sip_rtp_rxstat = models.CharField(_(u'sip rtp rx stat'), null=True, max_length=30)
    sip_rtp_txstat = models.CharField(_(u'sip rtp tx stat'), null=True, max_length=30)
    kamailio_server = models.IntegerField(_(u"SIP server"), default=1)
    media_server = models.IntegerField(
        _(u"Media server name"),
        null=True
    )
    processed = models.DateTimeField(_(u"time cdr was processed"), null=True)

    class Meta:
        db_table = 'acc_cdrs'
        ordering = ('-start_time',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_acccdr_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_acccdr_update', args=(self.pk,))


class MissedCall(models.Model):

    # Fields
    method = models.CharField(max_length=16, default='', help_text=_(u"A method is the primary function that a request is meant to invoke on a server."))
    from_tag = models.CharField(max_length=64, default='', help_text=_(u"The tag parameter serves as a general mechanism to identify a dialog, which is the combination of the Call-ID along with two tags, one from participant in the dialog."))
    to_tag = models.CharField(max_length=64, default='', help_text=_(u"The tag parameter serves as a general mechanism to identify a dialog, which is the combination of the Call-ID along with two tags, one from participant in the dialog."))
    callid = models.CharField(max_length=255, default='', db_index=True, help_text=_(u"Call-ID header field uniquely identifies a particular invitation or all registrations of a particular client."))
    sip_code = models.CharField(max_length=3, default='', help_text=_(u"SIP reply code."))
    sip_reason = models.CharField(max_length=128, default='', help_text=_(u"SIP reply reason"))
    time = models.DateTimeField(help_text=_(u"Date and time when this record was written."))
    time_attr = models.IntegerField(help_text=_(u"Unix timestamp"))
    time_exten = models.IntegerField(help_text=_(u"extended value related to the time of event"))
    from_user = models.CharField(max_length=128, default='', help_text=_(u"FROM user field"))
    from_domain = models.CharField(max_length=128, default='', help_text=_(u"FROM domain field"))
    src_ip = models.CharField(max_length=128, default='', help_text=_(u"source IP"))
    ruri_user = models.CharField(max_length=128, default='', help_text=_(u"RURI user field"))
    ruri_domain = models.CharField(max_length=128, default='', help_text=_(u"RURI domain field"))
    cseq = models.CharField(max_length=128, default='', help_text=_(u"cseq field"))
    orig_customer = models.IntegerField(null=True, blank=True)
    term_customer = models.IntegerField(null=True, blank=True)
    orig_provider = models.IntegerField(null=True, blank=True)
    term_provider = models.IntegerField(null=True, blank=True)
    call_direction = models.CharField(max_length=128, default='', help_text=_(u"inbound / outbound"))
    called_did = models.CharField(max_length=128, default='')
    e164_caller = models.CharField(max_length=128, default='')
    e164_called = models.CharField(max_length=128, default='')
    called_did = models.CharField(max_length=128, default='')
    caller_destination = models.IntegerField(null=True, blank=True)
    called_destination = models.IntegerField(null=True, blank=True)
    did_destination = models.IntegerField(null=True, blank=True)
    leg_a_class = models.CharField(max_length=128, default='', help_text=_(u"on-net / off-net"))
    leg_b_class = models.CharField(max_length=128, default='', help_text=_(u"on-net / off-net"))
    o_c_rate_id = models.IntegerField(null=True, blank=True)
    o_c_rate_type = models.IntegerField(null=True, blank=True)
    t_c_rate_id = models.IntegerField(null=True, blank=True)
    t_c_rate_type = models.IntegerField(null=True, blank=True)
    o_p_rate_id = models.IntegerField(null=True, blank=True)
    o_p_rate_type = models.IntegerField(null=True, blank=True)
    t_p_rate_id = models.IntegerField(null=True, blank=True)
    t_p_rate_type = models.IntegerField(null=True, blank=True)


    class Meta:
        db_table = 'missed_calls'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_missedcall_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_missedcall_update', args=(self.pk,))


class UacReg(models.Model):

    # Fields
    l_uuid = models.CharField(max_length=64, default="", db_index=True, help_text=_(u"Local unique id used to build and match contact addresses."))
    l_username = models.CharField(max_length=64, default="", help_text=_(u"Local username"))
    l_domain = models.CharField(max_length=64, default="", help_text=_(u"Local domain"))
    r_username = models.CharField(max_length=64, default="", help_text=_(u"Remote username"))
    r_domain = models.CharField(max_length=64, default="", help_text=_(u"Remote domain"))
    realm = models.CharField(max_length=64, default="", help_text=_(u"realm"))
    auth_username = models.CharField(max_length=64, default="", help_text=_(u"Auth username"))
    auth_password = models.CharField(max_length=64, default="", blank=True, help_text=_(u"Auth password"))
    auth_ha1 = models.CharField(max_length=128, default="", blank=True, help_text=_(u"""Hashed (HA1) auth password - to calculate : echo -n "username:realm:password" | md5sum"""))
    auth_proxy = models.CharField(max_length=255, default="", blank=True, help_text=_(u"Outbound proxy SIP address"))
    expires = models.IntegerField(default=360, help_text=_(u"Expiration time in seconds, 0 means disabled"))
    flags = models.IntegerField(default=0, help_text=_(u"Flags to control the behaviour"))
    # need to tweak that presentation https://www.kamailio.org/docs/modules/devel/modules/uac.html#uac.r.uac.reg_info
    reg_delay = models.IntegerField(default=0, help_text=_(u"initial registration delay"))
    socket = models.CharField(max_length=128, default="", blank=True, help_text=_(u"Used socket for sending out requests"))


    class Meta:
        db_table = 'uacreg'
        ordering = ('-pk',)

    def __str__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_uacreg_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_uacreg_update', args=(self.pk,))


class Trusted(models.Model):

    # Choices
    PROTO_CHOICES = (
        ('any', 'any'),
        ('udp', 'udp'),
        ('tcp', 'tcp'),
        ('tls', 'tls'),
        ('sctp', 'sctp'),
    )

    # Fields
    src_ip = models.CharField(max_length=50, db_index=True, default="", help_text=_(u"Source address is equal to source address of request"))
    proto = models.CharField(max_length=4, choices=PROTO_CHOICES, default="any", help_text=_(u"Transport protocol is either any or equal to transport protocol of request"))
    from_pattern = models.CharField(max_length=64, null=True, blank=True, help_text=_(u"Regular expression matches From URI of request."))
    ruri_pattern = models.CharField(max_length=64, null=True, blank=True, help_text=_(u"Regular expression matches Request URI of request."))
    tag = models.CharField(max_length=64, default="", help_text=_(u"Tag"))
    priority = models.IntegerField(default=0, help_text=_(u"Priority of rule"))


    class Meta:
        db_table = 'trusted'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_trusted_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_trusted_update', args=(self.pk,))


class Version(models.Model):

    # Fields
    table_name = models.CharField(max_length=32, unique=True)
    table_version = models.IntegerField(default=0)


    class Meta:
        db_table = 'version'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_version_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_version_update', args=(self.pk,))


class Location(models.Model):

    # Fields
    ruid = models.CharField(max_length=64, default='', unique=True, help_text=_(u"Record internal unique id"))
    username = models.CharField(max_length=64, default='', help_text=_(u"Username / phone number"))
    domain = models.CharField(max_length=64, null=True, blank=True, help_text=_(u"Doamin name"))
    contact = models.CharField(max_length=512, default='', help_text=_(u"Contact header field value provides a URI whoses meaning depends on the type of request or response it is in."))
    received = models.CharField(max_length=128, null=True, blank=True, help_text=_(u"Received IP:PORT in the format SIP:IP:PORT"))
    path = models.CharField(max_length=512, null=True, blank=True, help_text=_(u"Path Header(s) per RFC 3327"))
    expires = models.DateTimeField(db_index=True, help_text=_(u"Date and time when this entry expires."))
    q = models.DecimalField(max_digits=10, decimal_places=2, default=1.0, help_text=_(u"Value used for preferential routing."))
    callid = models.CharField(max_length=255, default='Default-Call-ID', help_text=_(u"	 Call-ID header field uniquely identifies a particular invitation or all registrations of a particular client."))
    cseq = models.IntegerField(default=1, help_text=_(u"CSeq header field contains a single decimal sequence number and the request method."))
    last_modified = models.DateTimeField(help_text=_(u"Date and time when this entry was last modified"))
    flags = models.IntegerField(default=0, help_text=_(u"Internal flags"))
    cflags = models.IntegerField(default=0, help_text=_(u"Branch and contact flags"))
    user_agent = models.CharField(max_length=255, default='', help_text=_(u"User-Agent header field contains information about the UAC originating the request."))
    socket = models.CharField(max_length=64, null=True, blank=True, help_text=_(u"Socket used to connect to Kamailio. For example: UDP:IP:PORT"))
    methods = models.IntegerField(null=True, blank=True, help_text=_(u"Flags that indicate the SIP Methods this contact will accept."))
    instance = models.CharField(max_length=255, null=True, blank=True, help_text=_(u"The value of SIP instance parameter for GRUU."))
    reg_id = models.IntegerField(default=0, help_text=_(u"The value of reg-id contact parameter"))
    server_id = models.IntegerField(default=0, help_text=_(u"The value of server_id from configuration file"))
    connection_id = models.IntegerField(default=0, help_text=_(u"The value of connection id for location record"))
    keepalive = models.IntegerField(default=0, help_text=_(u"The value to control sending keep alive requests"))
    partition = models.IntegerField(default=0, help_text=_(u"The value to of the partition for keep alive requests"))


    class Meta:
        db_table = 'location'
        ordering = ('-pk',)
        verbose_name = _(u"user location")
        indexes = [
            models.Index(fields=['username', 'domain', 'contact']),
            models.Index(fields=['server_id', 'connection_id']),
        ]

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_location_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_location_update', args=(self.pk,))


class LocationAttrs(models.Model):

    # Fields
    ruid = models.CharField(max_length=64, default='', help_text=_(u"Record internal unique id"))
    username = models.CharField(max_length=64, default='', help_text=_(u"Username / phone number"))
    domain = models.CharField(max_length=64, null=True, blank=True, help_text=_(u"Domain name"))
    aname = models.CharField(max_length=64, default='', help_text=_(u"Attribute name"))
    atype = models.IntegerField(default=0, help_text=_(u"Attribute type"))
    avalue = models.CharField(max_length=512, default='', help_text=_(u"Attribute value"))
    last_modified = models.DateTimeField(db_index=True, help_text=_(u"Date and time when this entry was last modified"))


    class Meta:
        db_table = 'location_attrs'
        ordering = ('-pk',)
        indexes = [
            models.Index(fields=['username', 'domain', 'ruid']),
        ]

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_locationattrs_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_locationattrs_update', args=(self.pk,))


class UserBlackList(models.Model):
    # Choices
    WHITELIST_CHOICES = (
        ('0', 'blacklist'),
        ('1', 'whitelist'),
    )
    # Fields
    username = models.CharField(max_length=64, default='', help_text=_(u"The user that is used for the blacklist lookup"))
    domain = models.CharField(max_length=64, default='', help_text=_(u"The domain that is used for the blacklist lookup"))
    prefix = models.CharField(max_length=64, default='', help_text=_(u"The prefix that is matched for the blacklist"))
    whitelist = models.CharField(
        max_length=1,
        choices=WHITELIST_CHOICES,
        default='0',
        help_text=_(u"Specify if this a blacklist (0) or a whitelist (1) entry")
    )


    class Meta:
        db_table = 'userblacklist'
        ordering = ('-pk',)
        indexes = [
            models.Index(fields=['username', 'domain', 'prefix']),
        ]

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_userblacklist_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_userblacklist_update', args=(self.pk,))


class GlobalBlackList(models.Model):
    # Choices
    WHITELIST_CHOICES = (
        ('0', 'blacklist'),
        ('1', 'whitelist'),
    )
    # Fields
    prefix = models.CharField(max_length=64, default='', db_index=True, help_text=_(u"The prefix that is matched for the blacklist"))
    whitelist = models.CharField(
        max_length=1,
        choices=WHITELIST_CHOICES,
        default='0',
        help_text=_(u"Specify if this a blacklist (0) or a whitelist (1) entry")
    )
    description = models.TextField(max_length=255, default='', help_text=_(u"A comment for the entry"))


    class Meta:
        db_table = 'globalblacklist'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_globalblacklist_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_globalblacklist_update', args=(self.pk,))


class SpeedDial(models.Model):

    # Fields
    username = models.CharField(max_length=64, default='', help_text=_(u"Username / phone number"))
    domain = models.CharField(max_length=64, default='', help_text=_(u"Domain name"))
    sd_username = models.CharField(max_length=64, default='', help_text=_(u"Speed dial username"))
    sd_domain = models.CharField(max_length=64, default='', help_text=_(u"Speed dial domain"))
    new_uri = models.CharField(max_length=128, default='', help_text=_(u"New URI"))
    fname = models.CharField(max_length=64, default='', help_text=_(u"First name"))
    lname = models.CharField(max_length=64, default='', help_text=_(u"Last name"))
    description = models.CharField(max_length=64, default='', help_text=_(u"Description"))


    class Meta:
        db_table = 'speed_dial'
        ordering = ('-pk',)
        unique_together = [
            ["username", "domain", "sd_domain", "sd_username"],
        ]

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_speeddial_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_speeddial_update', args=(self.pk,))


class PipeLimit(models.Model):
    # choices
    ALGO_CHOICES = (
        ('NOP', 'NOP'),
        ('RED', 'RED'),
        ('TAILDROP', 'TAILDROP'),
        ('FEEDBACK', 'FEEDBACK'),
        ('NETWORK', 'NETWORK'),
    )
    # Fields
    pipeid = models.CharField(max_length=64, default='', help_text=_(u"Unique ID for pipe"))
    algorithm = models.CharField(
        max_length=32,
        choices=ALGO_CHOICES,
        default='TAILDROP',
        help_text=_(u"Algorithm to be used for pipe limits. See the readme of the module for description of available options: NOP, RED, TAILDROP, FEEDBACK, NETWORK"))
    plimit = models.IntegerField(default=0, help_text=_(u"Pipe limit (hits per second)"))


    class Meta:
        db_table = 'pl_pipes'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_pipelimit_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_pipelimit_update', args=(self.pk,))


class Mtree(models.Model):

    # Fields
    tprefix = models.CharField(max_length=32, default='', unique=True, help_text=_(u"Key to be used to index the values in the tree, usually a DID or prefix"))
    tvalue = models.CharField(max_length=128, default='', help_text=_(u"The value of the key"))


    class Meta:
        db_table = 'mtree'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_mtree_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_mtree_update', args=(self.pk,))


class Mtrees(models.Model):

    # Fields
    tname = models.CharField(max_length=128, default='', help_text=_(u"Name of shared memory tree"))
    tprefix = models.CharField(max_length=32, default='', help_text=_(u"Key to be used to index the values in the tree, usually a DID or prefix"))
    tvalue = models.CharField(max_length=128, default='', help_text=_(u"The value of the key"))


    class Meta:
        db_table = 'mtrees'
        ordering = ('-pk',)
        unique_together = [
            ["tname", "tprefix", "tvalue"],
        ]

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_mtrees_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_mtrees_update', args=(self.pk,))


class Htable(models.Model):

    # Fields
    key_name = models.CharField(max_length=64, default='', help_text=_(u"Name of the hash key"))
    key_type = models.IntegerField(default=0, help_text=_(u"Type of the key"))
    value_type = models.IntegerField(default=0, help_text=_(u"Type of the value"))
    key_value = models.CharField(max_length=128, default='', help_text=_(u"The value of the key"))
    expires = models.IntegerField(default=0, help_text=_(u"The epoch at which the key expires"))


    class Meta:
        db_table = 'htable'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_htable_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_htable_update', args=(self.pk,))


class RtpEngine(models.Model):
    # choices
    RTPE_CHOICES = (
        (0, _(u'disabled')),
        (1, _(u'enabled')),
    )
    # Fields
    setid = models.IntegerField(default="0", help_text=_(u"RTPEngine instance socket ID"))
    url = models.CharField(max_length=64, help_text=_(u"RTPEngine instance socket URL. Example : udp:rtpengine1.domain:8800"))
    weight = models.IntegerField(default=1, help_text=_(u"RTPEngine instance weight on startup"))
    disabled = models.IntegerField(default=0, choices=RTPE_CHOICES, help_text=_(u"RTPEngine instance state on startup"))
    stamp = models.DateTimeField(auto_now_add=True, help_text=_(u"RTPEngine instance add timestamp"))


    class Meta:
        db_table = 'rtpengine'
        ordering = ('-pk',)
        unique_together = [
            ["setid", "url"],
        ]

    def __str__(self):
        return u'%s - %s' % (self.setid, self.url)

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_rtpengine_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_rtpengine_update', args=(self.pk,))


class Statistic(models.Model):

    # Fields
    kamailio_id = models.PositiveSmallIntegerField()
    time_stamp = models.IntegerField(default=0)
    random = models.IntegerField(default=0)
    shm_used_size = models.IntegerField(default=0)
    shm_real_used_size = models.IntegerField(default=0)
    shm_max_used_size = models.IntegerField(default=0)
    shm_free_used_size = models.IntegerField(default=0)
    ul_users = models.IntegerField(default=0)
    ul_contacts = models.IntegerField(default=0)


    class Meta:
        db_table = 'statistics'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_statistic_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb_kamailio_statistic_update', args=(self.pk,))


class ToposD(models.Model):

    # Fields
    rectime = models.DateTimeField(db_index=True)
    s_method = models.CharField(max_length=64, default='')
    s_cseq = models.CharField(max_length=64, default='')
    a_callid = models.CharField(max_length=255, default='', db_index=True)
    a_uuid = models.CharField(max_length=255, default='', db_index=True)
    b_uuid = models.CharField(max_length=255, default='', db_index=True)
    a_contact = models.CharField(max_length=128, default='')
    b_contact = models.CharField(max_length=128, default='')
    as_contact = models.CharField(max_length=128, default='')
    bs_contact = models.CharField(max_length=128, default='')
    a_tag = models.CharField(max_length=255, default='')
    b_tag = models.CharField(max_length=255, default='')
    a_rr = models.TextField(null=True, blank=True)
    b_rr = models.TextField(null=True, blank=True)
    s_rr = models.TextField(null=True, blank=True)
    iflags = models.IntegerField(default=0)
    a_uri = models.CharField(max_length=128, default='')
    b_uri = models.CharField(max_length=128, default='')
    r_uri = models.CharField(max_length=128, default='')
    a_srcaddr = models.CharField(max_length=128, default='')
    b_srcaddr = models.CharField(max_length=128, default='')
    a_socket = models.CharField(max_length=128, default='')
    b_socket = models.CharField(max_length=128, default='')


    class Meta:
        db_table = 'topos_d'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb-kamailio_topos_d_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb-kamailio_topos_d_update', args=(self.pk,))


class ToposT(models.Model):

    # Fields
    rectime = models.DateTimeField(db_index=True)
    s_method = models.CharField(max_length=64, default='')
    s_cseq = models.CharField(max_length=64, default='')
    a_callid = models.CharField(max_length=255, default='', db_index=True)
    a_uuid = models.CharField(max_length=255, default='', db_index=True)
    b_uuid = models.CharField(max_length=255, default='')
    direction = models.IntegerField(default=0)
    x_via = models.TextField(null=True, blank=True)
    x_vbranch = models.CharField(max_length=255, default='', db_index=True)
    x_rr = models.TextField(null=True, blank=True)
    y_rr = models.TextField(null=True, blank=True)
    s_rr = models.TextField(null=True, blank=True)
    x_uri = models.CharField(max_length=128, default='')
    a_contact = models.CharField(max_length=128, default='')
    b_contact = models.CharField(max_length=128, default='')
    as_contact = models.CharField(max_length=128, default='')
    bs_contact = models.CharField(max_length=128, default='')
    x_tag = models.CharField(max_length=255, default='')
    a_tag = models.CharField(max_length=255, default='')
    b_tag = models.CharField(max_length=255, default='')
    a_srcaddr = models.CharField(max_length=128, default='')
    b_srcaddr = models.CharField(max_length=128, default='')
    a_socket = models.CharField(max_length=128, default='')
    b_socket = models.CharField(max_length=128, default='')


    class Meta:
        db_table = 'topos_t'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb-kamailio_topos_d_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb-kamailio_topos_d_update', args=(self.pk,))


class Domain(models.Model):

    # Fields
    domain = models.CharField(
        _(u"domain name"),
        max_length=64,
        unique=True,
        help_text=_(u"Domain name - exemple : pyfb-demo.org"))
    did = models.CharField(
        _(u"domain id"),
        max_length=64,
        null=True,
        blank=True,
        help_text=_(u"Domain id. Value of did column may be NULL, which means that it has the same value as domain column"))
    last_modified = models.DateTimeField(
        _(u"last modified"),
        auto_now=True,
        help_text=_(u"Date and time when this record was last modified."))

    class Meta:
        db_table = 'domain'
        ordering = ('-pk',)

    def __str__(self):
        return u'%s' % self.domain

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb-kamailio_domain_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb-kamailio_domain_update', args=(self.pk,))


# class DomainAttrs(models.Model):
#
#     # Fields
#     did = models.CharField(
#         _(u"domain id"),
#         max_length=64,
#         # To-Do : Add a fk to domain => view
#         help_text=_(u"Domain id."))
#     name = models.CharField(
#         _(u"domain name"),
#         max_length=32,
#         help_text=_(u"Name of attribute"))
#     type = models.IntegerField(
#         _(u"Type of attribut"),
#         # To-Do : Add a choices list
#         help_text=_(u"Type of attribute (0=integer, 2=string)"))
#     value = models.CharField(
#         _(u"domain name"),
#         max_length=255,
#         help_text=_(u"Domain name - exemple : pyfb-demo.org"))
#     last_modified = models.DateTimeField(
#         _(u"last modified"),
#         help_text=_(u"Date and time when this record was last modified."))
#
#     class Meta:
#         db_table = 'domain_attrs'
#         ordering = ('-pk',)
#         indexes = ['did', 'name']
#
#     def __unicode__(self):
#         return u'%s' % self.pk
#
#     def get_absolute_url(self):
#         return reverse('pyfb-kamailio:pyfb-kamailio_domain_attrs_detail', args=(self.pk,))
#
#     def get_update_url(self):
#         return reverse('pyfb-kamailio:pyfb-kamailio_domain_attrs_update', args=(self.pk,))


class DomainPolicy(models.Model):

    # Fields
    rule = models.CharField(
        _(u"domain rule"),
        max_length=255,
        db_index=True,
        help_text=_(u"Domain policy rule name which is equal to the URI as published in the domain policy NAPTRs."))
    type = models.CharField(
        _(u"domain policy rule type"),
        max_length=10,
        default="type",
        # To-Do : Add a choices list
        help_text=_(u"In the case of federation names, this is 'fed'. For standard referrals according to draft-lendl-speermint-technical-policy-00, this is 'std'. For direct domain lookups, this is 'dom'. Default value is 'type' !"))
    att = models.CharField(
        _(u"AVP name"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_(u"It contains the AVP's name. If the rule stored in this row triggers, than dp_can_connect() will add an AVP with that name."))
    val = models.CharField(
        _(u"value"),
        max_length=128,
        default="val",
        help_text=_(u"It contains the values for AVPs created by dp_can_connect(). Default value is 'val'"))
    description = models.TextField(
        _(u"description"),
        max_length=255,
        default="",
        help_text=_(u"Comment about the rule"))

    class Meta:
        db_table = 'domainpolicy'
        ordering = ('-pk',)
        unique_together = ['rule', 'att', 'val']

    def __unicode__(self):
        return u'%s' % self.rule

    def get_absolute_url(self):
        return reverse('pyfb-kamailio:pyfb-kamailio_domain_policy_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-kamailio:pyfb-kamailio_domain_policy_update', args=(self.pk,))
