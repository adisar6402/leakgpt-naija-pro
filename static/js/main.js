/**
 * LeakGPT Naija Pro - Main JavaScript File
 * Handles global functionality and enhanced user interactions
 */

// Global app configuration
const LeakGPT = {
    config: {
        uploadMaxSize: 16 * 1024 * 1024, // 16MB
        allowedFileTypes: ['txt', 'pdf'],
        apiEndpoints: {
            upload: '/upload',
            scamReport: '/scam-report',
            contact: '/contact'
        }
    },
    
    // Initialize the application
    init() {
        this.setupEventListeners();
        this.initializeComponents();
        this.setupFormValidation();
        this.initializeAnimations();
        this.setupAccessibility();
    },

    // Setup global event listeners
    setupEventListeners() {
        document.addEventListener('DOMContentLoaded', () => {
            this.handleNavbarScroll();
            this.initializeTooltips();
            this.setupFileUpload();
            this.setupFormEnhancements();
            this.setupTableSorting();
        });

        // Handle window resize
        window.addEventListener('resize', this.debounce(() => {
            this.handleResponsiveUpdates();
        }, 250));

        // Handle visibility change for auto-refresh
        document.addEventListener('visibilitychange', () => {
            this.handleVisibilityChange();
        });
    },

    // Initialize Bootstrap and other components
    initializeComponents() {
        // Initialize tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(tooltipTriggerEl => {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });

        // Initialize popovers
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(popoverTriggerEl => {
            return new bootstrap.Popover(popoverTriggerEl);
        });

        // Initialize modals
        this.setupModals();
    },

    // Enhanced file upload handling
    setupFileUpload() {
        const fileInputs = document.querySelectorAll('input[type="file"]');
        
        fileInputs.forEach(input => {
            // Drag and drop functionality
            this.setupDragAndDrop(input);
            
            // File validation
            input.addEventListener('change', (e) => {
                this.validateFile(e.target);
            });
        });
    },

    // Setup drag and drop for file uploads
    setupDragAndDrop(fileInput) {
        const dropZone = fileInput.closest('.card-body') || fileInput.parentElement;
        
        if (!dropZone) return;

        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('drag-over');
        });

        dropZone.addEventListener('dragleave', (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                this.validateFile(fileInput);
            }
        });
    },

    // File validation
    validateFile(fileInput) {
        const file = fileInput.files[0];
        if (!file) return;

        const errors = [];

        // Check file size
        if (file.size > this.config.uploadMaxSize) {
            errors.push(`File size must be less than ${this.formatFileSize(this.config.uploadMaxSize)}`);
        }

        // Check file type
        const extension = file.name.split('.').pop().toLowerCase();
        if (!this.config.allowedFileTypes.includes(extension)) {
            errors.push(`File type .${extension} is not allowed. Please upload ${this.config.allowedFileTypes.map(t => `.${t}`).join(', ')} files only.`);
        }

        // Display errors or success
        this.displayFileValidation(fileInput, errors, file);

        return errors.length === 0;
    },

    // Display file validation results
    displayFileValidation(fileInput, errors, file) {
        const container = fileInput.closest('.card-body') || fileInput.parentElement;
        
        // Remove existing validation messages
        const existingAlert = container.querySelector('.file-validation-alert');
        if (existingAlert) {
            existingAlert.remove();
        }

        if (errors.length > 0) {
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-danger file-validation-alert mt-2';
            alertDiv.innerHTML = `
                <strong>File Validation Error:</strong>
                <ul class="mb-0 mt-1">
                    ${errors.map(error => `<li>${error}</li>`).join('')}
                </ul>
            `;
            fileInput.parentElement.appendChild(alertDiv);
            
            // Clear the file input
            fileInput.value = '';
        } else if (file) {
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-success file-validation-alert mt-2';
            alertDiv.innerHTML = `
                <i class="fas fa-check-circle me-2"></i>
                <strong>${file.name}</strong> (${this.formatFileSize(file.size)}) - Ready for upload
            `;
            fileInput.parentElement.appendChild(alertDiv);
        }
    },

    // Format file size for display
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    // Form enhancement and validation
    setupFormEnhancements() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            // Add loading states
            form.addEventListener('submit', (e) => {
                this.handleFormSubmission(form);
            });

            // Real-time validation
            const inputs = form.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                input.addEventListener('blur', () => {
                    this.validateField(input);
                });
            });
        });
    },

    // Handle form submission with loading states
    handleFormSubmission(form) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (!submitBtn) return;

        const originalText = submitBtn.innerHTML;
        const loadingText = submitBtn.dataset.loading || '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        
        submitBtn.innerHTML = loadingText;
        submitBtn.disabled = true;

        // Re-enable after timeout (fallback)
        setTimeout(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }, 30000);
    },

    // Field validation
    validateField(field) {
        const fieldType = field.type;
        const value = field.value.trim();
        let isValid = true;
        let message = '';

        // Email validation
        if (fieldType === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                message = 'Please enter a valid email address';
            }
        }

        // Phone validation for Nigerian numbers
        if (field.name === 'phone' && value) {
            const phoneRegex = /^(\+234|234|0)[789]\d{9}$/;
            if (!phoneRegex.test(value)) {
                isValid = false;
                message = 'Please enter a valid Nigerian phone number';
            }
        }

        // URL validation
        if (field.name === 'url' || fieldType === 'url') {
            try {
                new URL(value);
            } catch {
                isValid = false;
                message = 'Please enter a valid URL';
            }
        }

        this.displayFieldValidation(field, isValid, message);
        return isValid;
    },

    // Display field validation
    displayFieldValidation(field, isValid, message) {
        const feedback = field.parentElement.querySelector('.invalid-feedback') || 
                        field.parentElement.querySelector('.valid-feedback');
        
        if (feedback) {
            feedback.remove();
        }

        if (!isValid && message) {
            field.classList.add('is-invalid');
            field.classList.remove('is-valid');
            
            const feedbackDiv = document.createElement('div');
            feedbackDiv.className = 'invalid-feedback';
            feedbackDiv.textContent = message;
            field.parentElement.appendChild(feedbackDiv);
        } else if (field.value.trim()) {
            field.classList.add('is-valid');
            field.classList.remove('is-invalid');
        }
    },

    // Setup form validation
    setupFormValidation() {
        // Custom validation for specific forms
        const scamReportForm = document.getElementById('scamReportForm');
        if (scamReportForm) {
            this.setupScamReportValidation(scamReportForm);
        }

        const contactForm = document.getElementById('contactForm');
        if (contactForm) {
            this.setupContactFormValidation(contactForm);
        }
    },

    // Scam report form validation
    setupScamReportValidation(form) {
        const reportTypeInputs = form.querySelectorAll('input[name="report_type"]');
        const contentField = form.querySelector('#content');
        
        reportTypeInputs.forEach(input => {
            input.addEventListener('change', () => {
                this.updateScamReportUI(input.value, contentField);
            });
        });
    },

    // Update scam report UI based on selected type
    updateScamReportUI(type, contentField) {
        const examples = {
            message: {
                placeholder: 'Paste the suspicious message here...',
                help: 'Copy and paste the exact message you received'
            },
            url: {
                placeholder: 'https://suspicious-website.com',
                help: 'Enter the complete URL of the suspicious website'
            },
            phone: {
                placeholder: '+234 xxx xxx xxxx',
                help: 'Enter the phone number that contacted you'
            }
        };

        if (examples[type]) {
            contentField.placeholder = examples[type].placeholder;
            const helpText = contentField.parentElement.querySelector('.form-text');
            if (helpText) {
                helpText.textContent = examples[type].help;
            }
        }
    },

    // Contact form validation
    setupContactFormValidation(form) {
        const messageField = form.querySelector('#message');
        if (messageField) {
            messageField.addEventListener('input', () => {
                this.updateCharacterCount(messageField);
            });
        }
    },

    // Update character count for text areas
    updateCharacterCount(textArea) {
        const currentLength = textArea.value.length;
        const minLength = 10;
        
        let counter = textArea.parentElement.querySelector('.char-counter');
        if (!counter) {
            counter = document.createElement('div');
            counter.className = 'char-counter form-text text-end';
            textArea.parentElement.appendChild(counter);
        }

        counter.textContent = `${currentLength} characters`;
        
        if (currentLength < minLength) {
            counter.classList.add('text-danger');
            counter.classList.remove('text-success');
            textArea.classList.add('is-invalid');
            textArea.classList.remove('is-valid');
        } else {
            counter.classList.add('text-success');
            counter.classList.remove('text-danger');
            textArea.classList.add('is-valid');
            textArea.classList.remove('is-invalid');
        }
    },

    // Handle navbar scroll effects
    handleNavbarScroll() {
        const navbar = document.querySelector('.navbar');
        if (!navbar) return;

        let lastScrollTop = 0;
        
        window.addEventListener('scroll', () => {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > 100) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }

            // Hide/show navbar on scroll
            if (scrollTop > lastScrollTop && scrollTop > 200) {
                navbar.style.transform = 'translateY(-100%)';
            } else {
                navbar.style.transform = 'translateY(0)';
            }
            
            lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
        });
    },

    // Initialize animations
    initializeAnimations() {
        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);

        // Observe elements for animation
        const animateElements = document.querySelectorAll('.feature-card, .stat-card, .card');
        animateElements.forEach(el => {
            observer.observe(el);
        });
    },

    // Setup table sorting
    setupTableSorting() {
        const tables = document.querySelectorAll('table.sortable');
        tables.forEach(table => {
            this.makeSortable(table);
        });
    },

    // Make table sortable
    makeSortable(table) {
        const headers = table.querySelectorAll('th');
        headers.forEach((header, index) => {
            if (header.dataset.sortable !== 'false') {
                header.style.cursor = 'pointer';
                header.addEventListener('click', () => {
                    this.sortTable(table, index);
                });
            }
        });
    },

    // Sort table by column
    sortTable(table, columnIndex) {
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const isAscending = table.dataset.sortDirection !== 'asc';
        
        rows.sort((a, b) => {
            const cellA = a.cells[columnIndex].textContent.trim();
            const cellB = b.cells[columnIndex].textContent.trim();
            
            // Try to parse as number
            const numA = parseFloat(cellA);
            const numB = parseFloat(cellB);
            
            if (!isNaN(numA) && !isNaN(numB)) {
                return isAscending ? numA - numB : numB - numA;
            }
            
            // String comparison
            return isAscending ? 
                cellA.localeCompare(cellB) : 
                cellB.localeCompare(cellA);
        });

        // Clear tbody and re-append sorted rows
        tbody.innerHTML = '';
        rows.forEach(row => tbody.appendChild(row));
        
        // Update sort direction
        table.dataset.sortDirection = isAscending ? 'asc' : 'desc';
        
        // Update header indicators
        const headers = table.querySelectorAll('th');
        headers.forEach((h, i) => {
            h.classList.remove('sort-asc', 'sort-desc');
            if (i === columnIndex) {
                h.classList.add(isAscending ? 'sort-asc' : 'sort-desc');
            }
        });
    },

    // Setup modals
    setupModals() {
        // Auto-show modals based on URL parameters
        const urlParams = new URLSearchParams(window.location.search);
        const showModal = urlParams.get('modal');
        if (showModal) {
            const modal = document.getElementById(showModal);
            if (modal) {
                const bsModal = new bootstrap.Modal(modal);
                bsModal.show();
            }
        }
    },

    // Initialize tooltips
    initializeTooltips() {
        // Add tooltips to truncated text
        const truncatedElements = document.querySelectorAll('[title]');
        truncatedElements.forEach(el => {
            if (el.scrollWidth > el.clientWidth) {
                el.setAttribute('data-bs-toggle', 'tooltip');
                el.setAttribute('data-bs-placement', 'top');
                new bootstrap.Tooltip(el);
            }
        });
    },

    // Setup accessibility features
    setupAccessibility() {
        // Skip links
        this.addSkipLinks();
        
        // Focus management
        this.manageFocus();
        
        // Keyboard navigation
        this.setupKeyboardNavigation();
    },

    // Add skip links for accessibility
    addSkipLinks() {
        if (document.querySelector('.skip-links')) return;
        
        const skipLinks = document.createElement('div');
        skipLinks.className = 'skip-links sr-only';
        skipLinks.innerHTML = `
            <a href="#main-content" class="skip-link">Skip to main content</a>
            <a href="#navigation" class="skip-link">Skip to navigation</a>
        `;
        document.body.insertBefore(skipLinks, document.body.firstChild);
    },

    // Manage focus for accessibility
    manageFocus() {
        // Focus first input in modals
        document.addEventListener('shown.bs.modal', (e) => {
            const firstInput = e.target.querySelector('input, select, textarea');
            if (firstInput) {
                firstInput.focus();
            }
        });
    },

    // Setup keyboard navigation
    setupKeyboardNavigation() {
        // Global keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Alt + H = Home
            if (e.altKey && e.key === 'h') {
                window.location.href = '/';
            }
            
            // Alt + U = Upload
            if (e.altKey && e.key === 'u') {
                window.location.href = '/upload';
            }
            
            // Alt + R = Report Scam
            if (e.altKey && e.key === 'r') {
                window.location.href = '/scam-report';
            }
        });
    },

    // Handle visibility change for auto-refresh
    handleVisibilityChange() {
        if (document.hidden) {
            // Page is hidden, pause any auto-refresh
            if (this.refreshInterval) {
                clearInterval(this.refreshInterval);
            }
        } else {
            // Page is visible, resume auto-refresh if needed
            this.setupAutoRefresh();
        }
    },

    // Setup auto-refresh for admin dashboard
    setupAutoRefresh() {
        if (window.location.pathname.includes('/admin/dashboard')) {
            this.refreshInterval = setInterval(() => {
                // Only refresh if no modals are open and user isn't actively typing
                const activeModal = document.querySelector('.modal.show');
                const activeInput = document.activeElement;
                
                if (!activeModal && (!activeInput || activeInput.tagName !== 'INPUT')) {
                    this.softRefresh();
                }
            }, 60000); // Refresh every minute
        }
    },

    // Soft refresh that preserves scroll position
    softRefresh() {
        const scrollPosition = window.scrollY;
        
        fetch(window.location.href)
            .then(response => response.text())
            .then(html => {
                // Update only the content areas, not the entire page
                const parser = new DOMParser();
                const newDoc = parser.parseFromString(html, 'text/html');
                
                // Update statistics
                const statsElements = document.querySelectorAll('.stat-number');
                const newStatsElements = newDoc.querySelectorAll('.stat-number');
                
                statsElements.forEach((stat, index) => {
                    if (newStatsElements[index]) {
                        this.animateCountUp(stat, parseInt(newStatsElements[index].textContent));
                    }
                });
                
                // Restore scroll position
                window.scrollTo(0, scrollPosition);
            })
            .catch(error => {
                console.error('Auto-refresh failed:', error);
            });
    },

    // Animate count up for statistics
    animateCountUp(element, targetValue) {
        const currentValue = parseInt(element.textContent) || 0;
        const increment = Math.ceil((targetValue - currentValue) / 20);
        
        if (increment === 0) return;
        
        const timer = setInterval(() => {
            const newValue = parseInt(element.textContent) + increment;
            
            if ((increment > 0 && newValue >= targetValue) || 
                (increment < 0 && newValue <= targetValue)) {
                element.textContent = targetValue;
                clearInterval(timer);
            } else {
                element.textContent = newValue;
            }
        }, 50);
    },

    // Handle responsive updates
    handleResponsiveUpdates() {
        // Update table responsive behavior
        const tables = document.querySelectorAll('table');
        tables.forEach(table => {
            const container = table.closest('.table-responsive');
            if (container && window.innerWidth < 768) {
                // Add mobile-friendly table styling
                table.classList.add('table-sm');
            } else {
                table.classList.remove('table-sm');
            }
        });
    },

    // Utility: Debounce function
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Utility: Show notification
    showNotification(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed notification`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after duration
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, duration);
    },

    // Utility: Copy to clipboard
    copyToClipboard(text) {
        if (navigator.clipboard) {
            return navigator.clipboard.writeText(text).then(() => {
                this.showNotification('Copied to clipboard!', 'success');
            });
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            
            try {
                document.execCommand('copy');
                this.showNotification('Copied to clipboard!', 'success');
            } catch (err) {
                this.showNotification('Failed to copy to clipboard', 'danger');
            }
            
            document.body.removeChild(textArea);
        }
    },

    // Utility: Format currency
    formatCurrency(amount, currency = '₦') {
        return `${currency}${amount.toLocaleString()}`;
    },

    // Utility: Format date
    formatDate(dateString, options = {}) {
        const date = new Date(dateString);
        const defaultOptions = {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };
        
        return date.toLocaleDateString('en-NG', { ...defaultOptions, ...options });
    }
};

// Initialize the application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    LeakGPT.init();
});

// Global functions for template use
window.copyToClipboard = (text) => LeakGPT.copyToClipboard(text);
window.showNotification = (message, type, duration) => LeakGPT.showNotification(message, type, duration);

// Export for module use if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LeakGPT;
}
