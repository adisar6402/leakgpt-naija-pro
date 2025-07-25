# Generated by Django 5.2.4 on 2025-07-22 21:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SystemMetrics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_documents', models.IntegerField(default=0)),
                ('total_scam_reports', models.IntegerField(default=0)),
                ('flagged_documents', models.IntegerField(default=0)),
                ('high_risk_reports', models.IntegerField(default=0)),
                ('avg_risk_score', models.FloatField(default=0.0)),
                ('active_sessions', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='AnalyticsEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(choices=[('document_upload', 'Document Upload'), ('scam_report', 'Scam Report'), ('page_view', 'Page View'), ('admin_login', 'Admin Login'), ('export_data', 'Data Export')], max_length=50)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('ip_address', models.GenericIPAddressField()),
                ('user_agent', models.TextField(blank=True, null=True)),
                ('metadata', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'ordering': ['-timestamp'],
                'indexes': [models.Index(fields=['event_type', 'timestamp'], name='analytics_a_event_t_64745b_idx'), models.Index(fields=['timestamp'], name='analytics_a_timesta_aef2a5_idx')],
            },
        ),
    ]
