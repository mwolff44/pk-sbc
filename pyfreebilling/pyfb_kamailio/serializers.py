# -*- coding: utf-8 -*-
from . import models

from rest_framework import serializers


class DialogSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Dialog
        fields = (
            'pk',
            'hash_entry',
            'hash_id',
            'callid',
            'from_uri',
            'from_tag',
            'to_uri',
            'to_tag',
            'caller_cseq',
            'callee_cseq',
            'caller_route_set',
            'callee_route_set',
            'caller_contact',
            'callee_contact',
            'caller_sock',
            'callee_sock',
            'state',
            'start_time',
            'timeout',
            'sflags',
            'iflags',
            'toroute_name',
            'req_uri',
            'xdata',
        )


class DialogVarSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DialogVar
        fields = (
            'pk',
            'hash_entry',
            'hash_id',
            'dialog_key',
            'dialog_value',
        )


class AccSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Acc
        fields = (
            'pk',
            'method',
            'from_tag',
            'to_tag',
            'callid',
            'sip_code',
            'sip_reason',
            'time',
            'time_attr',
            'time_exten',
        )


class AccCdrSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AccCdr
        fields = (
            'pk',
            'start_time',
            'end_time',
            'duration',
        )


class MissedCallSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MissedCall
        fields = (
            'pk',
            'method',
            'from_tag',
            'to_tag',
            'callid',
            'sip_code',
            'sip_reason',
            'time',
        )


class UacRegSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UacReg
        fields = (
            'pk',
            'l_uuid',
            'l_username',
            'l_domain',
            'r_username',
            'r_domain',
            'realm',
            'auth_username',
            'auth_password',
            'auth_ha1',
            'auth_proxy',
            'expires',
            'flags',
            'reg_delay',
            'socket',
        )


class TrustedSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Trusted
        fields = (
            'pk',
            'src_ip',
            'proto',
            'from_pattern',
            'ruri_pattern',
            'tag',
            'priority',
        )


class VersionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Version
        fields = (
            'pk',
            'table_name',
            'table_version',
        )


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Location
        fields = (
            'pk',
            'ruid',
            'username',
            'domain',
            'contact',
            'received',
            'path',
            'expires',
            'q',
            'callid',
            'cseq',
            'last_modified',
            'flags',
            'cflags',
            'user_agent',
            'socket',
            'methods',
            'instance',
            'reg_id',
            'server_id',
            'connection_id',
            'keepalive',
            'partition',
        )


class LocationAttrsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LocationAttrs
        fields = (
            'pk',
            'ruid',
            'username',
            'domain',
            'aname',
            'atype',
            'avalue',
            'last_modified',
        )


class UserBlackListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserBlackList
        fields = (
            'pk',
            'username',
            'domain',
            'prefix',
            'whitelist',
        )


class GlobalBlackListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GlobalBlackList
        fields = (
            'pk',
            'prefix',
            'whitelist',
            'description',
        )


class SpeedDialSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SpeedDial
        fields = (
            'pk',
            'username',
            'domain',
            'sd_username',
            'sd_domain',
            'new_uri',
            'fname',
            'lname',
            'description',
        )


class PipeLimitSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PipeLimit
        fields = (
            'pk',
            'pipeid',
            'algorithm',
            'plimit',
        )


class MtreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Mtree
        fields = (
            'pk',
            'tprefix',
            'tvalue',
        )


class MtreesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Mtrees
        fields = (
            'pk',
            'tname',
            'tprefix',
            'tvalue',
        )


class HtableSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Htable
        fields = (
            'pk',
            'key_name',
            'key_type',
            'value_type',
            'key_value',
            'expires',
        )


class RtpEngineSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RtpEngine
        fields = (
            'pk',
            'setid',
            'url',
            'weight',
            'disabled',
            'stamp',
        )


class StatisticSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Statistic
        fields = (
            'pk',
            'kamailio_id',
            'time_stamp',
            'random',
            'shm_used_size',
            'shm_real_used_size',
            'shm_max_used_size',
            'shm_free_used_size',
            'ul_users',
            'ul_contacts',
        )
