function submitForm() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const formData = {
        username: username,
        password: password
    };

    // Make an AJAX request to the Flask backend
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // If authentication is successful, redirect to message page
            window.location.href = '/index';
        } else {
            // Display error message on the login page
            document.getElementById('errorMessage').innerText = 'Invalid credentials!';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
