/**
 * Smart Hostel Management System
 * Premium Interactive JavaScript with Theme Toggle
 */

// ==================== DOM Ready ====================
document.addEventListener('DOMContentLoaded', function () {
    initializeTheme();
    initializeThemeToggle();
    initializePage();
    initializeAnimations();
    initializeInteractiveElements();
    initializeParticles();
    initializeScrollEffects();
    initializeTiltEffect();
    initializeTooltips();
    initializeNotifications();
    initializeCounters();
    initializeLazyLoading();
    initializeFormValidation();
    initializeSmoothScroll();
    initializeKeyboardNavigation();

    console.log('🏨 Smart Hostel Management System Initialized');
    console.log('✨ Premium UI Effects Active');
    console.log('🌙 Theme System Ready');
});

// ==================== Theme Management ====================
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeColors(savedTheme);
}

function initializeThemeToggle() {
    // Create theme toggle button
    const toggleBtn = document.createElement('button');
    toggleBtn.className = 'theme-toggle';
    toggleBtn.setAttribute('aria-label', 'Toggle theme');
    toggleBtn.innerHTML = `
        <span class="icon-sun">☀️</span>
        <span class="icon-moon">🌙</span>
    `;
    document.body.appendChild(toggleBtn);

    toggleBtn.addEventListener('click', toggleTheme);

    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            const theme = e.matches ? 'dark' : 'light';
            setTheme(theme);
        }
    });
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);

    // Add rotation animation
    const toggle = document.querySelector('.theme-toggle');
    toggle.style.transform = 'scale(1.2) rotate(360deg)';
    setTimeout(() => {
        toggle.style.transform = '';
    }, 500);

    showNotification(`Switched to ${newTheme} mode`, 'info');
}

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    updateThemeColors(theme);

    // Dispatch custom event for other components
    window.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));
}

function updateThemeColors(theme) {
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
        metaThemeColor.content = theme === 'dark' ? '#0f172a' : '#f8fafc';
    }
}

// ==================== Page Initialization ====================
function initializePage() {
    // Add loading complete class
    document.body.classList.add('loaded');

    // Stagger animation for cards
    const cards = document.querySelectorAll('.glass-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';

        setTimeout(() => {
            card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });

    // Add hover sound effect (optional)
    addHoverSounds();
}

function addHoverSounds() {
    // Optional: Add subtle hover sounds for interactive elements
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            // Could add audio feedback here
        });
    });
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
            // Add completion effect
            element.classList.add('counter-complete');
        }
        element.textContent = Math.floor(current).toLocaleString();
    }, 16);
}

// ==================== Scroll Effects ====================
function initializeScrollEffects() {
    // Navbar background on scroll
    const navbar = document.querySelector('.navbar');
    let lastScroll = 0;

    if (navbar) {
        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;

            // Add/remove scrolled class
            if (currentScroll > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }

            // Hide/show navbar on scroll direction
            if (currentScroll > lastScroll && currentScroll > 200) {
                navbar.style.transform = 'translateY(-100%)';
            } else {
                navbar.style.transform = 'translateY(0)';
            }

            lastScroll = currentScroll;
        });
    }

    // Reveal elements on scroll
    const revealElements = document.querySelectorAll('.glass-card, .gallery-item, .status-item, [data-reveal]');

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
        if (!el.classList.contains('loaded')) {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            revealObserver.observe(el);
        }
    });

    // Parallax effect for background
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        document.body.style.backgroundPositionY = `${scrolled * 0.3}px`;
    });

    // Progress indicator
    createScrollProgress();
}

function createScrollProgress() {
    const progress = document.createElement('div');
    progress.className = 'scroll-progress';
    progress.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary), var(--secondary), var(--accent));
        z-index: 9999;
        transition: width 0.1s ease-out;
        width: 0%;
    `;
    document.body.appendChild(progress);

    window.addEventListener('scroll', () => {
        const winScroll = document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        progress.style.width = scrolled + '%';
    });
}

// ==================== Interactive Animations ====================
function initializeAnimations() {
    // Ripple effect on buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', createRipple);
        btn.addEventListener('mouseenter', createGlowEffect);
    });

    // Magnetic effect on buttons
    buttons.forEach(btn => {
        btn.addEventListener('mousemove', magneticEffect);
        btn.addEventListener('mouseleave', resetMagnetic);
    });

    // Add pulse animation to important elements
    document.querySelectorAll('.badge-primary, .badge-success').forEach(el => {
        el.style.animation = 'pulse 2s ease-in-out infinite';
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
        background: radial-gradient(circle, rgba(255,255,255,0.5) 0%, transparent 70%);
        border-radius: 50%;
        transform: scale(0);
        animation: rippleEffect 0.6s ease-out forwards;
        pointer-events: none;
    `;

    button.style.position = 'relative';
    button.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
}

