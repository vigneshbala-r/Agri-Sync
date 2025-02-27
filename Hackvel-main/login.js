/login/
// Toggle Password Visibility
function togglePassword() {
    const passwordInput = document.getElementById('password');
    const eyeIcon = document.getElementById('eye-icon');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeIcon.src = 'pic/imgi1.png'; // Change to visible icon
    } else {
        passwordInput.type = 'password';
        eyeIcon.src = 'pic/imgi2.png'; // Change to hidden icon
    }
}