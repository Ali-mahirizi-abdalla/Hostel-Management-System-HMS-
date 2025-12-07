/**
 * Smart Hostel Management System
 * Premium Interactive JavaScript
 */

// ==================== DOM Ready ====================
document.addEventListener('DOMContentLoaded', function () {
    initializePage();
    initializeAnimations();
    initializeInteractiveElements();
    initializeParticles();
    initializeScrollEffects();
    initializeTiltEffect();
    initializeTooltips();
    initializeNotifications();
});

// ==================== Page Initialization ====================
function initializePage() {
    // Add loading complete class
    document.body.classList.add('loaded');

    // Stagger animation for cards
    const cards = document.querySelectorAll('.glass-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('animate-slide-up');
    });

    // Initialize counters
    initializeCounters();
}

// ==================== Counter Animation ====================
function initializeCounters() {
    const counters = document.querySelectorAll('[data-count]');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                animateCounter(counter);
                observer.unobserve(counter);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => observer.observe(counter));
}

function animateCounter(element) {
    const target = parseInt(element.dataset.count);
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;

    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current);
    }, 16);
}

// ==================== Scroll Effects ====================
function initializeScrollEffects() {
    // Navbar background on scroll
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }

    // Reveal elements on scroll
    const revealElements = document.querySelectorAll('.glass-card, .gallery-item, .status-item');

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    revealElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
        revealObserver.observe(el);
    });

    // Parallax effect
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('[data-parallax]');

        parallaxElements.forEach(el => {
            const speed = el.dataset.parallax || 0.5;
            el.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });
}

// ==================== Interactive Animations ====================
function initializeAnimations() {
    // Ripple effect on buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', createRipple);
    });

    // Magnetic effect on buttons
    buttons.forEach(btn => {
        btn.addEventListener('mousemove', magneticEffect);
        btn.addEventListener('mouseleave', resetMagnetic);
    });
}

function createRipple(e) {
    const button = e.currentTarget;
    const ripple = document.createElement('span');
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;

    ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${x}px;
        top: ${y}px;
        background: radial-gradient(circle, rgba(255,255,255,0.4) 0%, transparent 70%);
        border-radius: 50%;
        transform: scale(0);
        animation: rippleEffect 0.6s ease-out;
        pointer-events: none;
    `;

    button.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
}

function magneticEffect(e) {
    const btn = e.currentTarget;
    const rect = btn.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;

    btn.style.transform = `translate(${x * 0.1}px, ${y * 0.1}px)`;
}

function resetMagnetic(e) {
    e.currentTarget.style.transform = '';
}

// ==================== Interactive Elements ====================
function initializeInteractiveElements() {
    // Meal option cards
    const mealOptions = document.querySelectorAll('.meal-option');
    mealOptions.forEach(option => {
        const checkbox = option.querySelector('.meal-checkbox');
        const label = option.querySelector('.meal-label');

        if (checkbox && label) {
            label.addEventListener('click', () => {
                setTimeout(() => {
                    if (checkbox.checked) {
                        createConfetti(label);
                        label.classList.add('selected-pulse');
                        setTimeout(() => label.classList.remove('selected-pulse'), 500);
                    }
                }, 10);
            });
        }
    });

    // Gallery items hover effect
    const galleryItems = document.querySelectorAll('.gallery-container');
    galleryItems.forEach(item => {
        item.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-12px) scale(1.02) rotateX(2deg)';
        });
        item.addEventListener('mouseleave', function () {
            this.style.transform = '';
        });
    });

    // Form inputs glow effect
    const inputs = document.querySelectorAll('.form-input, .form-select, .form-textarea');
    inputs.forEach(input => {
        input.addEventListener('focus', function () {
            this.parentElement.classList.add('input-focused');
        });
        input.addEventListener('blur', function () {
            this.parentElement.classList.remove('input-focused');
        });
    });
}

// ==================== Confetti Effect ====================
function createConfetti(element) {
    const colors = ['#6366f1', '#8b5cf6', '#ec4899', '#10b981', '#f59e0b'];
    const rect = element.getBoundingClientRect();

    for (let i = 0; i < 20; i++) {
        const confetti = document.createElement('div');
        confetti.style.cssText = `
            position: fixed;
            width: 10px;
            height: 10px;
            background: ${colors[Math.floor(Math.random() * colors.length)]};
            left: ${rect.left + rect.width / 2}px;
            top: ${rect.top + rect.height / 2}px;
            border-radius: ${Math.random() > 0.5 ? '50%' : '2px'};
            pointer-events: none;
            z-index: 9999;
            animation: confettiPop 1s ease-out forwards;
            --x: ${(Math.random() - 0.5) * 200}px;
            --y: ${Math.random() * -150 - 50}px;
            --r: ${Math.random() * 720 - 360}deg;
        `;
        document.body.appendChild(confetti);
        setTimeout(() => confetti.remove(), 1000);
    }
}

// ==================== Tilt Effect ====================
function initializeTiltEffect() {
    const tiltElements = document.querySelectorAll('[data-tilt]');

    tiltElements.forEach(el => {
        el.addEventListener('mousemove', handleTilt);
        el.addEventListener('mouseleave', resetTilt);
    });
}

function handleTilt(e) {
    const el = e.currentTarget;
    const rect = el.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const rotateX = (y - centerY) / 20;
    const rotateY = (centerX - x) / 20;

    el.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
    el.style.transition = 'transform 0.1s ease-out';

    // Add glow effect based on mouse position
    const glowX = (x / rect.width) * 100;
    const glowY = (y / rect.height) * 100;
    el.style.background = `
        radial-gradient(circle at ${glowX}% ${glowY}%, rgba(99, 102, 241, 0.1) 0%, transparent 50%),
        rgba(255, 255, 255, 0.03)
    `;
}

function resetTilt(e) {
    const el = e.currentTarget;
    el.style.transform = '';
    el.style.background = '';
    el.style.transition = 'transform 0.5s ease-out, background 0.5s ease-out';
}

// ==================== Floating Particles ====================
function initializeParticles() {
    const container = document.createElement('div');
    container.className = 'particles-container';
    container.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    `;
    document.body.prepend(container);

    // Create floating particles
    for (let i = 0; i < 30; i++) {
        createParticle(container);
    }
}

