// Theme Toggle Functionality
const themeToggle = document.getElementById('theme-toggle');
const htmlElement = document.documentElement;

// Check for saved theme preference or default to 'light'
const currentTheme = localStorage.getItem('theme') || 'light';

// Apply the saved theme on page load
if (currentTheme === 'dark') {
    htmlElement.setAttribute('data-theme', 'dark');
    themeToggle.checked = true;
} else {
    htmlElement.setAttribute('data-theme', 'light');
    themeToggle.checked = false;
}

// Toggle theme on checkbox change
themeToggle.addEventListener('change', function() {
    if (this.checked) {
        htmlElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
    } else {
        htmlElement.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
    }
});

// Lazy load GIF only on hover
const gifContainer = document.querySelector('.gif-container');
const gifLoader = document.querySelector('.gif-loader');
let gifLoaded = false;

if (gifContainer && gifLoader) {
    // Set initial empty src to prevent auto-loading
    const gifSrc = gifLoader.getAttribute('src');
    gifLoader.removeAttribute('src');
    
    gifContainer.addEventListener('mouseenter', function() {
        if (!gifLoaded) {
            gifLoader.src = gifSrc + '?t=' + Date.now(); // Force reload with timestamp
            gifLoaded = true;
        }
    });
    
    gifContainer.addEventListener('mouseleave', function() {
        // Remove src to stop animation and save bandwidth
        setTimeout(() => {
            gifLoader.removeAttribute('src');
            gifLoaded = false;
        }, 100);
    });
}

// Add smooth reveal animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all menu items and content sections
document.querySelectorAll('.menu-item, .hero-section').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// Console easter egg
console.log('%c🚀 Bienvenue sur notre site futuriste! 🚀', 'font-size: 20px; color: #ff3a39; font-weight: bold;');
console.log('%cDéveloppé pour la Nuit de l\'Info 2024', 'font-size: 14px; color: #667eea;');
console.log('%cToggle le mode sombre pour une expérience optimale! 🌙', 'font-size: 12px; color: #764ba2;');