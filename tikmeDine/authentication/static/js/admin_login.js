// Image Slider JavaScript
let currentImageIndex = 0;
const images = document.querySelectorAll('.image-slider img');
const totalImages = images.length;

setInterval(() => {
    images[currentImageIndex].classList.add('hidden');
    currentImageIndex = (currentImageIndex + 1) % totalImages;
    images[currentImageIndex].classList.remove('hidden');
}, 3000); // Change image every 3 seconds

function toggleVisibility(field_id) {
    var field = document.getElementById(field_id);
    if (field.type === "password") {
        field.type = "text";
    } else {
        field.type = "password";
    }
}