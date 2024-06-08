document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const submitBtn = document.getElementById('InfoSubmitBtn');

    const bankName = document.getElementById('bank-name');
    const bankAccount = document.getElementById('bank_account');
    const bankNickname = document.getElementById('bank_nickname');
    const caseTypeRadios = document.querySelectorAll('input[name="case_type"]');

    const errorMessages = {
        'bank-name': document.getElementById('error-bank-name'),
        'bank_account': document.getElementById('error-bank-account'),
        'bank_nickname': document.getElementById('error-bank-nickname')
    };

    function showErrorMessage(fieldId, message) {
        const errorElement = errorMessages[fieldId];
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        const inputElement = document.getElementById(fieldId);
        inputElement.classList.add('invalid');
    }

    function clearErrorMessage(fieldId) {
        const errorElement = errorMessages[fieldId];
        errorElement.textContent = '';
        errorElement.style.display = 'none';
        const inputElement = document.getElementById(fieldId);
        inputElement.classList.remove('invalid');
    }

    function isFieldEmpty(field) {
        return !field.value.trim();
    }

    function validateField(field) {
        const fieldId = field.id;
        let valid = true;

        if (valid) {
            clearErrorMessage(fieldId);
        }

        return valid;
    }

    function validateForm() {
        let valid = true;
        [bankName, bankAccount, bankNickname].forEach(field => {
            if (!validateField(field)) {
                valid = false;
            }
        });

        const caseTypeChecked = Array.from(caseTypeRadios).some(radio => radio.checked);
        if (!caseTypeChecked) {
            valid = false;
        }

        return valid;
    }

    function toggleSubmitButton() {
        submitBtn.disabled = !validateForm();
        submitBtn.style.cursor = validateForm() ? 'pointer' : 'default';
        submitBtn.style.opacity = validateForm() ? '1' : '0.6';
    }

    [bankName, bankAccount, bankNickname].forEach(field => {
        field.addEventListener('input', function () {
            clearErrorMessage(field.id);
            toggleSubmitButton();
        });
        field.addEventListener('blur', function() {
            validateField(field);
        });
        field.addEventListener('focus', function() {
            clearErrorMessage(field.id);
            if (field.id === 'bank-name') {
                field.setAttribute('title', '은행명을 입력해주세요.');
            } else if (field.id === 'bank_account') {
                field.setAttribute('title', '계좌번호를 입력해주세요.');
            } else if (field.id === 'bank_nickname') {
                field.setAttribute('title', '명의자 성명을 입력해주세요.');
            }
        });
    });

    caseTypeRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            toggleSubmitButton();
        });
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        if (validateForm()) {
            form.submit();
        } else {
            alert('필수 항목을 모두 입력해주세요.');
        }
    });

    toggleSubmitButton();
});
