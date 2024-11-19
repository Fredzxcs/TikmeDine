document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');
    const errorMessageDiv = document.getElementById('errorMessage');
    const loadingIndicator = document.getElementById('loadingIndicator');

    // Handle login form submission
    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            event.preventDefault(); // Prevent default form submission

            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value.trim();

            // Clear error messages and show loading indicator
            errorMessageDiv.style.display = 'none';
            errorMessageDiv.textContent = '';
            if (loadingIndicator) loadingIndicator.style.display = 'block'; // Show loading spinner

            // Send login request to the server
            fetch('/api-auth/admin_login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded', // Standard form encoding
                    'X-CSRFToken': getCSRFToken(), // CSRF token
                },
                body: new URLSearchParams({
                    username: username,
                    password: password
                })
            })
                .then(response => {
                    if (response.ok) {
                        window.location.href = response.url;  // Redirect on success
                    } else {
                        response.text().then(text => {
                            throw new Error(text || 'Login failed');
                        });
                    }
                })
                .catch(error => {
                    // Hide loading spinner and display error
                    if (loadingIndicator) loadingIndicator.style.display = 'none';
                    console.error('Error:', error);
                    errorMessageDiv.style.display = 'block';
                    errorMessageDiv.textContent = error.message;
                });
        });
    }

    // Function to get CSRF token for Django
    function getCSRFToken() {
        let csrfToken = null;
        const cookies = document.cookie.split(';');
        cookies.forEach(cookie => {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                csrfToken = value;
            }
        });
        return csrfToken;
    }

    // Password toggle visibility function
    window.togglePassword = function () {
        const passwordInput = document.getElementById('password');
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
    };
});
