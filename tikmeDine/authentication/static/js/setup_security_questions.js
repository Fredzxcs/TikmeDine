// Function to get the JWT token from local storage
function getToken() {
    return localStorage.getItem('jwtToken');
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

// Function to send a request with the JWT token
function sendRequestWithToken(url, method = 'GET', data = null) {
    const token = getToken();
    if (!token) {
        console.error("No token found");
        return;
    }

    const headers = new Headers({
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    });

    const options = {
        method: method,
        headers: headers,
        body: data ? JSON.stringify(data) : null
    };

    return fetch(url, options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .catch(error => console.error('There was a problem with your fetch operation:', error));
}

// Call onPageLoad when the document is ready
document.addEventListener('DOMContentLoaded', onPageLoad);
