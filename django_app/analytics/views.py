from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import AnalyticsEvent, SystemMetrics
from .serializers import AnalyticsEventSerializer, SystemMetricsSerializer


class AnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoints for analytics data"""
    queryset = AnalyticsEvent.objects.all()
    serializer_class = AnalyticsEventSerializer
    
    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        """Get dashboard statistics for admin panel"""
        # Get date range from query params
        days = int(request.query_params.get('days', 7))
        start_date = timezone.now() - timedelta(days=days)
        
        # Calculate basic stats
        events = AnalyticsEvent.objects.filter(timestamp__gte=start_date)
        
        stats = {
            'total_events': events.count(),
            'document_uploads': events.filter(event_type='document_upload').count(),
            'scam_reports': events.filter(event_type='scam_report').count(),
            'page_views': events.filter(event_type='page_view').count(),
            'admin_logins': events.filter(event_type='admin_login').count(),
            'date_range': {
                'start': start_date.isoformat(),
                'end': timezone.now().isoformat(),
                'days': days
            }
        }
        
        # Get hourly breakdown for charts
        hourly_stats = []
        for i in range(24):
            hour_start = timezone.now().replace(hour=i, minute=0, second=0, microsecond=0)
            hour_end = hour_start + timedelta(hours=1)
            
            hour_events = events.filter(
                timestamp__gte=hour_start,
                timestamp__lt=hour_end
            )
            
            hourly_stats.append({
                'hour': i,
                'events': hour_events.count(),
                'uploads': hour_events.filter(event_type='document_upload').count(),
                'reports': hour_events.filter(event_type='scam_report').count()
            })
        
        stats['hourly_breakdown'] = hourly_stats
        
        return Response(stats)
    
    @action(detail=False, methods=['post'])
    def track_event(self, request):
        """Track a new analytics event"""
        data = request.data.copy()
        data['ip_address'] = self.get_client_ip(request)
        data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')
        
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SystemMetricsViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoints for system metrics"""
    queryset = SystemMetrics.objects.all()
    serializer_class = SystemMetricsSerializer
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest system metrics"""
        latest_metrics = SystemMetrics.objects.first()
        if latest_metrics:
            serializer = self.get_serializer(latest_metrics)
            return Response(serializer.data)
        return Response({'message': 'No metrics available'}, status=status.HTTP_404_NOT_FOUND)