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

function changeStatus(employeeId, status) {
    // Add your logic for changing account status here
    console.log(`Change status of employee ${employeeId} to ${status}`);
}

function sendEmail(employeeId, emailType) {
    // Add your logic for sending emails here
    console.log(`Send ${emailType} email to employee ${employeeId}`);
}

function toggleSidebar() {
    var sidebar = document.querySelector('.sidebar');
    var mainContent = document.querySelector('.main-content');
    sidebar.classList.toggle('collapsed');
    if (sidebar.classList.contains('collapsed')) {
        mainContent.style.marginLeft = '60px';
    } else {
        mainContent.style.marginLeft = '250px';
    }
}

function showPasswordSection() {
    document.getElementById('security-questions').style.display = 'none';
    document.getElementById('password-section').style.display = 'block';
}