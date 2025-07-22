from rest_framework import serializers
from .models import AnalyticsEvent, SystemMetrics


class AnalyticsEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsEvent
        fields = ['id', 'event_type', 'timestamp', 'ip_address', 'user_agent', 'metadata']
        read_only_fields = ['id', 'timestamp']


class SystemMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemMetrics
        fields = ['id', 'timestamp', 'total_documents', 'total_scam_reports', 
                 'flagged_documents', 'high_risk_reports', 'avg_risk_score', 'active_sessions']
        read_only_fields = ['id', 'timestamp']