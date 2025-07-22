import os
import PyPDF2
from flask import request
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf'}

def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension
    
    Args:
        filename (str): The filename to check
        
    Returns:
        bool: True if file extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    """
    Extract text content from a PDF file
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text content
        
    Raises:
        Exception: If PDF cannot be read or processed
    """
    try:
        text_content = ""
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Extract text from all pages
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += page.extract_text() + "\n"
        
        # Clean up the text
        text_content = text_content.strip()
        
        if not text_content:
            raise Exception("No text content could be extracted from the PDF")
            
        return text_content
        
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def get_client_ip():
    """
    Get the client's IP address, handling proxies
    
    Returns:
        str: Client IP address
    """
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr

def sanitize_filename(filename):
    """
    Sanitize filename for safe storage
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Use werkzeug's secure_filename and add timestamp
    from datetime import datetime
    
    secure_name = secure_filename(filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
    
    return timestamp + secure_name

def format_file_size(size_bytes):
    """
    Format file size in human readable format
    
    Args:
        size_bytes (int): File size in bytes
        
    Returns:
        str: Formatted file size
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s} {size_names[i]}"

def validate_file_upload(file):
    """
    Validate uploaded file for security and format requirements
    
    Args:
        file: Flask file upload object
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not file:
        return False, "No file provided"
    
    if file.filename == '':
        return False, "No file selected"
    
    if not allowed_file(file.filename):
        return False, "File type not allowed. Please upload .txt or .pdf files only."
    
    # Check file size (assuming max 16MB from app config)
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    file.seek(0)  # Reset to beginning
    
    max_size = 16 * 1024 * 1024  # 16MB
    if file_size > max_size:
        return False, f"File too large. Maximum size is {format_file_size(max_size)}"
    
    if file_size == 0:
        return False, "File is empty"
    
    return True, None
