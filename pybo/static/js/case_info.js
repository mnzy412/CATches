document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const submitBtn = document.getElementById('InfoSubmitBtn');
    
    const bankName = document.getElementById('bank-name');
    const bankAccount = document.getElementById('bank_account');
    const bankNickname = document.getElementById('bank_nickname');
    const suspectPhone = document.getElementById('suspect_phone');
    const caseDate = document.getElementById('case_date');
    const casePrice = document.getElementById('case_price');
    const caseItem = document.getElementById('case_item');
    const suspectKey = document.getElementById('suspect_key');
    const phishingUrl = document.getElementById('phishing_url');
    const caseDescription = document.getElementById('case_description');
    
    const errorMessages = {
        'bank-name': document.createElement('div'),
        'bank_account': document.createElement('div'),
        'bank_nickname': document.createElement('div'),
        'suspect_phone': document.createElement('div'),
        'case_date': document.createElement('div'),
        'case_price': document.createElement('div'),
        'case_item': document.createElement('div'),
        'suspect_key': document.createElement('div'),
        'phishing_url': document.createElement('div'),
        'case_description': document.createElement('div')
    };

    // 각 필드에 오류 메시지 요소를 추가
    Object.keys(errorMessages).forEach(fieldId => {
        const field = document.getElementById(fieldId);
        const errorMessage = errorMessages[fieldId];
        errorMessage.className = 'error-message';
        errorMessage.style.display = 'none';
        field.parentNode.insertBefore(errorMessage, field.nextSibling);
    });

    function showErrorMessage(fieldId, message) {
        clearErrorMessages();
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

    function clearErrorMessages() {
        Object.keys(errorMessages).forEach(fieldId => {
            clearErrorMessage(fieldId);
        });
    }

    function validateField(field, pattern, message, fieldId) {
        if (!pattern.test(field.value.trim())) {
            showErrorMessage(fieldId, message);
            return false;
        } else {
            clearErrorMessage(fieldId);
        }
        return true;
    }
    
    function isFormValid() {
        const specialCharPattern = /^[^!@#$%^&*(),.?":{}|<>]+$/;
        let valid = true;
        
        valid &= validateField(bankName, specialCharPattern, '특수문자나 특수기호는 입력할 수 없습니다.', 'bank-name');
        valid &= validateField(bankAccount, /^\d{11,14}$/, '계좌번호는 11자리에서 14자리여야 합니다.', 'bank_account');
        valid &= validateField(bankNickname, specialCharPattern, '특수문자나 특수기호는 입력할 수 없습니다.', 'bank_nickname');
        valid &= validateField(suspectPhone, /^\d{11}$/, '연락처는 숫자 11자리여야 합니다.', 'suspect_phone');
        valid &= validateField(casePrice, /^\d+$/, '입금 금액은 숫자만 포함해야 합니다.', 'case_price');
        valid &= validateField(caseItem, specialCharPattern, '특수문자나 특수기호는 입력할 수 없습니다.', 'case_item');
        valid &= validateField(suspectKey, specialCharPattern, '특수문자나 특수기호는 입력할 수 없습니다.', 'suspect_key');
        valid &= validateField(phishingUrl, /^(http:\/\/|https:\/\/)[^\s$.?#].[^\s]*$/, 'URL 형식이 올바르지 않습니다.', 'phishing_url');
        
        if (!caseDate.value.trim()) {
            showErrorMessage('case_date', '입금일을 선택해주세요.');
            valid = false;
        } else {
            clearErrorMessage('case_date');
        }

        if (!caseDescription.value.trim()) {
            showErrorMessage('case_description', '사건 개요를 입력해주세요.');
            valid = false;
        } else {
            clearErrorMessage('case_description');
        }
        
        return valid;
    }

    function getFieldPattern(field) {
        switch (field.id) {
            case 'bank-name':
            case 'bank_nickname':
            case 'case_item':
            case 'suspect_key':
                return /^[^!@#$%^&*(),.?":{}|<>]+$/;
            case 'bank_account':
                return /^\d{11,14}$/;
            case 'suspect_phone':
                return /^\d{11}$/;
            case 'case_price':
                return /^\d+$/;
            case 'phishing_url':
                return /^(http:\/\/|https:\/\/)[^\s$.?#].[^\s]*$/;
            default:
                return /.*/;
        }
    }

    function getFieldMessage(field) {
        switch (field.id) {
            case 'bank-name':
            case 'bank_nickname':
            case 'case_item':
            case 'suspect_key':
                return '특수문자나 특수기호는 입력할 수 없습니다.';
            case 'bank_account':
                return '계좌번호는 11자리에서 14자리여야 합니다.';
            case 'suspect_phone':
                return '연락처는 숫자 11자리여야 합니다.';
            case 'case_price':
                return '입금 금액은 숫자만 포함해야 합니다.';
            case 'phishing_url':
                return 'URL 형식이 올바르지 않습니다.';
            default:
                return '';
        }
    }

    [bankName, bankAccount, bankNickname, suspectPhone, casePrice, caseItem, suspectKey, phishingUrl, caseDate, caseDescription].forEach(field => {
        field.addEventListener('focus', function () {
            validateField(field, getFieldPattern(field), getFieldMessage(field), field.id);
        });

        field.addEventListener('input', function () {
            validateField(field, getFieldPattern(field), getFieldMessage(field), field.id);
            submitBtn.disabled = !isFormValid();
        });
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        if (isFormValid()) {
            alert('양식이 제출되었습니다.');
            // form.submit(); // 실제로 폼을 제출하려면 이 줄의 주석을 해제하세요
        } else {
            alert('양식을 다시 작성해주세요.');
        }
    });
});
