// Image Slider JavaScript
let currentImageIndex = 0;
const images = document.querySelectorAll('.image-slider img');
const totalImages = images.length;

setInterval(() => {
    images[currentImageIndex].classList.add('hidden');
    currentImageIndex = (currentImageIndex + 1) % totalImages;
    images[currentImageIndex].classList.remove('hidden');
}, 3000); // Change image every 3 seconds