import unittest
from django.core.urlresolvers import reverse
from django.test import Client
from .models import Version, Location, LocationAttrs, UserBlackList, GlobalBlackList, SpeedDial, PipeLimit, Mtree, Mtrees, Htable
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


def create_version(**kwargs):
    defaults = {}
    defaults["table_name"] = "table_name"
    defaults["table_version"] = "table_version"
    defaults.update(**kwargs)
    return Version.objects.create(**defaults)


def create_location(**kwargs):
    defaults = {}
    defaults["ruid"] = "ruid"
    defaults["username"] = "username"
    defaults["domain"] = "domain"
    defaults["contact"] = "contact"
    defaults["received"] = "received"
    defaults["path"] = "path"
    defaults["expires"] = "expires"
    defaults["q"] = "q"
    defaults["callid"] = "callid"
    defaults["cseq"] = "cseq"
    defaults["last_modified"] = "last_modified"
    defaults["flags"] = "flags"
    defaults["cflags"] = "cflags"
    defaults["user_agent"] = "user_agent"
    defaults["socket"] = "socket"
    defaults["methods"] = "methods"
    defaults["instance"] = "instance"
    defaults["reg_id"] = "reg_id"
    defaults["server_id"] = "server_id"
    defaults["connection_id"] = "connection_id"
    defaults["keepalive"] = "keepalive"
    defaults["partition"] = "partition"
    defaults.update(**kwargs)
    return Location.objects.create(**defaults)


def create_locationattrs(**kwargs):
    defaults = {}
    defaults["ruid"] = "ruid"
    defaults["username"] = "username"
    defaults["domain"] = "domain"
    defaults["aname"] = "aname"
    defaults["atype"] = "atype"
    defaults["avalue"] = "avalue"
    defaults["last_modified"] = "last_modified"
    defaults.update(**kwargs)
    return LocationAttrs.objects.create(**defaults)


def create_userblacklist(**kwargs):
    defaults = {}
    defaults["username"] = "username"
    defaults["domain"] = "domain"
    defaults["prefix"] = "prefix"
    defaults["whitelist"] = "whitelist"
    defaults.update(**kwargs)
    return UserBlackList.objects.create(**defaults)


def create_globalblacklist(**kwargs):
    defaults = {}
    defaults["prefix"] = "prefix"
    defaults["whitelist"] = "whitelist"
    defaults["description"] = "description"
    defaults.update(**kwargs)
    return GlobalBlackList.objects.create(**defaults)


def create_speeddial(**kwargs):
    defaults = {}
    defaults["username"] = "username"
    defaults["domain"] = "domain"
    defaults["sd_username"] = "sd_username"
    defaults["sd_domain"] = "sd_domain"
    defaults["new_uri"] = "new_uri"
    defaults["fname"] = "fname"
    defaults["lname"] = "lname"
    defaults["description"] = "description"
    defaults.update(**kwargs)
    return SpeedDial.objects.create(**defaults)


def create_pipelimit(**kwargs):
    defaults = {}
    defaults["pipeid"] = "pipeid"
    defaults["algorithm"] = "algorithm"
    defaults["plimit"] = "plimit"
    defaults.update(**kwargs)
    return PipeLimit.objects.create(**defaults)


def create_mtree(**kwargs):
    defaults = {}
    defaults["tprefix"] = "tprefix"
    defaults["tvalue"] = "tvalue"
    defaults.update(**kwargs)
    return Mtree.objects.create(**defaults)


def create_mtrees(**kwargs):
    defaults = {}
    defaults["tname"] = "tname"
    defaults["tprefix"] = "tprefix"
    defaults["tvalue"] = "tvalue"
    defaults.update(**kwargs)
    return Mtrees.objects.create(**defaults)


def create_htable(**kwargs):
    defaults = {}
    defaults["key_name"] = "key_name"
    defaults["key_type"] = "key_type"
    defaults["value_type"] = "value_type"
    defaults["key_value"] = "key_value"
    defaults["expires"] = "expires"
    defaults.update(**kwargs)
    return Htable.objects.create(**defaults)


