# -*- coding: utf-8 -*-
from . import models
from . import serializers
from rest_framework import viewsets, permissions


class DialogViewSet(viewsets.ModelViewSet):
    """ViewSet for the Dialog class"""

    queryset = models.Dialog.objects.all()
    serializer_class = serializers.DialogSerializer
    permission_classes = [permissions.IsAuthenticated]


class DialogVarViewSet(viewsets.ModelViewSet):
    """ViewSet for the DialogVar class"""

    queryset = models.DialogVar.objects.all()
    serializer_class = serializers.DialogVarSerializer
    permission_classes = [permissions.IsAuthenticated]


class AccViewSet(viewsets.ModelViewSet):
    """ViewSet for the Acc class"""

    queryset = models.Acc.objects.all()
    serializer_class = serializers.AccSerializer
    permission_classes = [permissions.IsAuthenticated]


class AccCdrViewSet(viewsets.ModelViewSet):
    """ViewSet for the AccCdr class"""

    queryset = models.AccCdr.objects.all()
    serializer_class = serializers.AccCdrSerializer
    permission_classes = [permissions.IsAuthenticated]


class MissedCallViewSet(viewsets.ModelViewSet):
    """ViewSet for the MissedCall class"""

    queryset = models.MissedCall.objects.all()
    serializer_class = serializers.MissedCallSerializer
    permission_classes = [permissions.IsAuthenticated]


class UacRegViewSet(viewsets.ModelViewSet):
    """ViewSet for the UacReg class"""

    queryset = models.UacReg.objects.all()
    serializer_class = serializers.UacRegSerializer
    permission_classes = [permissions.IsAuthenticated]


class TrustedViewSet(viewsets.ModelViewSet):
    """ViewSet for the Trusted class"""

    queryset = models.Trusted.objects.all()
    serializer_class = serializers.TrustedSerializer
    permission_classes = [permissions.IsAuthenticated]


class VersionViewSet(viewsets.ModelViewSet):
    """ViewSet for the Version class"""

    queryset = models.Version.objects.all()
    serializer_class = serializers.VersionSerializer
    permission_classes = [permissions.IsAuthenticated]


class LocationViewSet(viewsets.ModelViewSet):
    """ViewSet for the Location class"""

    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer
    permission_classes = [permissions.IsAuthenticated]


class LocationAttrsViewSet(viewsets.ModelViewSet):
    """ViewSet for the LocationAttrs class"""

    queryset = models.LocationAttrs.objects.all()
    serializer_class = serializers.LocationAttrsSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserBlackListViewSet(viewsets.ModelViewSet):
    """ViewSet for the UserBlackList class"""

    queryset = models.UserBlackList.objects.all()
    serializer_class = serializers.UserBlackListSerializer
    permission_classes = [permissions.IsAuthenticated]


class GlobalBlackListViewSet(viewsets.ModelViewSet):
    """ViewSet for the GlobalBlackList class"""

    queryset = models.GlobalBlackList.objects.all()
    serializer_class = serializers.GlobalBlackListSerializer
    permission_classes = [permissions.IsAuthenticated]


class SpeedDialViewSet(viewsets.ModelViewSet):
    """ViewSet for the SpeedDial class"""

    queryset = models.SpeedDial.objects.all()
    serializer_class = serializers.SpeedDialSerializer
    permission_classes = [permissions.IsAuthenticated]


class PipeLimitViewSet(viewsets.ModelViewSet):
    """ViewSet for the PipeLimit class"""

    queryset = models.PipeLimit.objects.all()
    serializer_class = serializers.PipeLimitSerializer
    permission_classes = [permissions.IsAuthenticated]


class MtreeViewSet(viewsets.ModelViewSet):
    """ViewSet for the Mtree class"""

    queryset = models.Mtree.objects.all()
    serializer_class = serializers.MtreeSerializer
    permission_classes = [permissions.IsAuthenticated]


class MtreesViewSet(viewsets.ModelViewSet):
    """ViewSet for the Mtrees class"""

    queryset = models.Mtrees.objects.all()
    serializer_class = serializers.MtreesSerializer
    permission_classes = [permissions.IsAuthenticated]


class HtableViewSet(viewsets.ModelViewSet):
    """ViewSet for the Htable class"""

    queryset = models.Htable.objects.all()
    serializer_class = serializers.HtableSerializer
    permission_classes = [permissions.IsAuthenticated]


class RtpEngineViewSet(viewsets.ModelViewSet):
    """ViewSet for the RtpEngine class"""

    queryset = models.RtpEngine.objects.all()
    serializer_class = serializers.RtpEngineSerializer
    permission_classes = [permissions.IsAuthenticated]


class StatisticViewSet(viewsets.ModelViewSet):
    """ViewSet for the Statistic class"""

    queryset = models.Statistic.objects.all()
    serializer_class = serializers.StatisticSerializer
    permission_classes = [permissions.IsAuthenticated]
