# LeakGPT Naija Pro - System Architecture Guide

## Overview

LeakGPT Naija Pro is an anonymous whistleblowing and fraud detection platform specifically designed for Nigeria. The application enables users to upload documents (.txt/.pdf) for AI-powered analysis to detect corruption and fraud indicators, as well as report scam messages, URLs, and phone numbers. The platform emphasizes complete anonymity, security, and real-time analysis capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Bootstrap 5.3.0 with custom CSS for responsive design
- **JavaScript**: Vanilla JavaScript with modern ES6+ features
- **Templates**: Jinja2 templating engine with Flask
- **UI/UX**: Mobile-first responsive design with accessibility considerations
- **Static Assets**: Organized CSS/JS files with proper caching strategies

### Backend Architecture
- **Framework**: Flask with SQLAlchemy ORM
- **Language**: Python 3.8+
- **Structure**: MVC pattern with separate models, views, and business logic
- **File Processing**: PyPDF2 for PDF text extraction, secure file handling
- **Authentication**: Flask-Login for admin sessions only (anonymous public access)

### Database Architecture
- **Primary**: SQLite for development (configurable to PostgreSQL via DATABASE_URL)
- **ORM**: SQLAlchemy with declarative base model
- **Models**: 
  - DocumentAnalysis (stores analysis results)
  - ScamReport (fraud reports)
  - ContactMessage (user inquiries)
  - AdminUser (admin authentication)

## Key Components

### Document Analysis Engine
- **AI Logic Module** (`ai_logic.py`): Mock AI that detects corruption keywords and fraud patterns
- **Text Extraction**: Handles both .txt and .pdf file processing
- **Risk Assessment**: 0-100 scoring system with pattern matching
- **Security**: Files are processed and immediately deleted for anonymity

### Scam Reporting System
- **Multi-Type Support**: Messages, URLs, and phone numbers
- **Pattern Detection**: Nigerian-specific fraud patterns (419 scams, advance fee fraud)
- **Risk Classification**: Automatic categorization (Low/Medium/High)
- **Anonymous Submission**: No user registration required

### Admin Dashboard
- **Analytics**: Comprehensive tracking of uploads and flagged content
- **Export Functionality**: CSV export for documents and scam reports
- **Filtering**: Advanced filtering by date, type, keywords, and risk levels
- **Real-time Statistics**: Live dashboard with key metrics

### Security & Privacy Layer
- **Anonymous Processing**: No personal information stored
- **Secure File Handling**: Files deleted after analysis
- **IP Logging**: Limited logging for security purposes only
- **HTTPS Encryption**: All data transfers encrypted
- **Audit Logging**: Comprehensive tracking of admin actions
- **Rate Limiting**: Client-side protection against spam submissions

## Data Flow

1. **Document Upload Flow**:
   - User uploads file → File validation → Text extraction → AI analysis → Results display → File deletion

2. **Scam Report Flow**:
   - User submits report → Pattern analysis → Risk assessment → Database storage → Confirmation

3. **Admin Analytics Flow**:
   - Database queries → Statistical analysis → Dashboard display → Export capabilities

## External Dependencies

### Core Dependencies
- **Flask**: Web framework and routing
- **SQLAlchemy**: Database ORM and migrations
- **Flask-Login**: Session management for admin users
- **PyPDF2**: PDF text extraction
- **Werkzeug**: Security utilities and file handling

### Frontend Dependencies
- **Bootstrap 5.3.0**: UI framework via CDN
- **Font Awesome 6.4.0**: Icon library via CDN
- **Custom CSS/JS**: Enhanced user experience

### Development Dependencies
- **Python 3.8+**: Runtime environment
- **pip**: Package management

## Deployment Strategy

### Environment Configuration
- **Development**: SQLite database, debug mode enabled
- **Production**: Configurable via environment variables
  - `DATABASE_URL`: Database connection string
  - `SESSION_SECRET`: Session encryption key

### File Storage
- **Upload Directory**: Temporary file storage (`uploads/`)
- **Security**: Files processed and deleted immediately
- **Size Limits**: 16MB maximum file size

### Database Migration
- **Development**: SQLite with auto-creation
- **Production**: PostgreSQL support via environment variables
- **Schema**: Automated table creation on first run

### Security Considerations
- **Anonymous Access**: No user registration for public features
- **Admin Authentication**: Secure login for administrative functions
- **File Security**: Immediate deletion after processing
- **Data Privacy**: Minimal logging and anonymous processing

### Scalability Notes
- **Database**: Easily migrable from SQLite to PostgreSQL
- **File Processing**: Stateless design allows horizontal scaling
- **Caching**: Static assets served with proper headers
- **Session Management**: Server-side sessions for admin users only