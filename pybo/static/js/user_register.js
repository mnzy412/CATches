document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registerForm');
    const submitBtn = document.getElementById('submitBtn');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const agreeCheckbox = document.getElementById('agree');

    function validateForm() {
        if (emailInput.value && passwordInput.value && agreeCheckbox.checked) {
            submitBtn.disabled = false;
        } else {
            submitBtn.disabled = true;
        }
    }

    emailInput.addEventListener('input', validateForm);
    passwordInput.addEventListener('input', validateForm);
    agreeCheckbox.addEventListener('change', validateForm);

    form.addEventListener('submit', function(event) {
        if (submitBtn.disabled) {
            event.preventDefault();
        }
    });
});
