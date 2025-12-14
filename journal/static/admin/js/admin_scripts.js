/**
 * Admin Panel Interactive Features
 * Handles maintenance mode toggle, toast notifications, and real-time updates
 */

document.addEventListener('DOMContentLoaded', function () {
    initMaintenanceToggle();
    initToastNotifications();
});

/**
 * Initialize Maintenance Mode Toggle
 */
function initMaintenanceToggle() {
    const toggle = document.getElementById('maintenanceToggle');
    if (!toggle) return;

    toggle.addEventListener('change', function () {
        const isEnabled = this.checked;
        const configId = this.dataset.configId;

        // Show loading state
        const card = document.querySelector('.maintenance-card');
        card.classList.add('loading');

        // Get CSRF token
        const csrfToken = getCookie('csrftoken');

        // Send AJAX request
        fetch('/admin/toggle-maintenance/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                maintenance_mode: isEnabled,
                config_id: configId
            })
        })
            .then(response => response.json())
            .then(data => {
                card.classList.remove('loading');

                if (data.success) {
                    // Update status indicator
                    updateStatusIndicator(isEnabled);

                    // Show success toast
                    showToast(
                        'success',
                        `Maintenance mode ${isEnabled ? 'enabled' : 'disabled'} successfully!`
                    );
                } else {
                    // Revert toggle on error
                    toggle.checked = !isEnabled;
                    showToast('error', data.message || 'Failed to update maintenance mode');
                }
            })
            .catch(error => {
                card.classList.remove('loading');
                toggle.checked = !isEnabled;
                showToast('error', 'An error occurred. Please try again.');
                console.error('Error:', error);
            });
    });
}

/**
 * Update Status Indicator
 */
function updateStatusIndicator(isMaintenanceMode) {
    const indicator = document.querySelector('.status-indicator');
    const statusText = indicator.querySelector('.status-text');

    if (isMaintenanceMode) {
        indicator.classList.remove('status-live');
        indicator.classList.add('status-maintenance');
        statusText.textContent = 'Maintenance';
    } else {
        indicator.classList.remove('status-maintenance');
        indicator.classList.add('status-live');
        statusText.textContent = 'Live';
    }
}

/**
 * Toast Notification System
 */
let toastContainer;

function initToastNotifications() {
    toastContainer = document.getElementById('toastContainer');
}

function showToast(type, message) {
    if (!toastContainer) {
        toastContainer = document.getElementById('toastContainer');
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    const icon = document.createElement('div');
    icon.className = 'toast-icon';

    if (type === 'success') {
        icon.innerHTML = `
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" style="color: #10b981;">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
        `;
    } else {
        icon.innerHTML = `
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" style="color: #ef4444;">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
        `;
    }

    const messageEl = document.createElement('div');
    messageEl.className = 'toast-message';
    messageEl.textContent = message;

    toast.appendChild(icon);
    toast.appendChild(messageEl);
    toastContainer.appendChild(toast);

    // Auto-remove after 4 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 4000);
}

/**
 * Get CSRF Token from Cookies
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Auto-refresh Statistics (Optional - every 30 seconds)
 */
function autoRefreshStats() {
    setInterval(() => {
        fetch('/admin/get-stats/')
            .then(response => response.json())
            .then(data => {
                updateStatCards(data);
            })
            .catch(error => console.error('Error refreshing stats:', error));
    }, 30000); // 30 seconds
}

/**
 * Update Stat Cards with New Data
 */
function updateStatCards(data) {
    if (data.total_users !== undefined) {
        document.querySelector('.stat-card:nth-child(1) .stat-value').textContent = data.total_users;
    }
    if (data.total_entries !== undefined) {
        document.querySelector('.stat-card:nth-child(2) .stat-value').textContent = data.total_entries;
    }
    if (data.active_users_today !== undefined) {
        document.querySelector('.stat-card:nth-child(3) .stat-value').textContent = data.active_users_today;
    }
    if (data.google_users !== undefined) {
        document.querySelector('.stat-card:nth-child(4) .stat-value').textContent = data.google_users;
    }
}

// Add slideOut animation to CSS dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
