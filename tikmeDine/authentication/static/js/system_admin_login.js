document.getElementById('login-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    // Send login request
    fetch('/auth/system_admin_login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            password: password
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Login failed');
        }
        return response.json();
    })
    .then(data => {
        if (data.token && data.redirect_url) {
            // Store the token
            sessionStorage.setItem('jwtToken', data.token);
            // Redirect to the dashboard using the provided redirect_url
            window.location.href = data.redirect_url;
        } else {
            document.getElementById('error-message').innerText = data.error || 'Login failed';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('error-message').innerText = 'An error occurred. Please try again.';
    });
});

// Fetch dashboard data after redirection
window.addEventListener('load', function() {
    const token = sessionStorage.getItem('jwtToken');
    if (token) {
        fetch('/system_admin_dashboard/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`, // Include the token
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch dashboard');
            }
            return response.json();
        })
        .then(data => {
            // Handle the dashboard data
            document.getElementById('dashboard-content').innerText = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            console.error('Error fetching dashboard:', error);
            document.getElementById('error-message').innerText = 'An error occurred while loading the dashboard.';
        });
    }
});

function togglePassword() {
    const passwordField = document.getElementById('password');
    const eyeIcon = document.querySelector('.eye-icon');
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        eyeIcon.innerHTML = '🙈'; // Change icon to indicate password is visible
    } else {
        passwordField.type = 'password';
        eyeIcon.innerHTML = '👁️'; // Change icon back to indicate password is hidden
    }
}
