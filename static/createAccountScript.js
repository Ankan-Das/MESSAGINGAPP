function submitForm() {
    const name = document.getElementById('name').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    // Perform client-side form validation
    if (password !== confirmPassword) {
        document.getElementById('createAccountForm').reset();  // Reset form
        alert('Password and Confirm Password must match.');
        return false;
    }

    const formData = {
        name: name,
        username: username,
        password: password
    };

    // Make an AJAX request to the Flask backend
    fetch('/createAccount', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // If account creation is successful, redirect to login page
            window.location.href = '/';
        } else {
            // Display error message on the create account page
            document.getElementById('createAccountForm').reset();  // Reset form
            document.getElementById('createAccountForm').querySelector('.error-message').innerText = 'Could not create an account! Please contact Admin.';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

    return false;  // Prevent default form submission
}
