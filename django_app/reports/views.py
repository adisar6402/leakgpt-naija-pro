from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import DocumentReport, ScamReportEnhanced, TrendAnalysis
from .serializers import DocumentReportSerializer, ScamReportEnhancedSerializer, TrendAnalysisSerializer


class DocumentReportViewSet(viewsets.ModelViewSet):
    """API endpoints for document reports"""
    queryset = DocumentReport.objects.all()
    serializer_class = DocumentReportSerializer
    
    @action(detail=False, methods=['get'])
    def flagged_documents(self, request):
        """Get all flagged documents"""
        flagged = self.queryset.filter(is_flagged=True)
        serializer = self.get_serializer(flagged, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def high_risk(self, request):
        """Get high-risk documents (score > 70)"""
        high_risk = self.queryset.filter(risk_score__gte=70)
        serializer = self.get_serializer(high_risk, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get document analysis statistics"""
        total_docs = self.queryset.count()
        flagged_docs = self.queryset.filter(is_flagged=True).count()
        avg_risk = self.queryset.aggregate(
            avg_risk=models.Avg('risk_score')
        )['avg_risk'] or 0
        
        stats = {
            'total_documents': total_docs,
            'flagged_documents': flagged_docs,
            'flagged_percentage': (flagged_docs / total_docs * 100) if total_docs > 0 else 0,
            'average_risk_score': round(avg_risk, 2),
            'processing_efficiency': {
                'avg_processing_time': self.queryset.aggregate(
                    avg_time=models.Avg('processing_time')
                )['avg_time'] or 0
            }
        }
        
        return Response(stats)


class ScamReportEnhancedViewSet(viewsets.ModelViewSet):
    """API endpoints for enhanced scam reports"""
    queryset = ScamReportEnhanced.objects.all()
    serializer_class = ScamReportEnhancedSerializer
    
    @action(detail=False, methods=['get'])
    def by_risk_level(self, request):
        """Get reports grouped by risk level"""
        risk_level = request.query_params.get('level', 'high')
        reports = self.queryset.filter(risk_level=risk_level)
        serializer = self.get_serializer(reports, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def verification_queue(self, request):
        """Get reports requiring verification"""
        unverified = self.queryset.filter(
            is_verified=False,
            risk_level__in=['medium', 'high']
        )
        serializer = self.get_serializer(unverified, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Mark a report as verified"""
        report = self.get_object()
        report.is_verified = True
        report.admin_notes = request.data.get('admin_notes', '')
        report.save()
        
        serializer = self.get_serializer(report)
        return Response(serializer.data)


class TrendAnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoints for trend analysis"""
    queryset = TrendAnalysis.objects.all()
    serializer_class = TrendAnalysisSerializer
    
    @action(detail=False, methods=['get'])
    def top_keywords(self, request):
        """Get top trending keywords"""
        days = int(request.query_params.get('days', 7))
        start_date = timezone.now().date() - timedelta(days=days)
        
        trends = self.queryset.filter(
            analysis_date__gte=start_date
        ).order_by('-frequency')[:20]
        
        serializer = self.get_serializer(trends, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def risk_patterns(self, request):
        """Get keywords with high risk correlation"""
        high_risk_keywords = self.queryset.filter(
            risk_correlation__gte=0.7
        ).order_by('-risk_correlation')[:10]
        
        serializer = self.get_serializer(high_risk_keywords, many=True)
        return Response(serializer.data)