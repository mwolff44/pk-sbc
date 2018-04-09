from django.core.urlresolvers import reverse
from django_extensions.db.fields import AutoSlugField
from django.db.models import *
from django.db import models as models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django_extensions.db import fields as extension_fields


class Dialog(models.Model):

    # Fields
    hash_entry = IntegerField(help_text=_(u"Number of the hash entry in the dialog hash table"))
    hash_id = IntegerField(help_text=_(u"The ID on the hash entry"))
    callid = CharField(max_length=255, help_text=_(u"Call-ID of the dialog"))
    from_uri = CharField(max_length=128, help_text=_(u"The URI of the FROM header (as per INVITE)"))
    from_tag = CharField(max_length=64, help_text=_(u"The tag parameter serves as a general mechanism to identify a dialog, which is the combination of the Call-ID along with two tags, one from participant in the dialog."))
    to_uri = CharField(max_length=128, help_text=_(u"The URI of the TO header (as per INVITE)"))
    to_tag = CharField(max_length=64, help_text=_(u"The tag parameter serves as a general mechanism to identify a dialog, which is the combination of the Call-ID along with two tags, one from participant in the dialog."))
    caller_cseq = CharField(max_length=20, help_text=_(u"Last Cseq number on the caller side."))
    callee_cseq = CharField(max_length=20, help_text=_(u"Last Cseq number on the callee side."))
    caller_route_set = CharField(max_length=512, null=True, blank=True, help_text=_(u"Route set on the caller side."))
    callee_route_set = CharField(max_length=512, null=True, blank=True, help_text=_(u"Route set on the callee side."))
    caller_contact = CharField(max_length=128, help_text=_(u"Caller's contact uri."))
    callee_contact = CharField(max_length=128, help_text=_(u"Callee's contact uri."))
    caller_sock = CharField(max_length=64, help_text=_(u"Local socket used to communicate with caller"))
    callee_stock = CharField(max_length=64, help_text=_(u"Local socket used to communicate with callee"))
    state = IntegerField(help_text=_(u"The state of the dialog."))
    start_time = IntegerField(help_text=_(u"The timestamp (unix time) when the dialog was confirmed."))
    timeout = IntegerField(help_text=_(u"The timestamp (unix time) when the dialog will expire."))
    sflags = IntegerField(help_text=_(u"The flags to set for dialog and accesible from config file."))
    iflags = IntegerField(help_text=_(u"The internal flags for dialog."))
    toroute_name = CharField(max_length=32, null=True, blank=True, help_text=_(u"The name of route to be executed at dialog timeout."))
    req_uri = CharField(max_length=128, help_text=_(u"The URI of initial request in dialog"))
    xdata = CharField(max_length=512, blank=True, null=True, help_text=_(u"Extra data associated to the dialog (e.g., serialized profiles)."))


    class Meta:
        db_table = 'dialog'
        app_label = 'sipdialog'
        ordering = ('-pk',)
        verbose_name = _(u"SIP dialog")
        verbose_name_plural = _(u"SIP dialogs")
        indexes = [
            models.Index(fields=['hash_entry', 'hash_id']),
        ]

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('sipdialog_dialog_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('sipdialog_dialog_update', args=(self.pk,))


class DialogVar(models.Model):

    # Fields
    hash_entry = IntegerField(help_text=_(u"Number of the hash entry in the dialog hash table"))
    hash_id = IntegerField(help_text=_(u"The ID on the hash entry"))
    dialog_key = CharField(max_length=128, help_text=_(u"The key of the dialog variable"))
    dialog_value = CharField(max_length=512, help_text=_(u"The value of the dialog variable"))


    class Meta:
        db_table = 'dialog_vars'
        app_label = 'sipdialog'
        ordering = ('-pk',)
        verbose_name = _(u"SIP dialog vars")
        verbose_name_plural = _(u"SIP dialog vars")
        indexes = [
            models.Index(fields=['hash_entry', 'hash_id']),
        ]

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('sipdialog_dialogvar_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('sipdialog_dialogvar_update', args=(self.pk,))
