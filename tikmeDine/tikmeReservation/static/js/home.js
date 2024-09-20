document.addEventListener("DOMContentLoaded", function() {
    // Function to handle the fade-in effect
    function fadeInOnScroll() {
        const aboutSection = document.querySelector('.about');
        const sectionPosition = aboutSection.getBoundingClientRect().top;
        const viewportHeight = window.innerHeight;

        if (sectionPosition < viewportHeight * 0.75) {
            aboutSection.style.opacity = '1';
        }
    }

    // Initial check
    fadeInOnScroll();

    // Add scroll event listener
    window.addEventListener('scroll', fadeInOnScroll);
});

window.addEventListener('scroll', function() {
const showcaseItems = document.querySelectorAll('.showcase-item');

showcaseItems.forEach(item => {
    const itemPosition = item.getBoundingClientRect().top;
    const windowHeight = window.innerHeight;

    if(itemPosition < windowHeight - 100) {
    item.classList.add('showcase-visible');
    }
});
});

function openGallery(src, alt) {
    document.querySelector('.gallery-container').style.display = 'flex';
    document.querySelector('#expandedImg').src = src;
    document.querySelector('#imgtext').innerText = alt;
}

document.querySelectorAll('.gallery-column img').forEach(img => {
    img.addEventListener('click', function() {
        openGallery(this.src, this.alt);    
    });
});

document.querySelector('.gallery-container .closebtn').addEventListener('click', function() {
    document.querySelector('.gallery-container').style.display = 'none';
});

document.addEventListener('DOMContentLoaded', function() {
    const galleryColumns = document.querySelectorAll('.gallery-column');
    
    function handleScroll() {
        const windowHeight = window.innerHeight;
        
        galleryColumns.forEach(column => {
            const columnTop = column.getBoundingClientRect().top;
            
            if (columnTop < windowHeight * 0.9) { // Trigger when image is 90% in view
                column.classList.add('show');
            } else {
                column.classList.remove('show');
            }
        });
    }
    
    window.addEventListener('scroll', handleScroll);
    handleScroll(); // Initial check
});