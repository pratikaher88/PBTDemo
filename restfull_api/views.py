# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from pbtform import models
from restfull_api import serializers
from rest_framework import permissions


class BarrierReport(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.BarrierReport.objects.all()
    serializer_class = serializers.BarrierReportSerializerFull
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class InformationRequest(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.InformationRequest.objects.all()
    serializer_class = serializers.InformationRequestSerializerFull
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class IssueReport(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.IssueReport.objects.all()
    serializer_class = serializers.IssueReportSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class BarrierStatus(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.IssueStatus.objects.all()
    serializer_class = serializers.IssueStatusSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
