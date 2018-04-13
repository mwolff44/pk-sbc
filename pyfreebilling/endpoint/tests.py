import unittest
from django.core.urlresolvers import reverse
from django.test import Client
from .models import UacReg, Trusted
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


def create_uacreg(**kwargs):
    defaults = {}
    defaults["l_uuid"] = "l_uuid"
    defaults["l_username"] = "l_username"
    defaults["l_domain"] = "l_domain"
    defaults["r_username"] = "r_username"
    defaults["r_domain"] = "r_domain"
    defaults["realm"] = "realm"
    defaults["auth_username"] = "auth_username"
    defaults["auth_password"] = "auth_password"
    defaults["auth_ha1"] = "auth_ha1"
    defaults["auth_proxy"] = "auth_proxy"
    defaults["expires"] = "expires"
    defaults["flags"] = "flags"
    defaults["reg_delay"] = "reg_delay"
    defaults.update(**kwargs)
    return UacReg.objects.create(**defaults)


def create_trusted(**kwargs):
    defaults = {}
    defaults["src_ip"] = "src_ip"
    defaults["proto"] = "proto"
    defaults["from_pattern"] = "from_pattern"
    defaults["ruri_pattern"] = "ruri_pattern"
    defaults["tag"] = "tag"
    defaults["priority"] = "priority"
    defaults.update(**kwargs)
    return Trusted.objects.create(**defaults)


class UacRegViewTest(unittest.TestCase):
    '''
    Tests for UacReg
    '''
    def setUp(self):
        self.client = Client()

    def test_list_uacreg(self):
        url = reverse('endpoint_uacreg_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_uacreg(self):
        url = reverse('endpoint_uacreg_create')
        data = {
            "l_uuid": "l_uuid",
            "l_username": "l_username",
            "l_domain": "l_domain",
            "r_username": "r_username",
            "r_domain": "r_domain",
            "realm": "realm",
            "auth_username": "auth_username",
            "auth_password": "auth_password",
            "auth_ha1": "auth_ha1",
            "auth_proxy": "auth_proxy",
            "expires": "expires",
            "flags": "flags",
            "reg_delay": "reg_delay",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_uacreg(self):
        uacreg = create_uacreg()
        url = reverse('endpoint_uacreg_detail', args=[uacreg.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_uacreg(self):
        uacreg = create_uacreg()
        data = {
            "l_uuid": "l_uuid",
            "l_username": "l_username",
            "l_domain": "l_domain",
            "r_username": "r_username",
            "r_domain": "r_domain",
            "realm": "realm",
            "auth_username": "auth_username",
            "auth_password": "auth_password",
            "auth_ha1": "auth_ha1",
            "auth_proxy": "auth_proxy",
            "expires": "expires",
            "flags": "flags",
            "reg_delay": "reg_delay",
        }
        url = reverse('endpoint_uacreg_update', args=[uacreg.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class TrustedViewTest(unittest.TestCase):
    '''
    Tests for Trusted
    '''
    def setUp(self):
        self.client = Client()

    def test_list_trusted(self):
        url = reverse('endpoint_trusted_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_trusted(self):
        url = reverse('endpoint_trusted_create')
        data = {
            "src_ip": "src_ip",
            "proto": "proto",
            "from_pattern": "from_pattern",
            "ruri_pattern": "ruri_pattern",
            "tag": "tag",
            "priority": "priority",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_trusted(self):
        trusted = create_trusted()
        url = reverse('endpoint_trusted_detail', args=[trusted.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_trusted(self):
        trusted = create_trusted()
        data = {
            "src_ip": "src_ip",
            "proto": "proto",
            "from_pattern": "from_pattern",
            "ruri_pattern": "ruri_pattern",
            "tag": "tag",
            "priority": "priority",
        }
        url = reverse('endpoint_trusted_update', args=[trusted.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


