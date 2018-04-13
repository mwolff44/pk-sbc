import unittest
from django.core.urlresolvers import reverse
from django.test import Client
from .models import Acc, AccCdr, MissedCall
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


def create_acc(**kwargs):
    defaults = {}
    defaults["method"] = "method"
    defaults["from_tag"] = "from_tag"
    defaults["to_tag"] = "to_tag"
    defaults["callid"] = "callid"
    defaults["sip_code"] = "sip_code"
    defaults["sip_reason"] = "sip_reason"
    defaults["time"] = "time"
    defaults["time_attr"] = "time_attr"
    defaults["time_exten"] = "time_exten"
    defaults.update(**kwargs)
    return Acc.objects.create(**defaults)


def create_acccdr(**kwargs):
    defaults = {}
    defaults["start_time"] = "start_time"
    defaults["end_time"] = "end_time"
    defaults["duration"] = "duration"
    defaults.update(**kwargs)
    return AccCdr.objects.create(**defaults)


def create_missedcall(**kwargs):
    defaults = {}
    defaults["method"] = "method"
    defaults["from_tag"] = "from_tag"
    defaults["to_tag"] = "to_tag"
    defaults["callid"] = "callid"
    defaults["sip_code"] = "sip_code"
    defaults["sip_reason"] = "sip_reason"
    defaults["time"] = "time"
    defaults.update(**kwargs)
    return MissedCall.objects.create(**defaults)


class AccViewTest(unittest.TestCase):
    '''
    Tests for Acc
    '''
    def setUp(self):
        self.client = Client()

    def test_list_acc(self):
        url = reverse('accounting_acc_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_acc(self):
        url = reverse('accounting_acc_create')
        data = {
            "method": "method",
            "from_tag": "from_tag",
            "to_tag": "to_tag",
            "callid": "callid",
            "sip_code": "sip_code",
            "sip_reason": "sip_reason",
            "time": "time",
            "time_attr": "time_attr",
            "time_exten": "time_exten",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_acc(self):
        acc = create_acc()
        url = reverse('accounting_acc_detail', args=[acc.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_acc(self):
        acc = create_acc()
        data = {
            "method": "method",
            "from_tag": "from_tag",
            "to_tag": "to_tag",
            "callid": "callid",
            "sip_code": "sip_code",
            "sip_reason": "sip_reason",
            "time": "time",
            "time_attr": "time_attr",
            "time_exten": "time_exten",
        }
        url = reverse('accounting_acc_update', args=[acc.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class AccCdrViewTest(unittest.TestCase):
    '''
    Tests for AccCdr
    '''
    def setUp(self):
        self.client = Client()

    def test_list_acccdr(self):
        url = reverse('accounting_acccdr_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_acccdr(self):
        url = reverse('accounting_acccdr_create')
        data = {
            "start_time": "start_time",
            "end_time": "end_time",
            "duration": "duration",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_acccdr(self):
        acccdr = create_acccdr()
        url = reverse('accounting_acccdr_detail', args=[acccdr.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_acccdr(self):
        acccdr = create_acccdr()
        data = {
            "start_time": "start_time",
            "end_time": "end_time",
            "duration": "duration",
        }
        url = reverse('accounting_acccdr_update', args=[acccdr.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class MissedCallViewTest(unittest.TestCase):
    '''
    Tests for MissedCall
    '''
    def setUp(self):
        self.client = Client()

    def test_list_missedcall(self):
        url = reverse('accounting_missedcall_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_missedcall(self):
        url = reverse('accounting_missedcall_create')
        data = {
            "method": "method",
            "from_tag": "from_tag",
            "to_tag": "to_tag",
            "callid": "callid",
            "sip_code": "sip_code",
            "sip_reason": "sip_reason",
            "time": "time",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_missedcall(self):
        missedcall = create_missedcall()
        url = reverse('accounting_missedcall_detail', args=[missedcall.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_missedcall(self):
        missedcall = create_missedcall()
        data = {
            "method": "method",
            "from_tag": "from_tag",
            "to_tag": "to_tag",
            "callid": "callid",
            "sip_code": "sip_code",
            "sip_reason": "sip_reason",
            "time": "time",
        }
        url = reverse('accounting_missedcall_update', args=[missedcall.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
