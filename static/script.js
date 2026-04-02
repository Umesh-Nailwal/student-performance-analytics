document.addEventListener('DOMContentLoaded', () => {

    // FLASH AUTO HIDE
    const flashContainer = document.getElementById('flash-container');
    if (flashContainer) {
        setTimeout(() => {
            flashContainer.style.transition = "opacity 0.6s ease";
            flashContainer.style.opacity = "0";
            setTimeout(() => {
                flashContainer.remove();
            }, 600);
        }, 3000);
    }

    // HAMBURGER MENU
    const menuBtn = document.getElementById('mobile-menu');
    const sidebar = document.getElementById('sidebar');

    if (menuBtn && sidebar) {

        menuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            sidebar.classList.toggle('active');
        });

        document.addEventListener('click', (e) => {
            if (
                window.innerWidth <= 768 &&
                !sidebar.contains(e.target) &&
                !menuBtn.contains(e.target)
            ) {
                sidebar.classList.remove('active');
            }
        });
    }

});