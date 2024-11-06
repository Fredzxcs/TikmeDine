// Function to get the JWT token from local storage
function getToken() {
    return localStorage.getItem('jwtToken'); // Assuming the JWT is stored in local storage
}

// Function to validate the JWT token
function isTokenValid(token) {
    if (!token) return false;

    // Decode the payload from the token
    const payload = JSON.parse(atob(token.split('.')[1])); // Base64 decode the payload

    const currentTime = Math.floor(Date.now() / 1000); // Get current time in seconds

    // Check if the token is expired
    return payload.exp > currentTime; // Return true if token is not expired
}

// Function to handle form submission
function handleFormSubmit(event) {
    event.preventDefault(); // Prevent default form submission

    const token = getToken();

    // Check if the token is valid
    if (!isTokenValid(token)) {
        alert("Your session has expired or you are not logged in. Please log in again.");
        window.location.href = '/admin_login'; // Redirect to the login page
        return; // Exit the function
    }

    // Get the email value
    const email = document.getElementById('email').value;

    // Make a request to the server to send the password reset email
    fetch('/send_reset_email/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` // Include the JWT in the headers
        },
        body: JSON.stringify({ email: email })
    })
    .then(response => {
        if (response.ok) {
            alert("Password reset email sent. Please check your inbox.");
            window.location.href = '/admin_login'; // Optionally redirect after successful submission
        } else {
            return response.json().then(data => {
                alert(data.error || "An error occurred. Please try again.");
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An unexpected error occurred. Please try again.");
    });
}

// Attach the event listener to the form
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
});