function createGlowEffect(e) {
    const button = e.currentTarget;
    const glow = document.createElement('span');

    glow.style.cssText = `
        position: absolute;
        inset: -2px;
        background: inherit;
        border-radius: inherit;
        filter: blur(15px);
        opacity: 0;
        z-index: -1;
        animation: glowPulse 0.3s ease-out forwards;
    `;

    button.style.position = 'relative';
    button.appendChild(glow);

    button.addEventListener('mouseleave', () => glow.remove(), { once: true });
}

function magneticEffect(e) {
    const btn = e.currentTarget;
    const rect = btn.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;

    btn.style.transform = `translate(${x * 0.15}px, ${y * 0.15}px)`;
}

function resetMagnetic(e) {
    e.currentTarget.style.transform = '';
}

// ==================== Interactive Elements ====================
function initializeInteractiveElements() {
    // Meal option cards with confetti
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
                        vibrate(50); // Haptic feedback
                        setTimeout(() => label.classList.remove('selected-pulse'), 500);
                    }
                }, 10);
            });
        }
    });

    // Gallery items hover effect
    const galleryItems = document.querySelectorAll('.gallery-container');
    galleryItems.forEach(item => {
        item.addEventListener('mouseenter', function (e) {
            this.style.transform = 'translateY(-12px) scale(1.02)';
            createSparkles(this);
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

        // Real-time validation feedback
        input.addEventListener('input', function () {
            if (this.validity.valid) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            } else {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            }
        });
    });

    // Card hover 3D effect
    document.querySelectorAll('.glass-card').forEach(card => {
        card.addEventListener('mousemove', handle3DEffect);
        card.addEventListener('mouseleave', reset3DEffect);
    });
}

function handle3DEffect(e) {
    const card = e.currentTarget;
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const rotateX = (y - centerY) / 30;
    const rotateY = (centerX - x) / 30;

    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px) scale(1.02)`;
}

function reset3DEffect(e) {
    e.currentTarget.style.transform = '';
}

function vibrate(duration) {
    if ('vibrate' in navigator) {
        navigator.vibrate(duration);
    }
}

// ==================== Sparkle Effect ====================
function createSparkles(element) {
    const rect = element.getBoundingClientRect();

    for (let i = 0; i < 5; i++) {
        const sparkle = document.createElement('div');
        sparkle.className = 'sparkle';
        sparkle.style.cssText = `
            position: fixed;
            width: 6px;
            height: 6px;
            background: white;
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            left: ${rect.left + Math.random() * rect.width}px;
            top: ${rect.top + Math.random() * rect.height}px;
            animation: sparkle 0.6s ease-out forwards;
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
        `;
        document.body.appendChild(sparkle);
        setTimeout(() => sparkle.remove(), 600);
    }
}

// ==================== Confetti Effect ====================
function createConfetti(element) {
    const colors = ['#6366f1', '#8b5cf6', '#ec4899', '#10b981', '#f59e0b', '#06b6d4'];
    const rect = element.getBoundingClientRect();

    for (let i = 0; i < 30; i++) {
        const confetti = document.createElement('div');
        const size = Math.random() * 8 + 4;

        confetti.style.cssText = `
            position: fixed;
            width: ${size}px;
            height: ${size}px;
            background: ${colors[Math.floor(Math.random() * colors.length)]};
            left: ${rect.left + rect.width / 2}px;
            top: ${rect.top + rect.height / 2}px;
            border-radius: ${Math.random() > 0.5 ? '50%' : '2px'};
            pointer-events: none;
            z-index: 9999;
            animation: confettiPop 1s ease-out forwards;
            --x: ${(Math.random() - 0.5) * 300}px;
            --y: ${Math.random() * -200 - 50}px;
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
        radial-gradient(circle at ${glowX}% ${glowY}%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
        var(--glass-bg)
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
    for (let i = 0; i < 40; i++) {
        createParticle(container);
    }

    // Create connecting lines effect
    createParticleConnections(container);
}

