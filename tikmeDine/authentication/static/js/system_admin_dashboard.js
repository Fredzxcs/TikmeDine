document.addEventListener('DOMContentLoaded', function() {
    const token = sessionStorage.getItem('jwtToken'); // Get the token from session storage
    if (!token) {
        // If no token, redirect to login page
        window.location.href = '/auth/system_admin_login/';
        return;
    }

    fetch('/auth/system_admin_dashboard/', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`, // Include the token
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        // Handle the dashboard data here
        document.getElementById('dashboard-content').innerText = JSON.stringify(data, null, 2);
        // You can customize how you display this data
    })
    .catch(error => {
        console.error('Error fetching dashboard:', error);
        // Handle error appropriately, e.g., redirect to login if unauthorized
    });
});