from django.db import models
from django.utils import timezone


class AnalyticsEvent(models.Model):
    """Track user interactions and system events"""
    EVENT_TYPES = [
        ('document_upload', 'Document Upload'),
        ('scam_report', 'Scam Report'),
        ('page_view', 'Page View'),
        ('admin_login', 'Admin Login'),
        ('export_data', 'Data Export'),
    ]
    
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['event_type', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.event_type} at {self.timestamp}"


class SystemMetrics(models.Model):
    """Store system performance and usage metrics"""
    timestamp = models.DateTimeField(default=timezone.now)
    total_documents = models.IntegerField(default=0)
    total_scam_reports = models.IntegerField(default=0)
    flagged_documents = models.IntegerField(default=0)
    high_risk_reports = models.IntegerField(default=0)
    avg_risk_score = models.FloatField(default=0.0)
    active_sessions = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return f"Metrics for {self.timestamp.date()}"