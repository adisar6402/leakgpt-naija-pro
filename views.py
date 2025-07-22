import os
import json
import csv
from datetime import datetime, timedelta
from flask import render_template, request, redirect, url_for, flash, jsonify, make_response, send_file, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from io import StringIO, BytesIO
import PyPDF2

from app import app, db
from models import DocumentAnalysis, ScamReport, ContactMessage, AdminUser
from ai_logic import analyze_document, analyze_scam_content
from utils import allowed_file, extract_text_from_pdf, get_client_ip

@app.route('/')
def index():
    """Home page"""
    # Get recent statistics for homepage
    total_documents = DocumentAnalysis.query.count()
    total_scam_reports = ScamReport.query.count()
    flagged_documents = DocumentAnalysis.query.filter_by(is_flagged=True).count()
    
    stats = {
        'total_documents': total_documents,
        'total_scam_reports': total_scam_reports,
        'flagged_documents': flagged_documents
    }
    
    return render_template('index.html', stats=stats)

@app.route('/upload')
def upload_page():
    """Document upload page"""
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle document upload and analysis"""
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename or "unknown")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Extract text based on file type
            if filename.lower().endswith('.pdf'):
                text_content = extract_text_from_pdf(filepath)
                file_type = 'pdf'
            else:
                with open(filepath, 'r', encoding='utf-8') as f:
                    text_content = f.read()
                file_type = 'txt'
            
            # Analyze the document
            analysis_result = analyze_document(text_content)
            
            # Save analysis to database
            analysis = DocumentAnalysis(
                filename=file.filename,
                file_type=file_type,
                original_text=text_content,
                flagged_keywords=json.dumps(analysis_result['flagged_keywords']),
                risk_score=analysis_result['risk_score'],
                summary=analysis_result['summary'],
                is_flagged=analysis_result['is_flagged'],
                ip_address=get_client_ip()
            )
            
            db.session.add(analysis)
            db.session.commit()
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return redirect(url_for('results', analysis_id=analysis.id))
            
        except Exception as e:
            app.logger.error(f"Error processing file: {str(e)}")
            flash('Error processing file. Please try again.', 'error')
            # Clean up file on error
            if os.path.exists(filepath):
                os.remove(filepath)
            return redirect(request.url)
    
    else:
        flash('Invalid file type. Please upload .txt or .pdf files only.', 'error')
        return redirect(request.url)

@app.route('/scam-report')
def scam_report_page():
    """Scam reporting page"""
    return render_template('scam_report.html')

@app.route('/scam-report', methods=['POST'])
def submit_scam_report():
    """Handle scam report submission"""
    report_type = request.form.get('report_type')
    content = request.form.get('content')
    description = request.form.get('description', '')
    
    if not report_type or not content:
        flash('Please fill in all required fields.', 'error')
        return redirect(request.url)
    
    try:
        # Analyze the scam content
        analysis_result = analyze_scam_content(content, report_type)
        
        # Save to database
        scam_report = ScamReport(
            report_type=report_type,
            content=content,
            description=description,
            flagged_patterns=json.dumps(analysis_result['patterns']),
            risk_level=analysis_result['risk_level'],
            ip_address=get_client_ip()
        )
        
        db.session.add(scam_report)
        db.session.commit()
        
        flash('Thank you for your report. It has been submitted for review.', 'success')
        return redirect(url_for('index'))
        
    except Exception as e:
        app.logger.error(f"Error processing scam report: {str(e)}")
        flash('Error submitting report. Please try again.', 'error')
        return redirect(request.url)

@app.route('/results/<int:analysis_id>')
def results(analysis_id):
    """Display analysis results"""
    analysis = DocumentAnalysis.query.get_or_404(analysis_id)
    
    # Parse flagged keywords from JSON
    flagged_keywords = json.loads(analysis.flagged_keywords) if analysis.flagged_keywords else []
    
    return render_template('results.html', analysis=analysis, flagged_keywords=flagged_keywords)

@app.route('/contact')
def contact_page():
    """Contact form page"""
    return render_template('contact.html')

@app.route('/contact', methods=['POST'])
def submit_contact():
    """Handle contact form submission"""
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')
    
    if not all([name, email, subject, message]):
        flash('Please fill in all fields.', 'error')
        return redirect(request.url)
    
    try:
        contact_msg = ContactMessage(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        db.session.add(contact_msg)
        db.session.commit()
        
        flash('Your message has been sent. We will get back to you soon.', 'success')
        return redirect(url_for('index'))
        
    except Exception as e:
        app.logger.error(f"Error saving contact message: {str(e)}")
        flash('Error sending message. Please try again.', 'error')
        return redirect(request.url)

# Admin routes
@app.route('/admin/login')
def admin_login():
    """Admin login page"""
    return render_template('admin/login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    """Handle admin login"""
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = AdminUser.query.filter_by(username=username).first()
    
    if user and password and check_password_hash(user.password_hash, password):
        login_user(user)
        return redirect(url_for('admin_dashboard'))
    
    flash('Invalid username or password.', 'error')
    return redirect(url_for('admin_login'))

@app.route('/admin/logout')
@login_required
def admin_logout():
    """Admin logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard"""
    # Get filter parameters
    date_filter = request.args.get('date_filter', '7')  # days
    report_type = request.args.get('type', 'all')
    keyword_filter = request.args.get('keyword', '')
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=int(date_filter))
    
    # Build queries
    doc_query = DocumentAnalysis.query.filter(DocumentAnalysis.analysis_date >= start_date)
    scam_query = ScamReport.query.filter(ScamReport.reported_date >= start_date)
    
    # Apply filters
    if keyword_filter:
        doc_query = doc_query.filter(DocumentAnalysis.flagged_keywords.contains(keyword_filter))
        scam_query = scam_query.filter(ScamReport.flagged_patterns.contains(keyword_filter))
    
    # Get data
    documents = doc_query.order_by(DocumentAnalysis.analysis_date.desc()).all()
    scam_reports = scam_query.order_by(ScamReport.reported_date.desc()).all()
    contact_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(20).all()
    
    # Calculate statistics
    stats = {
        'total_documents': len(documents),
        'flagged_documents': sum(1 for doc in documents if doc.is_flagged),
        'total_scam_reports': len(scam_reports),
        'high_risk_scams': sum(1 for report in scam_reports if report.risk_level == 'high'),
        'avg_risk_score': sum(doc.risk_score for doc in documents) / len(documents) if documents else 0
    }
    
    # Get keyword trends
    all_keywords = []
    for doc in documents:
        if doc.flagged_keywords:
            keywords = json.loads(doc.flagged_keywords)
            all_keywords.extend(keywords)
    
    keyword_counts = {}
    for keyword in all_keywords:
        keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
    
    top_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return render_template('admin/dashboard.html', 
                         documents=documents,
                         scam_reports=scam_reports,
                         contact_messages=contact_messages,
                         stats=stats,
                         top_keywords=top_keywords,
                         current_filters={
                             'date_filter': date_filter,
                             'type': report_type,
                             'keyword': keyword_filter
                         })

@app.route('/admin/export/documents')
@login_required
def export_documents():
    """Export document analysis data to CSV"""
    documents = DocumentAnalysis.query.order_by(DocumentAnalysis.analysis_date.desc()).all()
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['ID', 'Filename', 'File Type', 'Risk Score', 'Is Flagged', 
                    'Flagged Keywords', 'Analysis Date', 'Summary'])
    
    # Write data
    for doc in documents:
        keywords = json.loads(doc.flagged_keywords) if doc.flagged_keywords else []
        writer.writerow([
            doc.id,
            doc.filename,
            doc.file_type,
            doc.risk_score,
            'Yes' if doc.is_flagged else 'No',
            ', '.join(keywords),
            doc.analysis_date.strftime('%Y-%m-%d %H:%M:%S'),
            doc.summary
        ])
    
    output.seek(0)
    
    # Create response
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=documents_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    return response

@app.route('/admin/export/scams')
@login_required
def export_scam_reports():
    """Export scam reports to CSV"""
    scam_reports = ScamReport.query.order_by(ScamReport.reported_date.desc()).all()
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['ID', 'Type', 'Content', 'Description', 'Risk Level', 
                    'Flagged Patterns', 'Reported Date', 'Verified'])
    
    # Write data
    for report in scam_reports:
        patterns = json.loads(report.flagged_patterns) if report.flagged_patterns else []
        writer.writerow([
            report.id,
            report.report_type,
            report.content,
            report.description,
            report.risk_level,
            ', '.join(patterns),
            report.reported_date.strftime('%Y-%m-%d %H:%M:%S'),
            'Yes' if report.is_verified else 'No'
        ])
    
    output.seek(0)
    
    # Create response
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=scam_reports_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    return response
