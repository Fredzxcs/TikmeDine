// Function to get the JWT token from local storage
function getToken() {
    return localStorage.getItem('jwtToken'); // Assuming you're storing the JWT in local storage
}

// Function to validate the token (simple check, customize as needed)
function isTokenValid(token) {
    if (!token) return false;

    const payload = JSON.parse(atob(token.split('.')[1])); // Decode the payload
    const currentTime = Math.floor(Date.now() / 1000); // Current time in seconds

    // Check if the token is expired
    return payload.exp > currentTime;
}

// Function to handle page load
function onPageLoad() {
    const token = getToken();

    // Check if token is present and valid
    if (!token || !isTokenValid(token)) {
        alert("Your session has expired or you are not logged in. Please log in again.");
        window.location.href = '/login'; // Redirect to the login page
    }
}

// Function to toggle password visibility
function toggleVisibility(inputId) {
    const inputField = document.getElementById(inputId);
    if (inputField.type === "password") {
        inputField.type = "text"; // Show the password
    } else {
        inputField.type = "password"; // Hide the password
    }
}

// Function to submit the form with the JWT token (optional)
function submitForm(event) {
    event.preventDefault(); // Prevent the default form submission
    const form = event.target;
    
    const token = getToken();
    if (!token) {
        console.error("No token found");
        return;
    }

    // Prepare form data to send
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries()); // Convert FormData to a regular object

    const headers = new Headers({
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    });

    fetch(form.action, {
        method: form.method,
        headers: headers,
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        // Handle success response (e.g., redirect to another page)
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error response (e.g., show an error message)
    });
}

// Call onPageLoad when the document is ready
document.addEventListener('DOMContentLoaded', onPageLoad);

// Attach form submission event
document.addEventListener('submit', submitForm);