function createParticle(container) {
    const particle = document.createElement('div');
    const size = Math.random() * 4 + 2;
    const duration = Math.random() * 20 + 15;
    const delay = Math.random() * 10;

    particle.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.6) 0%, transparent 70%);
        border-radius: 50%;
        left: ${Math.random() * 100}%;
        top: ${Math.random() * 100}%;
        animation: floatParticle ${duration}s linear ${delay}s infinite;
        opacity: ${Math.random() * 0.5 + 0.2};
    `;

    container.appendChild(particle);
}

// ==================== Tooltips ====================
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');

    tooltipElements.forEach(el => {
        el.addEventListener('mouseenter', showTooltip);
        el.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(e) {
    const el = e.currentTarget;
    const text = el.dataset.tooltip;

    const tooltip = document.createElement('div');
    tooltip.className = 'custom-tooltip';
    tooltip.textContent = text;
    tooltip.style.cssText = `
        position: fixed;
        background: rgba(15, 23, 42, 0.95);
        color: white;
        padding: 8px 12px;
        border-radius: 8px;
        font-size: 0.875rem;
        z-index: 10000;
        pointer-events: none;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), 0 0 20px rgba(99, 102, 241, 0.2);
        border: 1px solid rgba(99, 102, 241, 0.3);
        animation: tooltipFade 0.2s ease-out;
    `;

    document.body.appendChild(tooltip);

    const rect = el.getBoundingClientRect();
    const tooltipRect = tooltip.getBoundingClientRect();

    tooltip.style.left = `${rect.left + rect.width / 2 - tooltipRect.width / 2}px`;
    tooltip.style.top = `${rect.top - tooltipRect.height - 10}px`;

    el._tooltip = tooltip;
}

function hideTooltip(e) {
    const tooltip = e.currentTarget._tooltip;
    if (tooltip) {
        tooltip.remove();
    }
}

// ==================== Notifications ====================
function initializeNotifications() {
    window.showNotification = function (message, type = 'info') {
        const notification = document.createElement('div');
        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ'
        };

        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <span class="notification-icon">${icons[type]}</span>
            <span class="notification-message">${message}</span>
            <button class="notification-close">×</button>
        `;

        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 16px 20px;
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            color: white;
            display: flex;
            align-items: center;
            gap: 12px;
            z-index: 10001;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4), 0 0 30px rgba(99, 102, 241, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            animation: slideInRight 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
            max-width: 400px;
        `;

        const colors = {
            success: '#10b981',
            error: '#ef4444',
            warning: '#f59e0b',
            info: '#6366f1'
        };

        notification.style.borderLeftColor = colors[type];
        notification.style.borderLeftWidth = '4px';
        notification.style.borderLeftStyle = 'solid';

        document.body.appendChild(notification);

        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => {
            notification.style.animation = 'slideOutRight 0.3s ease-out forwards';
            setTimeout(() => notification.remove(), 300);
        });

        setTimeout(() => {
            if (notification.parentElement) {
                notification.style.animation = 'slideOutRight 0.3s ease-out forwards';
                setTimeout(() => notification.remove(), 300);
            }
        }, 5000);
    };
}

// ==================== Form Submission Handler ====================
document.addEventListener('submit', function (e) {
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');

    if (submitBtn && !submitBtn.classList.contains('no-loading')) {
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = `
            <span class="loading-spinner"></span>
            Processing...
        `;
        submitBtn.disabled = true;

        // Re-enable after form processes (fallback)
        setTimeout(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }, 5000);
    }
});

// ==================== Dynamic Styles ====================
const dynamicStyles = document.createElement('style');
dynamicStyles.textContent = `
    @keyframes rippleEffect {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    @keyframes confettiPop {
        0% {
            transform: translate(0, 0) rotate(0deg) scale(1);
            opacity: 1;
        }
        100% {
            transform: translate(var(--x), var(--y)) rotate(var(--r)) scale(0);
            opacity: 0;
        }
    }
    
    @keyframes floatParticle {
        0%, 100% {
            transform: translate(0, 0) rotate(0deg);
        }
        25% {
            transform: translate(50px, -50px) rotate(90deg);
        }
        50% {
            transform: translate(0, -100px) rotate(180deg);
        }
        75% {
            transform: translate(-50px, -50px) rotate(270deg);
        }
    }
    
    @keyframes tooltipFade {
        from {
            opacity: 0;
            transform: translateY(5px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOutRight {
        to {
            opacity: 0;
            transform: translateX(100px);
        }
    }
    
    .navbar-scrolled {
        background: rgba(15, 23, 42, 0.98) !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4), 0 0 30px rgba(99, 102, 241, 0.2);
    }
    
    .input-focused {
        position: relative;
    }
    
    .input-focused::after {
        content: '';
        position: absolute;
        inset: -2px;
        border-radius: 14px;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        z-index: -1;
        opacity: 0.3;
        filter: blur(8px);
        animation: pulseGlow 1.5s ease-in-out infinite;
    }
    
    @keyframes pulseGlow {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 0.6; }
    }
    
    .selected-pulse {
        animation: selectedPulse 0.5s ease-out !important;
    }
    
    @keyframes selectedPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .loading-spinner {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-top-color: white;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    .notification-icon {
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        font-size: 14px;
        font-weight: bold;
    }
    
    .notification-success .notification-icon { background: rgba(16, 185, 129, 0.2); color: #10b981; }
    .notification-error .notification-icon { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
    .notification-warning .notification-icon { background: rgba(245, 158, 11, 0.2); color: #f59e0b; }
    .notification-info .notification-icon { background: rgba(99, 102, 241, 0.2); color: #6366f1; }
    
    .notification-close {
        background: none;
        border: none;
        color: rgba(255, 255, 255, 0.5);
        font-size: 20px;
        cursor: pointer;
        padding: 0 4px;
        margin-left: auto;
        transition: color 0.2s;
    }
    
    .notification-close:hover {
        color: white;
    }
    
    /* Glow effect on page margins */
    body::before {
        box-shadow: 
            inset 0 0 100px rgba(99, 102, 241, 0.1),
            inset 0 0 200px rgba(139, 92, 246, 0.05);
    }
`;
document.head.appendChild(dynamicStyles);

// ==================== Smooth Scroll ====================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// ==================== Keyboard Navigation ====================
document.addEventListener('keydown', function (e) {
    // ESC to close modals/notifications
    if (e.key === 'Escape') {
        document.querySelectorAll('.notification').forEach(n => n.remove());
    }
});

console.log('🏨 Smart Hostel Management System Initialized');
console.log('✨ Premium UI Effects Active');