function createParticle(container) {
    const particle = document.createElement('div');
    const size = Math.random() * 4 + 2;
    const duration = Math.random() * 25 + 15;
    const delay = Math.random() * 10;
    const hue = Math.random() * 60 + 230; // Purple to blue range

    particle.className = 'floating-particle';
    particle.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        background: radial-gradient(circle, hsla(${hue}, 70%, 60%, 0.8) 0%, transparent 70%);
        border-radius: 50%;
        left: ${Math.random() * 100}%;
        top: ${Math.random() * 100}%;
        animation: floatParticle ${duration}s linear ${delay}s infinite;
        opacity: ${Math.random() * 0.6 + 0.2};
        box-shadow: 0 0 ${size * 2}px hsla(${hue}, 70%, 60%, 0.3);
    `;

    container.appendChild(particle);
}

function createParticleConnections(container) {
    // SVG for connecting lines
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.style.cssText = `
        position: absolute;
        width: 100%;
        height: 100%;
        pointer-events: none;
    `;
    svg.innerHTML = `
        <defs>
            <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:rgba(99,102,241,0.2)"/>
                <stop offset="50%" style="stop-color:rgba(139,92,246,0.3)"/>
                <stop offset="100%" style="stop-color:rgba(99,102,241,0.2)"/>
            </linearGradient>
        </defs>
    `;
    container.appendChild(svg);
}

// ==================== Tooltips ====================
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');

    tooltipElements.forEach(el => {
        el.addEventListener('mouseenter', showTooltip);
        el.addEventListener('mouseleave', hideTooltip);
        el.addEventListener('focus', showTooltip);
        el.addEventListener('blur', hideTooltip);
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
        background: var(--bg-darker);
        color: var(--text-primary);
        padding: 10px 16px;
        border-radius: 8px;
        font-size: 0.875rem;
        z-index: 10000;
        pointer-events: none;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3), 0 0 20px rgba(99, 102, 241, 0.2);
        border: 1px solid var(--glass-border);
        animation: tooltipFade 0.2s ease-out;
        max-width: 250px;
        text-align: center;
    `;

    document.body.appendChild(tooltip);

    const rect = el.getBoundingClientRect();
    const tooltipRect = tooltip.getBoundingClientRect();

    let left = rect.left + rect.width / 2 - tooltipRect.width / 2;
    let top = rect.top - tooltipRect.height - 12;

    // Keep tooltip in viewport
    if (left < 10) left = 10;
    if (left + tooltipRect.width > window.innerWidth - 10) {
        left = window.innerWidth - tooltipRect.width - 10;
    }
    if (top < 10) {
        top = rect.bottom + 12;
    }

    tooltip.style.left = `${left}px`;
    tooltip.style.top = `${top}px`;

    el._tooltip = tooltip;
}

function hideTooltip(e) {
    const tooltip = e.currentTarget._tooltip;
    if (tooltip) {
        tooltip.style.animation = 'tooltipFadeOut 0.15s ease-out forwards';
        setTimeout(() => tooltip.remove(), 150);
    }
}

// ==================== Notifications ====================
function initializeNotifications() {
    window.showNotification = function (message, type = 'info', duration = 5000) {
        const container = getNotificationContainer();
        const notification = document.createElement('div');
        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ'
        };

        const colors = {
            success: 'var(--success)',
            error: 'var(--danger)',
            warning: 'var(--warning)',
            info: 'var(--primary)'
        };

        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <span class="notification-icon" style="background: ${colors[type]}20; color: ${colors[type]}">
                ${icons[type]}
            </span>
            <span class="notification-message">${message}</span>
            <button class="notification-close" aria-label="Close notification">×</button>
            <div class="notification-progress" style="background: ${colors[type]}"></div>
        `;

        notification.style.cssText = `
            padding: 16px 20px;
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border-radius: 12px;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 12px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3), 0 0 30px rgba(99, 102, 241, 0.2);
            border: 1px solid var(--glass-border);
            border-left: 4px solid ${colors[type]};
            animation: slideInRight 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
            margin-bottom: 10px;
            position: relative;
            overflow: hidden;
        `;

        container.appendChild(notification);

        // Progress bar animation
        const progress = notification.querySelector('.notification-progress');
        progress.style.cssText = `
            position: absolute;
            bottom: 0;
            left: 0;
            height: 3px;
            width: 100%;
            transform-origin: left;
            animation: progressShrink ${duration}ms linear forwards;
        `;

        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.style.cssText = `
            background: none;
            border: none;
            color: var(--text-muted);
            font-size: 20px;
            cursor: pointer;
            padding: 0 4px;
            margin-left: auto;
            transition: color 0.2s, transform 0.2s;
        `;

        closeBtn.addEventListener('mouseenter', () => {
            closeBtn.style.color = 'var(--text-primary)';
            closeBtn.style.transform = 'scale(1.2)';
        });

        closeBtn.addEventListener('mouseleave', () => {
            closeBtn.style.color = 'var(--text-muted)';
            closeBtn.style.transform = '';
        });

        const closeNotification = () => {
            notification.style.animation = 'slideOutRight 0.3s ease-out forwards';
            setTimeout(() => notification.remove(), 300);
        };

        closeBtn.addEventListener('click', closeNotification);

        setTimeout(closeNotification, duration);

        return notification;
    };
}

function getNotificationContainer() {
    let container = document.querySelector('.notification-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'notification-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10001;
            display: flex;
            flex-direction: column;
            max-width: 400px;
        `;
        document.body.appendChild(container);
    }
    return container;
}

