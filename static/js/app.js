// Slide in transition
window.dispatchEvent(new Event("scroll"));

document.addEventListener("DOMContentLoaded", function () {
    const elements = document.querySelectorAll('.slide-in');

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('slide-in-visible');
                observer.unobserve(entry.target); // Only animate once
            }
        });
    }, { threshold: 0.1 });

    elements.forEach(el => observer.observe(el));
});

document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('theme-toggle');
    const body = document.body;
    const icon = toggleButton.querySelector('i');

    // Set theme based on localStorage
    if (localStorage.getItem('theme') === 'light') {
        body.classList.add('light-mode');
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
    }

    toggleButton.addEventListener('click', () => {
        body.classList.toggle('light-mode');
        const isLight = body.classList.contains('light-mode');

        // Toggle the icon between sun and moon
        if (isLight) {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        }

        // Save the current theme in localStorage
        localStorage.setItem('theme', isLight ? 'light' : 'dark');
    });
  });