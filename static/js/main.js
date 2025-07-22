// Developer branding console message
console.log(
    '%c🛡️ LeakGPT Naija Pro — Developed by Abdulrahman Adisa Amuda',
    'color: #0d6efd; font-size: 16px; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'
);

// Dark mode functionality
class DarkModeManager {
    constructor() {
        this.init();
    }

    init() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        this.setTheme(savedTheme);
        this.bindEvents();
    }

    setTheme(theme) {
        document.documentElement.setAttribute('data-bs-theme', theme);
        localStorage.setItem('theme', theme);
        this.updateToggleIcon(theme);
    }

    updateToggleIcon(theme) {
        const icon = document.getElementById('darkModeIcon');
        if (icon) {
            icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        }
    }

    toggle() {
        const currentTheme = document.documentElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }

    bindEvents() {
        const toggleBtn = document.getElementById('darkModeToggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => this.toggle());
        }
    }
}

// Loading spinner utility
class LoadingManager {
    static show(element, message = 'Processing...') {
        if (element) {
            element.disabled = true;
            element.innerHTML = `<i class="fas fa-spinner fa-spin me-2"></i>${message}`;
            element.setAttribute('aria-busy', 'true');
        }
    }

    static hide(element, originalText = 'Submit') {
        if (element) {
            element.disabled = false;
            element.innerHTML = originalText;
            element.removeAttribute('aria-busy');
        }
    }

    static showOverlay(message = 'Processing your request...') {
        const overlay = document.createElement('div');
        overlay.id = 'loadingOverlay';
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="loading-content">
                <div class="spinner-border text-primary mb-3" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mb-0">${message}</p>
            </div>
        `;
        overlay.setAttribute('aria-live', 'polite');
        overlay.setAttribute('aria-label', message);
        document.body.appendChild(overlay);
    }

    static hideOverlay() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.remove();
        }
    }
}

// File upload validation with enhanced error handling
function validateFile(input) {
    const file = input.files[0];
    const maxSize = 16 * 1024 * 1024; // 16MB
    const allowedTypes = ['text/plain', 'application/pdf'];
    
    if (file) {
        // Clear previous error messages
        const errorDiv = document.getElementById('fileError');
        if (errorDiv) errorDiv.remove();

        if (file.size > maxSize) {
            showFileError(input, 'File size must be less than 16MB');
            return false;
        }
        
        if (!allowedTypes.includes(file.type)) {
            showFileError(input, 'Only .txt and .pdf files are allowed');
            return false;
        }

        // Show file selected indicator
        showFileSuccess(input, `Selected: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`);
    }
    
    return true;
}

function showFileError(input, message) {
    input.value = '';
    const errorDiv = document.createElement('div');
    errorDiv.id = 'fileError';
    errorDiv.className = 'alert alert-danger mt-2';
    errorDiv.innerHTML = `<i class="fas fa-exclamation-circle me-2"></i>${message}`;
    errorDiv.setAttribute('role', 'alert');
    input.parentNode.appendChild(errorDiv);
}

function showFileSuccess(input, message) {
    const errorDiv = document.getElementById('fileError');
    if (errorDiv) errorDiv.remove();
    
    const successDiv = document.createElement('div');
    successDiv.id = 'fileSuccess';
    successDiv.className = 'alert alert-success mt-2';
    successDiv.innerHTML = `<i class="fas fa-check-circle me-2"></i>${message}`;
    successDiv.setAttribute('role', 'status');
    input.parentNode.appendChild(successDiv);
}

// Rate limiting utility
class RateLimiter {
    constructor(limit = 5, windowMs = 300000) { // 5 requests per 5 minutes
        this.limit = limit;
        this.windowMs = windowMs;
        this.requests = [];
    }

    canMakeRequest() {
        const now = Date.now();
        this.requests = this.requests.filter(time => now - time < this.windowMs);
        
        if (this.requests.length >= this.limit) {
            return false;
        }
        
        this.requests.push(now);
        return true;
    }

    getRetryAfter() {
        if (this.requests.length > 0) {
            const oldestRequest = Math.min(...this.requests);
            return Math.ceil((oldestRequest + this.windowMs - Date.now()) / 1000);
        }
        return 0;
    }
}

// Enhanced form handling with accessibility and rate limiting
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dark mode
    new DarkModeManager();

    // Initialize rate limiters
    const uploadLimiter = new RateLimiter(3, 300000); // 3 uploads per 5 minutes
    const reportLimiter = new RateLimiter(5, 300000); // 5 reports per 5 minutes

    // Enhanced form submission handling
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const formType = form.getAttribute('data-form-type') || 'general';
            let limiter = null;
            let loadingMessage = 'Processing...';

            // Determine rate limiter and message based on form type
            if (formType === 'upload' || form.querySelector('input[type="file"]')) {
                limiter = uploadLimiter;
                loadingMessage = 'Analyzing document...';
            } else if (formType === 'scam-report' || form.action.includes('scam')) {
                limiter = reportLimiter;
                loadingMessage = 'Processing report...';
            }

            // Check rate limiting
            if (limiter && !limiter.canMakeRequest()) {
                e.preventDefault();
                const retryAfter = limiter.getRetryAfter();
                alert(`Too many requests. Please wait ${retryAfter} seconds before trying again.`);
                return;
            }

            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn ? submitBtn.textContent : 'Submit';
            
            if (submitBtn) {
                LoadingManager.show(submitBtn, loadingMessage);
                
                // Show overlay for file uploads
                if (formType === 'upload' || form.querySelector('input[type="file"]')) {
                    LoadingManager.showOverlay('AI is analyzing your document for corruption indicators...');
                }
            }

            // Reset form state on page unload (in case of errors)
            window.addEventListener('beforeunload', function() {
                if (submitBtn) {
                    LoadingManager.hide(submitBtn, originalText);
                }
                LoadingManager.hideOverlay();
            });
        });
    });
    
    // Enhanced file input handling
    const fileInput = document.getElementById('file');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            validateFile(this);
        });

        // Keyboard accessibility for file input
        fileInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    }

    // Keyboard navigation improvements
    const navLinks = document.querySelectorAll('.nav-link, .btn');
    navLinks.forEach(link => {
        link.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                this.click();
            }
        });
    });

    // Focus management for modals and overlays
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('shown.bs.modal', function() {
            const firstInput = this.querySelector('input, select, textarea, button');
            if (firstInput) firstInput.focus();
        });
    });

    // Error message accessibility
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (!alert.getAttribute('role')) {
            alert.setAttribute('role', alert.classList.contains('alert-danger') ? 'alert' : 'status');
        }
    });

    // Enhanced skip link functionality
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Skip to main content';
    skipLink.className = 'skip-link visually-hidden-focusable';
    skipLink.style.cssText = `
        position: absolute;
        top: -40px;
        left: 6px;
        z-index: 9999;
        padding: 8px 16px;
        background: #0d6efd;
        color: white;
        text-decoration: none;
        border-radius: 4px;
        transition: top 0.3s;
    `;
    skipLink.addEventListener('focus', function() {
        this.style.top = '6px';
    });
    skipLink.addEventListener('blur', function() {
        this.style.top = '-40px';
    });
    document.body.insertBefore(skipLink, document.body.firstChild);

    // Add main content ID for skip link
    const mainContent = document.querySelector('main') || document.querySelector('.main-content');
    if (mainContent && !mainContent.id) {
        mainContent.id = 'main-content';
        mainContent.setAttribute('tabindex', '-1');
    }
});