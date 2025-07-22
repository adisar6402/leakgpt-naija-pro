from datetime import datetime
from app import db
from flask_login import UserMixin

class AdminUser(UserMixin, db.Model):
    """Admin user model for dashboard access"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DocumentAnalysis(db.Model):
    """Model for storing document analysis results"""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)  # 'txt' or 'pdf'
    original_text = db.Column(db.Text, nullable=False)
    flagged_keywords = db.Column(db.Text)  # JSON string of flagged keywords
    risk_score = db.Column(db.Integer, default=0)  # 0-100 risk score
    summary = db.Column(db.Text)
    is_flagged = db.Column(db.Boolean, default=False)
    analysis_date = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))  # For tracking while maintaining anonymity

    def __repr__(self):
        return f'<DocumentAnalysis {self.filename}>'

class ScamReport(db.Model):
    """Model for storing scam reports"""
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(20), nullable=False)  # 'message', 'url', 'phone'
    content = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    flagged_patterns = db.Column(db.Text)  # JSON string of detected patterns
    risk_level = db.Column(db.String(10), default='low')  # low, medium, high
    is_verified = db.Column(db.Boolean, default=False)
    reported_date = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))

    def __repr__(self):
        return f'<ScamReport {self.report_type}: {self.content[:50]}>'

class ContactMessage(db.Model):
    """Model for storing contact form messages"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<ContactMessage from {self.name}>'
