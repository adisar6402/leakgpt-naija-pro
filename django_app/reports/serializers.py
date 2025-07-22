from rest_framework import serializers
from .models import DocumentReport, ScamReportEnhanced, TrendAnalysis


class DocumentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentReport
        fields = ['id', 'filename', 'file_type', 'file_size', 'upload_timestamp',
                 'analysis_completed', 'risk_score', 'is_flagged', 'flagged_keywords',
                 'summary', 'ip_address', 'processing_time']
        read_only_fields = ['id', 'upload_timestamp']


class ScamReportEnhancedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScamReportEnhanced
        fields = ['id', 'report_type', 'content', 'description', 'risk_level',
                 'flagged_patterns', 'submitted_timestamp', 'ip_address',
                 'is_verified', 'admin_notes', 'follow_up_required']
        read_only_fields = ['id', 'submitted_timestamp']


class TrendAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendAnalysis
        fields = ['id', 'analysis_date', 'keyword', 'frequency', 'trend_direction',
                 'risk_correlation']
        read_only_fields = ['id']