import unittest
from django.core.urlresolvers import reverse
from django.test import Client
from .models import Dialog, DialogVar
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType


def create_django_contrib_auth_models_user(**kwargs):
    defaults = {}
    defaults["username"] = "username"
    defaults["email"] = "username@tempurl.com"
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_django_contrib_auth_models_group(**kwargs):
    defaults = {}
    defaults["name"] = "group"
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_django_contrib_contenttypes_models_contenttype(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_dialog(**kwargs):
    defaults = {}
    defaults["hash_entry"] = "hash_entry"
    defaults["hash_id"] = "hash_id"
    defaults["callid"] = "callid"
    defaults["from_uri"] = "from_uri"
    defaults["from_tag"] = "from_tag"
    defaults["to_uri"] = "to_uri"
    defaults["to_tag"] = "to_tag"
    defaults["caller_cseq"] = "caller_cseq"
    defaults["callee_cseq"] = "callee_cseq"
    defaults["caller_route_set"] = "caller_route_set"
    defaults["callee_route_set"] = "callee_route_set"
    defaults["caller_contact"] = "caller_contact"
    defaults["callee_contact"] = "callee_contact"
    defaults["caller_sock"] = "caller_sock"
    defaults["callee_stock"] = "callee_stock"
    defaults["state"] = "state"
    defaults["start_time"] = "start_time"
    defaults["timeout"] = "timeout"
    defaults["sflags"] = "sflags"
    defaults["iflags"] = "iflags"
    defaults["toroute_name"] = "toroute_name"
    defaults["req_uri"] = "req_uri"
    defaults["xdata"] = "xdata"
    defaults.update(**kwargs)
    return Dialog.objects.create(**defaults)


def create_dialogvar(**kwargs):
    defaults = {}
    defaults["hash_entry"] = "hash_entry"
    defaults["hash_id"] = "hash_id"
    defaults["dialog_key"] = "dialog_key"
    defaults["dialog_value"] = "dialog_value"
    defaults.update(**kwargs)
    return DialogVar.objects.create(**defaults)


class DialogViewTest(unittest.TestCase):
    '''
    Tests for Dialog
    '''
    def setUp(self):
        self.client = Client()

    def test_list_dialog(self):
        url = reverse('sipdialog_dialog_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_dialog(self):
        url = reverse('sipdialog_dialog_create')
        data = {
            "hash_entry": "hash_entry",
            "hash_id": "hash_id",
            "callid": "callid",
            "from_uri": "from_uri",
            "from_tag": "from_tag",
            "to_uri": "to_uri",
            "to_tag": "to_tag",
            "caller_cseq": "caller_cseq",
            "callee_cseq": "callee_cseq",
            "caller_route_set": "caller_route_set",
            "callee_route_set": "callee_route_set",
            "caller_contact": "caller_contact",
            "callee_contact": "callee_contact",
            "caller_sock": "caller_sock",
            "callee_stock": "callee_stock",
            "state": "state",
            "start_time": "start_time",
            "timeout": "timeout",
            "sflags": "sflags",
            "iflags": "iflags",
            "toroute_name": "toroute_name",
            "req_uri": "req_uri",
            "xdata": "xdata",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_dialog(self):
        dialog = create_dialog()
        url = reverse('sipdialog_dialog_detail', args=[dialog.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_dialog(self):
        dialog = create_dialog()
        data = {
            "hash_entry": "hash_entry",
            "hash_id": "hash_id",
            "callid": "callid",
            "from_uri": "from_uri",
            "from_tag": "from_tag",
            "to_uri": "to_uri",
            "to_tag": "to_tag",
            "caller_cseq": "caller_cseq",
            "callee_cseq": "callee_cseq",
            "caller_route_set": "caller_route_set",
            "callee_route_set": "callee_route_set",
            "caller_contact": "caller_contact",
            "callee_contact": "callee_contact",
            "caller_sock": "caller_sock",
            "callee_stock": "callee_stock",
            "state": "state",
            "start_time": "start_time",
            "timeout": "timeout",
            "sflags": "sflags",
            "iflags": "iflags",
            "toroute_name": "toroute_name",
            "req_uri": "req_uri",
            "xdata": "xdata",
        }
        url = reverse('sipdialog_dialog_update', args=[dialog.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class DialogVarViewTest(unittest.TestCase):
    '''
    Tests for DialogVar
    '''
    def setUp(self):
        self.client = Client()

    def test_list_dialogvar(self):
        url = reverse('sipdialog_dialogvar_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_dialogvar(self):
        url = reverse('sipdialog_dialogvar_create')
        data = {
            "hash_entry": "hash_entry",
            "hash_id": "hash_id",
            "dialog_key": "dialog_key",
            "dialog_value": "dialog_value",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_dialogvar(self):
        dialogvar = create_dialogvar()
        url = reverse('sipdialog_dialogvar_detail', args=[dialogvar.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_dialogvar(self):
        dialogvar = create_dialogvar()
        data = {
            "hash_entry": "hash_entry",
            "hash_id": "hash_id",
            "dialog_key": "dialog_key",
            "dialog_value": "dialog_value",
        }
        url = reverse('sipdialog_dialogvar_update', args=[dialogvar.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