// ==================== Form Validation ====================
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            if (!form.checkValidity()) {
                e.preventDefault();

                // Shake invalid fields
                form.querySelectorAll(':invalid').forEach(field => {
                    field.style.animation = 'shake 0.5s ease-out';
                    setTimeout(() => field.style.animation = '', 500);
                });

                showNotification('Please fill in all required fields', 'error');
                return;
            }

            // Add loading state
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.classList.contains('no-loading')) {
                const originalContent = submitBtn.innerHTML;
                submitBtn.innerHTML = `
                    <span class="loading-spinner"></span>
                    Processing...
                `;
                submitBtn.disabled = true;

                // Fallback reset
                setTimeout(() => {
                    submitBtn.innerHTML = originalContent;
                    submitBtn.disabled = false;
                }, 10000);
            }
        });
    });
}

// ==================== Lazy Loading ====================
function initializeLazyLoading() {
    const lazyImages = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('lazy-loaded');
                imageObserver.unobserve(img);
            }
        });
    }, { rootMargin: '50px' });

    lazyImages.forEach(img => {
        img.classList.add('lazy-loading');
        imageObserver.observe(img);
    });
}

// ==================== Smooth Scroll ====================
function initializeSmoothScroll() {
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

                    // Update URL without jumping
                    history.pushState(null, null, href);
                }
            }
        });
    });
}

// ==================== Keyboard Navigation ====================
function initializeKeyboardNavigation() {
    // ESC to close modals/notifications
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            document.querySelectorAll('.notification').forEach(n => {
                n.style.animation = 'slideOutRight 0.3s ease-out forwards';
                setTimeout(() => n.remove(), 300);
            });
        }

        // Theme toggle with keyboard (Ctrl/Cmd + Shift + T)
        if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'T') {
            e.preventDefault();
            toggleTheme();
        }
    });

    // Tab focus improvements
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-nav');
        }
    });

    document.addEventListener('mousedown', () => {
        document.body.classList.remove('keyboard-nav');
    });
}

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
    
    @keyframes tooltipFadeOut {
        to {
            opacity: 0;
            transform: translateY(-5px);
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
    
    @keyframes progressShrink {
        from { transform: scaleX(1); }
        to { transform: scaleX(0); }
    }
    
    @keyframes sparkle {
        0% {
            transform: scale(0) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: scale(1.5) rotate(180deg);
            opacity: 0;
        }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        20% { transform: translateX(-10px); }
        40% { transform: translateX(10px); }
        60% { transform: translateX(-10px); }
        80% { transform: translateX(10px); }
    }
    
    @keyframes glowPulse {
        from { opacity: 0; }
        to { opacity: 0.5; }
    }
    
    .navbar-scrolled {
        background: var(--navbar-bg) !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3), 0 0 30px rgba(99, 102, 241, 0.2);
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
        width: 18px;
        height: 18px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-top-color: white;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    .notification-icon {
        width: 28px;
        height: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        font-size: 14px;
        font-weight: bold;
        flex-shrink: 0;
    }
    
    .notification-message {
        flex: 1;
        font-size: 0.95rem;
    }
    
    .lazy-loading {
        opacity: 0;
        transition: opacity 0.3s ease-out;
    }
    
    .lazy-loaded {
        opacity: 1;
    }
    
    .counter-complete {
        animation: counterPop 0.3s ease-out;
    }
    
    @keyframes counterPop {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
    
    .keyboard-nav *:focus {
        outline: 2px solid var(--primary) !important;
        outline-offset: 2px !important;
    }
    
    .is-valid {
        border-color: var(--success) !important;
    }
    
    .is-invalid {
        border-color: var(--danger) !important;
    }
    
    /* Theme toggle button styles */
    .theme-toggle .icon-sun,
    .theme-toggle .icon-moon {
        position: absolute;
        font-size: 1.5rem;
        transition: all 0.3s ease;
    }
    
    /* Scroll progress */
    .scroll-progress {
        box-shadow: 0 0 10px var(--primary);
    }
`;
document.head.appendChild(dynamicStyles);

// ==================== Utility Functions ====================
window.utils = {
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

    throttle(func, limit) {
        let inThrottle;
        return function (...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },

    formatNumber(num) {
        return new Intl.NumberFormat().format(num);
    },

    formatDate(date) {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(new Date(date));
    },

    copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Copied to clipboard!', 'success');
        }).catch(() => {
            showNotification('Failed to copy', 'error');
        });
    }
};
