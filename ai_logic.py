import re
import json
from datetime import datetime

# Fraud and corruption keywords
CORRUPTION_KEYWORDS = [
    'kickback', 'embezzlement', 'bribe', 'bribery', 'fraud', 'fraudulent',
    'corruption', 'corrupt', 'money laundering', 'illegal payment',
    '419', 'advance fee', 'wire transfer', 'offshore account',
    'under the table', 'palm greasing', 'envelope', 'cash payment',
    'ghost worker', 'inflated contract', 'phantom project',
    'budget padding', 'overinvoicing', 'kickbacks', 'cut',
    'settlement', 'gratification', 'commission', 'facilitation fee',
    'speed money', 'dash', 'kola', 'brown envelope',
    'contract inflation', 'budget manipulation', 'fake receipt',
    'double payment', 'ghost employee', 'phantom worker'
]

# Nigerian-specific fraud patterns
NIGERIAN_FRAUD_PATTERNS = [
    r'\b419\b', r'\babanijere\b', r'\byahoo\sboy\b', r'\bg\s*boys\b',
    r'\bmaga\b', r'\bmugu\b', r'\bformat\b', r'\bbilling\b',
    r'\bwire\stransfer\b', r'\binheritance\b', r'\blottery\b',
    r'\bcentral\sbank\b', r'\bminister\b', r'\bgeneral\b',
    r'\bmillion\sdollars\b', r'\btrust\sfund\b', r'\bbeneficiary\b'
]

# Scam patterns for different types
SCAM_PATTERNS = {
    'message': [
        r'urgent\s+response', r'wire\s+transfer', r'inheritance',
        r'lottery\s+winner', r'confidential\s+business', r'beneficiary',
        r'transfer.*million', r'diplomat', r'consignment', 
        r'deposit.*bank', r'claim.*fund', r'next.*kin'
    ],
    'url': [
        r'bit\.ly', r'tinyurl', r'goo\.gl', r't\.co',
        r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+',  # IP addresses
        r'[a-z0-9-]+\.tk$', r'[a-z0-9-]+\.ml$',  # Suspicious TLDs
        r'secure.*update', r'verify.*account', r'suspended.*account'
    ],
    'phone': [
        r'^\+?234[0-9]{10}$',  # Nigerian numbers
        r'^\+?1[0-9]{10}$',    # US numbers (often spoofed)
        r'^\+?44[0-9]{10}$',   # UK numbers (often spoofed)
    ]
}

def analyze_document(text_content):
    """
    Analyze document content for fraud and corruption indicators
    
    Args:
        text_content (str): The text content to analyze
        
    Returns:
        dict: Analysis results including flagged keywords, risk score, and summary
    """
    text_lower = text_content.lower()
    flagged_keywords = []
    risk_score = 0
    
    # Check for corruption keywords
    for keyword in CORRUPTION_KEYWORDS:
        if keyword.lower() in text_lower:
            flagged_keywords.append(keyword)
            # Higher weight for more serious terms
            if keyword.lower() in ['embezzlement', 'bribe', 'kickback', 'money laundering']:
                risk_score += 15
            else:
                risk_score += 10
    
    # Check for Nigerian fraud patterns
    for pattern in NIGERIAN_FRAUD_PATTERNS:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        if matches:
            flagged_keywords.extend(matches)
            risk_score += 20
    
    # Additional risk factors
    # Large monetary amounts
    money_patterns = re.findall(r'[\$₦€£][\d,]+(?:\.\d{2})?', text_content)
    if money_patterns:
        risk_score += len(money_patterns) * 5
    
    # Urgency indicators
    urgency_words = ['urgent', 'immediate', 'asap', 'deadline', 'expire']
    urgency_count = sum(1 for word in urgency_words if word in text_lower)
    risk_score += urgency_count * 3
    
    # Secrecy indicators
    secrecy_words = ['confidential', 'secret', 'private', 'discreet', 'classified']
    secrecy_count = sum(1 for word in secrecy_words if word in text_lower)
    risk_score += secrecy_count * 5
    
    # Cap risk score at 100
    risk_score = min(risk_score, 100)
    
    # Determine if flagged
    is_flagged = risk_score >= 30 or len(flagged_keywords) >= 3
    
    # Generate summary
    summary = generate_analysis_summary(flagged_keywords, risk_score, is_flagged)
    
    return {
        'flagged_keywords': list(set(flagged_keywords)),  # Remove duplicates
        'risk_score': risk_score,
        'is_flagged': is_flagged,
        'summary': summary
    }

def analyze_scam_content(content, report_type):
    """
    Analyze scam report content for suspicious patterns
    
    Args:
        content (str): The content to analyze
        report_type (str): Type of report (message, url, phone)
        
    Returns:
        dict: Analysis results including patterns and risk level
    """
    content_lower = content.lower()
    flagged_patterns = []
    risk_score = 0
    
    # Get patterns for specific report type
    patterns = SCAM_PATTERNS.get(report_type, [])
    
    # Check for type-specific patterns
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            flagged_patterns.extend(matches)
            risk_score += 25
    
    # General fraud indicators
    fraud_indicators = [
        'free money', 'guaranteed profit', 'risk free', 'get rich quick',
        'make money fast', 'no experience needed', 'work from home',
        'click here now', 'limited time offer', 'act now'
    ]
    
    for indicator in fraud_indicators:
        if indicator in content_lower:
            flagged_patterns.append(indicator)
            risk_score += 15
    
    # Nigerian specific terms
    nigerian_terms = ['naira', 'lagos', 'abuja', 'cbn', 'efcc', 'nnpc']
    for term in nigerian_terms:
        if term in content_lower:
            flagged_patterns.append(term)
            risk_score += 10
    
    # Determine risk level
    if risk_score >= 50:
        risk_level = 'high'
    elif risk_score >= 25:
        risk_level = 'medium'
    else:
        risk_level = 'low'
    
    return {
        'patterns': list(set(flagged_patterns)),
        'risk_level': risk_level,
        'risk_score': risk_score
    }

def generate_analysis_summary(flagged_keywords, risk_score, is_flagged):
    """
    Generate a human-readable summary of the analysis
    
    Args:
        flagged_keywords (list): List of flagged keywords
        risk_score (int): Risk score (0-100)
        is_flagged (bool): Whether the document is flagged
        
    Returns:
        str: Summary text
    """
    if not is_flagged:
        return "Document analysis complete. No significant fraud or corruption indicators detected."
    
    summary_parts = []
    
    if risk_score >= 70:
        summary_parts.append("⚠️ HIGH RISK: This document contains multiple indicators of potential fraud or corruption.")
    elif risk_score >= 40:
        summary_parts.append("⚠️ MODERATE RISK: This document contains some indicators that warrant further investigation.")
    else:
        summary_parts.append("ℹ️ LOW RISK: This document contains minor indicators that may require attention.")
    
    if flagged_keywords:
        keyword_text = ", ".join(flagged_keywords[:5])  # Show first 5 keywords
        if len(flagged_keywords) > 5:
            keyword_text += f" and {len(flagged_keywords) - 5} more"
        summary_parts.append(f"Flagged terms detected: {keyword_text}")
    
    # Add recommendations
    if risk_score >= 50:
        summary_parts.append("Recommendation: This document should be reviewed by compliance officers or relevant authorities.")
    elif risk_score >= 30:
        summary_parts.append("Recommendation: Consider additional review or investigation of the flagged content.")
    
    return " ".join(summary_parts)
