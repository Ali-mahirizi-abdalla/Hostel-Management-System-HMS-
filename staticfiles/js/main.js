/**
 * Smart Hostel Management System
 * Premium Interactive JavaScript with 3D Effects & Glowing UI
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

    // New 3D & Glow Effects
    initializeGlowingBorders();
    initializeAuroraEffect();
    initialize3DShapes();
    initializeMouseTrail();
    initializeMagneticCursor();
    initializeParallaxDepth();
    initializeNeonText();
    initializeHolographicCards();
    initializeElectricSparks();

    console.log('🏨 Smart Hostel Management System Initialized');
    console.log('✨ Premium 3D UI Effects Active');
    console.log('🌙 Theme System Ready');
    console.log('⚡ Glowing Borders Active');
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

    // Initialize sound system
    initializeSoundSystem();
}

// ==================== SOUND & HAPTIC FEEDBACK SYSTEM ====================
let audioContext = null;
let soundEnabled = true;

function initializeSoundSystem() {
    // Create audio context on first user interaction
    const initAudio = () => {
        if (!audioContext) {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            console.log('🔊 Sound System Initialized');
        }
        document.removeEventListener('click', initAudio);
        document.removeEventListener('touchstart', initAudio);
    };

    document.addEventListener('click', initAudio);
    document.addEventListener('touchstart', initAudio);

    // Add sound toggle button
    createSoundToggle();

    // Attach sounds to elements
    attachSoundEffects();
}

function createSoundToggle() {
    const toggle = document.createElement('button');
    toggle.className = 'sound-toggle';
    toggle.setAttribute('aria-label', 'Toggle sound effects');
    toggle.innerHTML = `<span class="sound-on">🔊</span><span class="sound-off">🔇</span>`;
    toggle.style.cssText = `
        position: fixed;
        bottom: 100px;
        right: 30px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
        z-index: 999;
        transition: all 0.3s ease;
    `;

    toggle.querySelector('.sound-off').style.display = 'none';

    toggle.addEventListener('click', () => {
        soundEnabled = !soundEnabled;
        toggle.querySelector('.sound-on').style.display = soundEnabled ? 'block' : 'none';
        toggle.querySelector('.sound-off').style.display = soundEnabled ? 'none' : 'block';

        if (soundEnabled) {
            playSound('toggle', 800, 0.1, 'sine');
            hapticFeedback('light');
        }

        showNotification(soundEnabled ? 'Sound enabled' : 'Sound disabled', 'info', 2000);
    });

    toggle.addEventListener('mouseenter', () => {
        toggle.style.transform = 'scale(1.1)';
    });

    toggle.addEventListener('mouseleave', () => {
        toggle.style.transform = '';
    });

    document.body.appendChild(toggle);
}

function attachSoundEffects() {
    // Button hover sounds
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            playSound('hover', 600, 0.05, 'sine');
            hapticFeedback('light');
        });

        btn.addEventListener('click', () => {
            if (btn.classList.contains('btn-primary')) {
                playSound('click', 400, 0.15, 'square');
            } else if (btn.classList.contains('btn-success')) {
                playSound('success', 523.25, 0.1, 'sine'); // C5
                setTimeout(() => playSound('success', 659.25, 0.1, 'sine'), 100); // E5
                setTimeout(() => playSound('success', 783.99, 0.1, 'sine'), 200); // G5
            } else {
                playSound('click', 300, 0.1, 'triangle');
            }
            hapticFeedback('medium');
        });
    });

    // Navigation links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('mouseenter', () => {
            playSound('hover', 500, 0.03, 'sine');
        });

        link.addEventListener('click', () => {
            playSound('navigate', 350, 0.08, 'triangle');
            hapticFeedback('light');
        });
    });

    // Meal option selections
    document.querySelectorAll('.meal-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            if (checkbox.checked) {
                // Success sound - ascending notes
                playSound('select', 440, 0.1, 'sine');
                setTimeout(() => playSound('select', 554.37, 0.1, 'sine'), 80);
                setTimeout(() => playSound('select', 659.25, 0.12, 'sine'), 160);
                hapticFeedback('success');
            } else {
                // Deselect sound - descending note
                playSound('deselect', 350, 0.08, 'triangle');
                hapticFeedback('light');
            }
        });
    });

    // Card hover sounds
    document.querySelectorAll('.glass-card').forEach(card => {
        card.addEventListener('mouseenter', () => {
            playSound('cardHover', 200, 0.02, 'sine');
        });
    });

    // Gallery item sounds
    document.querySelectorAll('.gallery-container').forEach(item => {
        item.addEventListener('mouseenter', () => {
            playSound('gallery', 450, 0.05, 'sine');
            hapticFeedback('light');
        });
    });

    // Form input sounds
    document.querySelectorAll('.form-input, .form-select, .form-textarea').forEach(input => {
        input.addEventListener('focus', () => {
            playSound('focus', 550, 0.04, 'sine');
        });

        input.addEventListener('input', utils.debounce(() => {
            playSound('type', 800 + Math.random() * 200, 0.02, 'sine');
        }, 50));
    });

    // Checkbox/toggle sounds
    document.querySelectorAll('.form-check-input').forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            if (checkbox.checked) {
                playSound('check', 600, 0.08, 'sine');
                setTimeout(() => playSound('check', 800, 0.06, 'sine'), 100);
            } else {
                playSound('uncheck', 400, 0.06, 'triangle');
            }
            hapticFeedback('light');
        });
    });
}

// Core sound generation using Web Audio API
function playSound(type, frequency = 440, volume = 0.1, waveType = 'sine') {
    if (!soundEnabled || !audioContext) return;

    try {
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);

        oscillator.type = waveType;
        oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime);

        // Volume envelope
        gainNode.gain.setValueAtTime(0, audioContext.currentTime);
        gainNode.gain.linearRampToValueAtTime(volume, audioContext.currentTime + 0.01);
        gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.15);

        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.15);
    } catch (e) {
        console.log('Sound play error:', e);
    }
}

// Play a musical chord
function playChord(frequencies, volume = 0.08, duration = 0.3) {
    if (!soundEnabled || !audioContext) return;

    frequencies.forEach((freq, index) => {
        setTimeout(() => {
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.type = 'sine';
            oscillator.frequency.setValueAtTime(freq, audioContext.currentTime);

            gainNode.gain.setValueAtTime(0, audioContext.currentTime);
            gainNode.gain.linearRampToValueAtTime(volume, audioContext.currentTime + 0.02);
            gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + duration);

            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + duration);
        }, index * 50);
    });
}

// Notification sounds
function playNotificationSound(type) {
    if (!soundEnabled || !audioContext) return;

    switch (type) {
        case 'success':
            playChord([523.25, 659.25, 783.99], 0.1, 0.4); // C Major
            break;
        case 'error':
            playSound('error', 200, 0.15, 'sawtooth');
            setTimeout(() => playSound('error', 150, 0.12, 'sawtooth'), 150);
            break;
        case 'warning':
            playSound('warning', 400, 0.1, 'triangle');
            setTimeout(() => playSound('warning', 350, 0.08, 'triangle'), 200);
            break;
        case 'info':
            playChord([440, 554.37], 0.06, 0.2);
            break;
    }
}

// Haptic feedback for mobile devices
function hapticFeedback(type = 'light') {
    if (!('vibrate' in navigator)) return;

    const patterns = {
        light: [10],
        medium: [20],
        heavy: [30],
        success: [10, 50, 10, 50, 30],
        error: [50, 30, 50],
        warning: [30, 20, 30],
        double: [15, 50, 15],
        triple: [10, 30, 10, 30, 10]
    };

    try {
        navigator.vibrate(patterns[type] || patterns.light);
    } catch (e) {
        // Vibration not supported
    }
}

// Enhanced notification with sound
const originalShowNotification = window.showNotification;
window.showNotification = function (message, type = 'info', duration = 5000) {
    playNotificationSound(type);
    hapticFeedback(type === 'success' ? 'success' : type === 'error' ? 'error' : 'light');

    if (originalShowNotification) {
        return originalShowNotification(message, type, duration);
    }
};

function addHoverSounds() {
    // Legacy function - now handled by attachSoundEffects()
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

// ==================== GLOWING MARGIN BORDERS ====================
function initializeGlowingBorders() {
    const borders = ['left', 'right', 'top', 'bottom'];

    borders.forEach(position => {
        const border = document.createElement('div');
        border.className = `glow-border-${position}`;
        document.body.appendChild(border);
    });

    // Add corner glow orbs
    const corners = ['top-left', 'top-right', 'bottom-left', 'bottom-right'];
    corners.forEach(corner => {
        const orb = document.createElement('div');
        orb.className = `corner-glow ${corner}`;
        document.body.appendChild(orb);
    });
}

// ==================== AURORA EFFECT ====================
function initializeAuroraEffect() {
    const aurora = document.createElement('div');
    aurora.className = 'aurora';

    for (let i = 0; i < 3; i++) {
        const layer = document.createElement('div');
        layer.className = 'aurora-layer';
        aurora.appendChild(layer);
    }

    document.body.prepend(aurora);
}

// ==================== 3D FLOATING SHAPES ====================
function initialize3DShapes() {
    const container = document.createElement('div');
    container.className = 'floating-shapes-container';
    container.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        perspective: 1000px;
        overflow: hidden;
    `;
    document.body.prepend(container);

    // Create multiple 3D shapes
    const shapes = [
        { type: 'cube', count: 3 },
        { type: 'pyramid', count: 2 },
        { type: 'ring', count: 4 },
        { type: 'orb', count: 5 }
    ];

    shapes.forEach(({ type, count }) => {
        for (let i = 0; i < count; i++) {
            create3DShape(container, type, i);
        }
    });
}

function create3DShape(container, type, index) {
    const shape = document.createElement('div');
    const size = Math.random() * 40 + 20;
    const x = Math.random() * 100;
    const y = Math.random() * 100;
    const duration = Math.random() * 30 + 20;
    const delay = Math.random() * 10;
    const hue = Math.random() * 60 + 220; // Purple to blue

    shape.className = `floating-3d-shape shape-${type}`;

    if (type === 'cube') {
        shape.style.cssText = `
            position: absolute;
            left: ${x}%;
            top: ${y}%;
            width: ${size}px;
            height: ${size}px;
            transform-style: preserve-3d;
            animation: float3DRotate ${duration}s linear infinite;
            animation-delay: -${delay}s;
        `;
        shape.innerHTML = `
            <div style="position: absolute; width: 100%; height: 100%; background: linear-gradient(135deg, hsla(${hue}, 70%, 60%, 0.15), transparent); border: 1px solid hsla(${hue}, 70%, 60%, 0.3); transform: translateZ(${size / 2}px); backdrop-filter: blur(2px);"></div>
            <div style="position: absolute; width: 100%; height: 100%; background: linear-gradient(135deg, hsla(${hue}, 70%, 60%, 0.1), transparent); border: 1px solid hsla(${hue}, 70%, 60%, 0.2); transform: rotateY(180deg) translateZ(${size / 2}px);"></div>
            <div style="position: absolute; width: 100%; height: 100%; background: linear-gradient(135deg, hsla(${hue}, 70%, 60%, 0.1), transparent); border: 1px solid hsla(${hue}, 70%, 60%, 0.2); transform: rotateY(90deg) translateZ(${size / 2}px);"></div>
            <div style="position: absolute; width: 100%; height: 100%; background: linear-gradient(135deg, hsla(${hue}, 70%, 60%, 0.1), transparent); border: 1px solid hsla(${hue}, 70%, 60%, 0.2); transform: rotateY(-90deg) translateZ(${size / 2}px);"></div>
            <div style="position: absolute; width: 100%; height: 100%; background: linear-gradient(135deg, hsla(${hue}, 70%, 60%, 0.1), transparent); border: 1px solid hsla(${hue}, 70%, 60%, 0.2); transform: rotateX(90deg) translateZ(${size / 2}px);"></div>
            <div style="position: absolute; width: 100%; height: 100%; background: linear-gradient(135deg, hsla(${hue}, 70%, 60%, 0.1), transparent); border: 1px solid hsla(${hue}, 70%, 60%, 0.2); transform: rotateX(-90deg) translateZ(${size / 2}px);"></div>
        `;
    } else if (type === 'ring') {
        shape.style.cssText = `
            position: absolute;
            left: ${x}%;
            top: ${y}%;
            width: ${size * 1.5}px;
            height: ${size * 1.5}px;
            border: 2px solid hsla(${hue}, 70%, 60%, 0.3);
            border-radius: 50%;
            animation: ringFloat ${duration}s ease-in-out infinite, ringSpin ${duration * 0.5}s linear infinite;
            animation-delay: -${delay}s;
            box-shadow: 0 0 20px hsla(${hue}, 70%, 60%, 0.2), inset 0 0 20px hsla(${hue}, 70%, 60%, 0.1);
        `;
    } else if (type === 'orb') {
        shape.style.cssText = `
            position: absolute;
            left: ${x}%;
            top: ${y}%;
            width: ${size}px;
            height: ${size}px;
            background: radial-gradient(circle at 30% 30%, hsla(${hue}, 70%, 70%, 0.4), hsla(${hue}, 70%, 40%, 0.1), transparent);
            border-radius: 50%;
            animation: orbFloat ${duration}s ease-in-out infinite;
            animation-delay: -${delay}s;
            box-shadow: 0 0 ${size}px hsla(${hue}, 70%, 60%, 0.3);
            filter: blur(1px);
        `;
    } else if (type === 'pyramid') {
        shape.style.cssText = `
            position: absolute;
            left: ${x}%;
            top: ${y}%;
            width: 0;
            height: 0;
            border-left: ${size / 2}px solid transparent;
            border-right: ${size / 2}px solid transparent;
            border-bottom: ${size}px solid hsla(${hue}, 70%, 60%, 0.2);
            animation: pyramidFloat ${duration}s ease-in-out infinite;
            animation-delay: -${delay}s;
            filter: drop-shadow(0 0 10px hsla(${hue}, 70%, 60%, 0.3));
        `;
    }

    container.appendChild(shape);
}

// ==================== MOUSE TRAIL EFFECT ====================
function initializeMouseTrail() {
    const trail = [];
    const trailLength = 20;

    for (let i = 0; i < trailLength; i++) {
        const dot = document.createElement('div');
        dot.className = 'mouse-trail-dot';
        dot.style.cssText = `
            position: fixed;
            width: ${12 - i * 0.5}px;
            height: ${12 - i * 0.5}px;
            background: radial-gradient(circle, rgba(99, 102, 241, ${0.8 - i * 0.04}), rgba(139, 92, 246, ${0.4 - i * 0.02}));
            border-radius: 50%;
            pointer-events: none;
            z-index: 9997;
            transition: transform 0.1s ease;
            opacity: 0;
            box-shadow: 0 0 ${10 - i * 0.3}px rgba(99, 102, 241, 0.5);
        `;
        document.body.appendChild(dot);
        trail.push({ element: dot, x: 0, y: 0 });
    }

    let mouseX = 0, mouseY = 0;
    let isMoving = false;
    let moveTimeout;

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        isMoving = true;

        trail.forEach(dot => dot.element.style.opacity = '1');

        clearTimeout(moveTimeout);
        moveTimeout = setTimeout(() => {
            isMoving = false;
            trail.forEach(dot => dot.element.style.opacity = '0');
        }, 200);
    });

    function animateTrail() {
        let x = mouseX;
        let y = mouseY;

        trail.forEach((dot, index) => {
            const nextX = x;
            const nextY = y;

            dot.element.style.left = `${dot.x}px`;
            dot.element.style.top = `${dot.y}px`;

            dot.x += (nextX - dot.x) * (0.35 - index * 0.01);
            dot.y += (nextY - dot.y) * (0.35 - index * 0.01);

            x = dot.x;
            y = dot.y;
        });

        requestAnimationFrame(animateTrail);
    }

    animateTrail();
}

// ==================== MAGNETIC CURSOR EFFECT ====================
function initializeMagneticCursor() {
    const magneticElements = document.querySelectorAll('.btn, .glass-card, .nav-link, .meal-label');

    magneticElements.forEach(el => {
        el.addEventListener('mousemove', (e) => {
            const rect = el.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;

            el.style.transform = `translate(${x * 0.1}px, ${y * 0.1}px) scale(1.02)`;
            el.style.boxShadow = `
                ${-x * 0.05}px ${-y * 0.05}px 30px rgba(99, 102, 241, 0.3),
                ${x * 0.05}px ${y * 0.05}px 30px rgba(139, 92, 246, 0.3)
            `;
        });

        el.addEventListener('mouseleave', () => {
            el.style.transform = '';
            el.style.boxShadow = '';
        });
    });
}

// ==================== PARALLAX DEPTH EFFECT ====================
function initializeParallaxDepth() {
    const depthElements = document.querySelectorAll('.glass-card, .gallery-container, .login-card');

    document.addEventListener('mousemove', (e) => {
        const x = (window.innerWidth / 2 - e.clientX) / 50;
        const y = (window.innerHeight / 2 - e.clientY) / 50;

        depthElements.forEach((el, index) => {
            const depth = (index % 3 + 1) * 0.5;
            el.style.transform = `
                perspective(1000px)
                rotateY(${x * depth}deg)
                rotateX(${-y * depth}deg)
                translateZ(${depth * 10}px)
            `;
        });
    });
}

// ==================== NEON TEXT EFFECT ====================
function initializeNeonText() {
    const titles = document.querySelectorAll('.page-title, .card-title, h1, h2');

    titles.forEach(title => {
        title.classList.add('neon-text');

        // Add flicker effect occasionally
        setInterval(() => {
            if (Math.random() > 0.95) {
                title.style.textShadow = 'none';
                setTimeout(() => {
                    title.style.textShadow = '';
                }, 50);
            }
        }, 100);
    });
}

// ==================== HOLOGRAPHIC CARDS ====================
function initializeHolographicCards() {
    const cards = document.querySelectorAll('.glass-card');

    cards.forEach(card => {
        const holo = document.createElement('div');
        holo.className = 'holo-effect';
        holo.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(
                105deg,
                transparent 20%,
                rgba(255, 255, 255, 0.03) 25%,
                rgba(255, 255, 255, 0.05) 30%,
                transparent 35%
            );
            background-size: 200% 200%;
            pointer-events: none;
            border-radius: inherit;
            animation: holoShine 8s ease-in-out infinite;
        `;
        card.style.position = 'relative';
        card.appendChild(holo);

        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;

            holo.style.background = `
                radial-gradient(circle at ${x}% ${y}%, 
                    rgba(99, 102, 241, 0.15) 0%,
                    rgba(139, 92, 246, 0.1) 25%,
                    rgba(236, 72, 153, 0.05) 50%,
                    transparent 70%
                )
            `;
        });

        card.addEventListener('mouseleave', () => {
            holo.style.background = '';
        });
    });
}

// ==================== ELECTRIC SPARKS ====================
function initializeElectricSparks() {
    const buttons = document.querySelectorAll('.btn-primary, .btn-success');

    buttons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            createElectricBurst(e.clientX, e.clientY);
        });

        btn.addEventListener('mouseenter', () => {
            btn.classList.add('electric-hover');
        });

        btn.addEventListener('mouseleave', () => {
            btn.classList.remove('electric-hover');
        });
    });
}

function createElectricBurst(x, y) {
    const colors = ['#6366f1', '#8b5cf6', '#ec4899', '#06b6d4', '#10b981'];

    for (let i = 0; i < 12; i++) {
        const spark = document.createElement('div');
        const angle = (i / 12) * Math.PI * 2;
        const velocity = Math.random() * 100 + 50;
        const size = Math.random() * 4 + 2;

        spark.style.cssText = `
            position: fixed;
            left: ${x}px;
            top: ${y}px;
            width: ${size}px;
            height: ${size * 3}px;
            background: linear-gradient(to bottom, ${colors[Math.floor(Math.random() * colors.length)]}, transparent);
            border-radius: 50%;
            pointer-events: none;
            z-index: 10000;
            transform: rotate(${angle}rad);
            animation: electricSpark 0.6s ease-out forwards;
            --tx: ${Math.cos(angle) * velocity}px;
            --ty: ${Math.sin(angle) * velocity}px;
            box-shadow: 0 0 10px currentColor;
        `;

        document.body.appendChild(spark);
        setTimeout(() => spark.remove(), 600);
    }
}

// ==================== DYNAMIC 3D STYLES ====================
const styles3D = document.createElement('style');
styles3D.textContent = `
    @keyframes float3DRotate {
        0% { transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg) translateY(0); }
        25% { transform: rotateX(90deg) rotateY(45deg) rotateZ(45deg) translateY(-20px); }
        50% { transform: rotateX(180deg) rotateY(90deg) rotateZ(90deg) translateY(0); }
        75% { transform: rotateX(270deg) rotateY(135deg) rotateZ(135deg) translateY(20px); }
        100% { transform: rotateX(360deg) rotateY(180deg) rotateZ(180deg) translateY(0); }
    }
    
    @keyframes ringFloat {
        0%, 100% { transform: translateY(0) rotateX(45deg); }
        50% { transform: translateY(-30px) rotateX(45deg); }
    }
    
    @keyframes ringSpin {
        from { transform: rotateX(45deg) rotateZ(0deg); }
        to { transform: rotateX(45deg) rotateZ(360deg); }
    }
    
    @keyframes orbFloat {
        0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.6; }
        25% { transform: translate(20px, -20px) scale(1.1); opacity: 0.8; }
        50% { transform: translate(0, -40px) scale(1); opacity: 0.6; }
        75% { transform: translate(-20px, -20px) scale(0.9); opacity: 0.4; }
    }
    
    @keyframes pyramidFloat {
        0%, 100% { transform: translateY(0) rotateY(0deg); }
        50% { transform: translateY(-25px) rotateY(180deg); }
    }
    
    @keyframes holoShine {
        0%, 100% { background-position: -200% -200%; }
        50% { background-position: 200% 200%; }
    }
    
    @keyframes electricSpark {
        0% { 
            opacity: 1; 
            transform: translate(0, 0) rotate(var(--angle, 0deg)) scale(1);
        }
        100% { 
            opacity: 0; 
            transform: translate(var(--tx), var(--ty)) rotate(var(--angle, 0deg)) scale(0);
        }
    }
    
    .neon-text {
        text-shadow: 
            0 0 5px var(--primary),
            0 0 10px var(--primary),
            0 0 20px var(--primary),
            0 0 40px var(--secondary),
            0 0 80px var(--secondary);
        animation: neonPulse 2s ease-in-out infinite alternate;
    }
    
    @keyframes neonPulse {
        from {
            text-shadow: 
                0 0 5px var(--primary),
                0 0 10px var(--primary),
                0 0 20px var(--primary),
                0 0 40px var(--secondary);
        }
        to {
            text-shadow: 
                0 0 10px var(--primary),
                0 0 20px var(--primary),
                0 0 40px var(--primary),
                0 0 80px var(--secondary),
                0 0 120px var(--accent);
        }
    }
    
    .electric-hover {
        animation: electricPulse 0.15s ease-in-out infinite;
    }
    
    @keyframes electricPulse {
        0%, 100% { 
            box-shadow: 
                0 0 5px var(--primary),
                0 0 10px var(--primary),
                0 0 20px var(--secondary);
        }
        50% { 
            box-shadow: 
                0 0 10px var(--primary),
                0 0 20px var(--primary),
                0 0 40px var(--secondary),
                0 0 60px var(--accent);
        }
    }
    
    /* Enhanced glass cards with 3D depth */
    .glass-card {
        transform-style: preserve-3d;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(
            45deg,
            var(--primary),
            var(--secondary),
            var(--accent),
            var(--primary)
        );
        background-size: 400% 400%;
        border-radius: calc(var(--radius-lg) + 2px);
        z-index: -1;
        opacity: 0;
        transition: opacity 0.3s ease;
        animation: gradientRotate 8s linear infinite;
        filter: blur(15px);
    }
    
    .glass-card:hover::before {
        opacity: 0.5;
    }
    
    @keyframes gradientRotate {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating animation for shapes */
    .floating-shapes-container {
        transform-style: preserve-3d;
    }
    
    /* Reduce motion for accessibility */
    @media (prefers-reduced-motion: reduce) {
        .floating-3d-shape,
        .mouse-trail-dot,
        .aurora-layer,
        .glow-border-left,
        .glow-border-right,
        .glow-border-top,
        .glow-border-bottom,
        .corner-glow {
            animation: none !important;
            opacity: 0 !important;
        }
    }
`;
document.head.appendChild(styles3D);
