"""
Hybrid Flask-Django Application
Integrates Django REST API with Flask frontend
"""

import os
import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.settings')
django.setup()

# Import Flask app
from app import app as flask_app
from django_app.wsgi import django_application

# Import Django views for integration
from django_app.analytics.views import AnalyticsViewSet
from django_app.reports.views import DocumentReportViewSet
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

# Add Django API routes to Flask
@flask_app.route('/api/analytics/dashboard', methods=['GET'])
def analytics_dashboard():
    """Integrate Django analytics with Flask"""
    try:
        from django_app.analytics.models import AnalyticsEvent
        from django.utils import timezone
        from datetime import timedelta
        
        # Get recent analytics data
        days = int(request.args.get('days', 7))
        start_date = timezone.now() - timedelta(days=days)
        events = AnalyticsEvent.objects.filter(timestamp__gte=start_date)
        
        stats = {
            'total_events': events.count(),
            'document_uploads': events.filter(event_type='document_upload').count(),
            'scam_reports': events.filter(event_type='scam_report').count(),
            'page_views': events.filter(event_type='page_view').count(),
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@flask_app.route('/api/reports/trends', methods=['GET'])
def report_trends():
    """Get trending keywords and patterns"""
    try:
        from django_app.reports.models import TrendAnalysis
        from django.utils import timezone
        from datetime import timedelta
        
        days = int(request.args.get('days', 30))
        start_date = timezone.now().date() - timedelta(days=days)
        
        trends = TrendAnalysis.objects.filter(
            analysis_date__gte=start_date
        ).order_by('-frequency')[:10]
        
        trend_data = []
        for trend in trends:
            trend_data.append({
                'keyword': trend.keyword,
                'frequency': trend.frequency,
                'trend_direction': trend.trend_direction,
                'risk_correlation': trend.risk_correlation
            })
        
        return jsonify(trend_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Enhanced Flask routes with Django integration
def track_analytics_event(event_type, metadata=None):
    """Track analytics events using Django models"""
    try:
        from django_app.analytics.models import AnalyticsEvent
        from utils import get_client_ip
        from flask import request
        
        AnalyticsEvent.objects.create(
            event_type=event_type,
            ip_address=get_client_ip(),
            user_agent=request.headers.get('User-Agent', ''),
            metadata=metadata or {}
        )
    except Exception as e:
        flask_app.logger.error(f"Failed to track analytics event: {e}")

def sync_document_to_django(analysis):
    """Sync Flask document analysis to Django models"""
    try:
        from django_app.reports.models import DocumentReport
        import json
        
        # Create Django model instance
        DocumentReport.objects.create(
            filename=analysis.filename,
            file_type=analysis.file_type,
            file_size=0,  # Would need to track this in Flask
            risk_score=analysis.risk_score,
            is_flagged=analysis.is_flagged,
            flagged_keywords=json.loads(analysis.flagged_keywords) if analysis.flagged_keywords else [],
            summary=analysis.summary,
            ip_address=analysis.ip_address,
            analysis_completed=True
        )
    except Exception as e:
        flask_app.logger.error(f"Failed to sync document to Django: {e}")

def sync_scam_report_to_django(scam_report):
    """Sync Flask scam report to Django models"""
    try:
        from django_app.reports.models import ScamReportEnhanced
        import json
        
        ScamReportEnhanced.objects.create(
            report_type=scam_report.report_type,
            content=scam_report.content,
            description=scam_report.description,
            risk_level=scam_report.risk_level,
            flagged_patterns=json.loads(scam_report.flagged_patterns) if scam_report.flagged_patterns else [],
            ip_address=scam_report.ip_address,
            is_verified=scam_report.is_verified
        )
    except Exception as e:
        flask_app.logger.error(f"Failed to sync scam report to Django: {e}")

# Export the hybrid application
app = flask_app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)