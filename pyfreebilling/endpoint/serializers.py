from . import models

from rest_framework import serializers


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


