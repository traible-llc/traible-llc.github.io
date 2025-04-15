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