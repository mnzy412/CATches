document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loginForm');
    const submitBtn = document.getElementById('submitBtn');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');

    function validateForm() {
        if (emailInput.value && passwordInput.value) {
            submitBtn.disabled = false;
        } else {
            submitBtn.disabled = true;
        }
    }

    emailInput.addEventListener('input', validateForm);
    passwordInput.addEventListener('input', validateForm);

    form.addEventListener('submit', function(event) {
        if (submitBtn.disabled) {
            event.preventDefault();
        }
    });
});
