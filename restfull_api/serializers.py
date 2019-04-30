from rest_framework import serializers
from pbtform.models import (BarrierReport, InformationRequest, IssueReport, IssueExtraData, IssueStatus, BarrierAutoTest)

class IssueStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueStatus
        fields = ('__all__')

class BarrierAutoTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarrierAutoTest
        fields = ('__all__')

class IssueExtraDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueExtraData
        fields = ('__all__')

class BarrierReportSerializer(serializers.ModelSerializer):
    extra_data = IssueExtraDataSerializer()
    auto_test = BarrierAutoTestSerializer()
    class Meta:
        model = BarrierReport
        fields = ('__all__')

class InformationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationRequest
        fields = ('__all__')

class IssueReportSerializer(serializers.ModelSerializer):
    barrier_report = BarrierReportSerializer()
    information_request = InformationRequestSerializer()
    class Meta:
        model = IssueReport
        fields = ('__all__')
        depth = 1

class BarrierReportSerializerFull(serializers.ModelSerializer):
    extra_data = IssueExtraDataSerializer()
    status = IssueStatusSerializer()
    class Meta:
        model = BarrierReport
        fields = ('__all__')
        depth = 2

class InformationRequestSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = InformationRequest
        fields = ('__all__')
        depth = 2
