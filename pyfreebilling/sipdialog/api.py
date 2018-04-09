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


