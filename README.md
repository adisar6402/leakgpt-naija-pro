# LeakGPT Naija Pro

An anonymous whistleblowing and fraud detection platform powered by AI, specifically designed for Nigeria. This application helps users detect corruption, fraud, and scams by analyzing documents and providing secure reporting mechanisms.

## 🛡️ Features

### Document Analysis
- **File Upload**: Support for `.txt` and `.pdf` files (up to 16MB)
- **AI-Powered Detection**: Advanced keyword analysis for corruption and fraud indicators
- **Risk Assessment**: Comprehensive scoring system (0-100) with detailed summaries
- **Anonymous Processing**: No personal information stored, files deleted after analysis
- **Real-time Results**: Instant analysis with flagged content highlighting

### Scam Reporting
- **Multi-Type Reports**: Support for suspicious messages, URLs, and phone numbers
- **Pattern Detection**: Nigerian-specific fraud pattern recognition
- **Risk Classification**: Automatic risk level assessment (Low/Medium/High)
- **Anonymous Submission**: Complete anonymity for whistleblowers

### Admin Dashboard
- **Comprehensive Analytics**: Track all uploads, flagged content, and trends
- **Advanced Filtering**: Filter by date, type, keywords, and risk levels
- **Export Functionality**: CSV export for documents and scam reports
- **Real-time Statistics**: Live dashboard with key metrics
- **Keyword Trends**: Monitor most common flagged terms

### Security & Privacy
- **Complete Anonymity**: No user registration required
- **Secure File Handling**: Files processed and deleted immediately
- **Encrypted Transmission**: HTTPS encryption for all data transfers
- **IP Privacy**: Limited IP logging for security purposes only

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd leakgpt-naija-pro
   ```

2. **Install dependencies**
   ```bash
   pip install flask flask-sqlalchemy flask-login werkzeug PyPDF2
   ```

3. **Set up environment variables** (optional)
   ```bash
   export SESSION_SECRET="your-secret-key-here"
   export DATABASE_URL="sqlite:///leakgpt.db"
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

### Default Admin Credentials
- **Username**: `admin`
- **Password**: `admin123`

⚠️ **Important**: Change the default admin credentials in production!

## 📁 Project Structure

