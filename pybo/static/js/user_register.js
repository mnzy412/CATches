document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loginForm');
    const submitBtn = document.getElementById('submitBtn');
    const nameInput = document.getElementById('name');
    const phoneInput = document.getElementById('phone');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');

    function validateForm() {
        if (nameInput.value && phoneInput.value && emailInput.value && passwordInput.value) {
            submitBtn.disabled = false;
        } else {
            submitBtn.disabled = true;
        }
    }

    nameInput.addEventListener('input', validateForm);
    phoneInput.addEventListener('input', validateForm);
    emailInput.addEventListener('input', validateForm);
    passwordInput.addEventListener('input', validateForm);

    form.addEventListener('submit', function(event) {
        if (submitBtn.disabled) {
            event.preventDefault();
        }
    });

    // 페이지 로드 시 초기 버튼 상태 설정
    validateForm();
});
