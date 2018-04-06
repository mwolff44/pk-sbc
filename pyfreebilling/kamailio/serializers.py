from . import models

from rest_framework import serializers


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
            'cfags', 
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


