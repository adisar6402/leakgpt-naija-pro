from django.db import models
from django.utils import timezone


class DocumentReport(models.Model):
    """Enhanced document analysis reporting with Django"""
    filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10)
    file_size = models.IntegerField(default=0)
    upload_timestamp = models.DateTimeField(default=timezone.now)
    analysis_completed = models.BooleanField(default=False)
    risk_score = models.IntegerField(default=0)
    is_flagged = models.BooleanField(default=False)
    flagged_keywords = models.JSONField(default=list, blank=True)
    summary = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField()
    processing_time = models.FloatField(default=0.0)  # seconds
    
    class Meta:
        ordering = ['-upload_timestamp']
        indexes = [
            models.Index(fields=['is_flagged', 'upload_timestamp']),
            models.Index(fields=['risk_score']),
        ]
    
    def __str__(self):
        return f"{self.filename} - Risk: {self.risk_score}"


class ScamReportEnhanced(models.Model):
    """Enhanced scam reporting with Django features"""
    REPORT_TYPES = [
        ('message', 'Suspicious Message'),
        ('url', 'Suspicious URL'),
        ('phone', 'Suspicious Phone Number'),
    ]
    
    RISK_LEVELS = [
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
    ]
    
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    content = models.TextField()
    description = models.TextField(blank=True)
    risk_level = models.CharField(max_length=10, choices=RISK_LEVELS, default='low')
    flagged_patterns = models.JSONField(default=list, blank=True)
    submitted_timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField()
    is_verified = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True)
    follow_up_required = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-submitted_timestamp']
        indexes = [
            models.Index(fields=['report_type', 'risk_level']),
            models.Index(fields=['submitted_timestamp']),
        ]
    
    def __str__(self):
        return f"{self.report_type} - {self.risk_level} - {self.submitted_timestamp.date()}"


class TrendAnalysis(models.Model):
    """Track trends in fraud patterns and keywords"""
    analysis_date = models.DateField(default=timezone.now)
    keyword = models.CharField(max_length=100)
    frequency = models.IntegerField(default=0)
    trend_direction = models.CharField(max_length=10, choices=[
        ('up', 'Increasing'),
        ('down', 'Decreasing'),
        ('stable', 'Stable')
    ], default='stable')
    risk_correlation = models.FloatField(default=0.0)  # -1 to 1
    
    class Meta:
        unique_together = ['analysis_date', 'keyword']
        ordering = ['-analysis_date', '-frequency']
    
    def __str__(self):
        return f"{self.keyword} - {self.analysis_date}"