class VersionViewTest(unittest.TestCase):
    '''
    Tests for Version
    '''
    def setUp(self):
        self.client = Client()

    def test_list_version(self):
        url = reverse('kamailio_version_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_version(self):
        url = reverse('kamailio_version_create')
        data = {
            "table_name": "table_name",
            "table_version": "table_version",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_version(self):
        version = create_version()
        url = reverse('kamailio_version_detail', args=[version.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_version(self):
        version = create_version()
        data = {
            "table_name": "table_name",
            "table_version": "table_version",
        }
        url = reverse('kamailio_version_update', args=[version.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class LocationViewTest(unittest.TestCase):
    '''
    Tests for Location
    '''
    def setUp(self):
        self.client = Client()

    def test_list_location(self):
        url = reverse('kamailio_location_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_location(self):
        url = reverse('kamailio_location_create')
        data = {
            "ruid": "ruid",
            "username": "username",
            "domain": "domain",
            "contact": "contact",
            "received": "received",
            "path": "path",
            "expires": "expires",
            "q": "q",
            "callid": "callid",
            "cseq": "cseq",
            "last_modified": "last_modified",
            "flags": "flags",
            "cflags": "cflags",
            "user_agent": "user_agent",
            "socket": "socket",
            "methods": "methods",
            "instance": "instance",
            "reg_id": "reg_id",
            "server_id": "server_id",
            "connection_id": "connection_id",
            "keepalive": "keepalive",
            "partition": "partition",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_location(self):
        location = create_location()
        url = reverse('kamailio_location_detail', args=[location.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_location(self):
        location = create_location()
        data = {
            "ruid": "ruid",
            "username": "username",
            "domain": "domain",
            "contact": "contact",
            "received": "received",
            "path": "path",
            "expires": "expires",
            "q": "q",
            "callid": "callid",
            "cseq": "cseq",
            "last_modified": "last_modified",
            "flags": "flags",
            "cflags": "cflags",
            "user_agent": "user_agent",
            "socket": "socket",
            "methods": "methods",
            "instance": "instance",
            "reg_id": "reg_id",
            "server_id": "server_id",
            "connection_id": "connection_id",
            "keepalive": "keepalive",
            "partition": "partition",
        }
        url = reverse('kamailio_location_update', args=[location.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class LocationAttrsViewTest(unittest.TestCase):
    '''
    Tests for LocationAttrs
    '''
    def setUp(self):
        self.client = Client()

    def test_list_locationattrs(self):
        url = reverse('kamailio_locationattrs_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_locationattrs(self):
        url = reverse('kamailio_locationattrs_create')
        data = {
            "ruid": "ruid",
            "username": "username",
            "domain": "domain",
            "aname": "aname",
            "atype": "atype",
            "avalue": "avalue",
            "last_modified": "last_modified",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_locationattrs(self):
        locationattrs = create_locationattrs()
        url = reverse('kamailio_locationattrs_detail', args=[locationattrs.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_locationattrs(self):
        locationattrs = create_locationattrs()
        data = {
            "ruid": "ruid",
            "username": "username",
            "domain": "domain",
            "aname": "aname",
            "atype": "atype",
            "avalue": "avalue",
            "last_modified": "last_modified",
        }
        url = reverse('kamailio_locationattrs_update', args=[locationattrs.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class UserBlackListViewTest(unittest.TestCase):
    '''
    Tests for UserBlackList
    '''
    def setUp(self):
        self.client = Client()

    def test_list_userblacklist(self):
        url = reverse('kamailio_userblacklist_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_userblacklist(self):
        url = reverse('kamailio_userblacklist_create')
        data = {
            "username": "username",
            "domain": "domain",
            "prefix": "prefix",
            "whitelist": "whitelist",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_userblacklist(self):
        userblacklist = create_userblacklist()
        url = reverse('kamailio_userblacklist_detail', args=[userblacklist.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_userblacklist(self):
        userblacklist = create_userblacklist()
        data = {
            "username": "username",
            "domain": "domain",
            "prefix": "prefix",
            "whitelist": "whitelist",
        }
        url = reverse('kamailio_userblacklist_update', args=[userblacklist.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class GlobalBlackListViewTest(unittest.TestCase):
    '''
    Tests for GlobalBlackList
    '''
    def setUp(self):
        self.client = Client()

    def test_list_globalblacklist(self):
        url = reverse('kamailio_globalblacklist_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_globalblacklist(self):
        url = reverse('kamailio_globalblacklist_create')
        data = {
            "prefix": "prefix",
            "whitelist": "whitelist",
            "description": "description",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_globalblacklist(self):
        globalblacklist = create_globalblacklist()
        url = reverse('kamailio_globalblacklist_detail', args=[globalblacklist.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_globalblacklist(self):
        globalblacklist = create_globalblacklist()
        data = {
            "prefix": "prefix",
            "whitelist": "whitelist",
            "description": "description",
        }
        url = reverse('kamailio_globalblacklist_update', args=[globalblacklist.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class SpeedDialViewTest(unittest.TestCase):
    '''
    Tests for SpeedDial
    '''
    def setUp(self):
        self.client = Client()

    def test_list_speeddial(self):
        url = reverse('kamailio_speeddial_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_speeddial(self):
        url = reverse('kamailio_speeddial_create')
        data = {
            "username": "username",
            "domain": "domain",
            "sd_username": "sd_username",
            "sd_domain": "sd_domain",
            "new_uri": "new_uri",
            "fname": "fname",
            "lname": "lname",
            "description": "description",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_speeddial(self):
        speeddial = create_speeddial()
        url = reverse('kamailio_speeddial_detail', args=[speeddial.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_speeddial(self):
        speeddial = create_speeddial()
        data = {
            "username": "username",
            "domain": "domain",
            "sd_username": "sd_username",
            "sd_domain": "sd_domain",
            "new_uri": "new_uri",
            "fname": "fname",
            "lname": "lname",
            "description": "description",
        }
        url = reverse('kamailio_speeddial_update', args=[speeddial.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class PipeLimitViewTest(unittest.TestCase):
    '''
    Tests for PipeLimit
    '''
    def setUp(self):
        self.client = Client()

    def test_list_pipelimit(self):
        url = reverse('kamailio_pipelimit_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_pipelimit(self):
        url = reverse('kamailio_pipelimit_create')
        data = {
            "pipeid": "pipeid",
            "algorithm": "algorithm",
            "plimit": "plimit",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_pipelimit(self):
        pipelimit = create_pipelimit()
        url = reverse('kamailio_pipelimit_detail', args=[pipelimit.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_pipelimit(self):
        pipelimit = create_pipelimit()
        data = {
            "pipeid": "pipeid",
            "algorithm": "algorithm",
            "plimit": "plimit",
        }
        url = reverse('kamailio_pipelimit_update', args=[pipelimit.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class MtreeViewTest(unittest.TestCase):
    '''
    Tests for Mtree
    '''
    def setUp(self):
        self.client = Client()

    def test_list_mtree(self):
        url = reverse('kamailio_mtree_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_mtree(self):
        url = reverse('kamailio_mtree_create')
        data = {
            "tprefix": "tprefix",
            "tvalue": "tvalue",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_mtree(self):
        mtree = create_mtree()
        url = reverse('kamailio_mtree_detail', args=[mtree.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_mtree(self):
        mtree = create_mtree()
        data = {
            "tprefix": "tprefix",
            "tvalue": "tvalue",
        }
        url = reverse('kamailio_mtree_update', args=[mtree.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class MtreesViewTest(unittest.TestCase):
    '''
    Tests for Mtrees
    '''
    def setUp(self):
        self.client = Client()

    def test_list_mtrees(self):
        url = reverse('kamailio_mtrees_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_mtrees(self):
        url = reverse('kamailio_mtrees_create')
        data = {
            "tname": "tname",
            "tprefix": "tprefix",
            "tvalue": "tvalue",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_mtrees(self):
        mtrees = create_mtrees()
        url = reverse('kamailio_mtrees_detail', args=[mtrees.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_mtrees(self):
        mtrees = create_mtrees()
        data = {
            "tname": "tname",
            "tprefix": "tprefix",
            "tvalue": "tvalue",
        }
        url = reverse('kamailio_mtrees_update', args=[mtrees.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class HtableViewTest(unittest.TestCase):
    '''
    Tests for Htable
    '''
    def setUp(self):
        self.client = Client()

    def test_list_htable(self):
        url = reverse('kamailio_htable_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_htable(self):
        url = reverse('kamailio_htable_create')
        data = {
            "key_name": "key_name",
            "key_type": "key_type",
            "value_type": "value_type",
            "key_value": "key_value",
            "expires": "expires",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_htable(self):
        htable = create_htable()
        url = reverse('kamailio_htable_detail', args=[htable.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_htable(self):
        htable = create_htable()
        data = {
            "key_name": "key_name",
            "key_type": "key_type",
            "value_type": "value_type",
            "key_value": "key_value",
            "expires": "expires",
        }
        url = reverse('kamailio_htable_update', args=[htable.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
