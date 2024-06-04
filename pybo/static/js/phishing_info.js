document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const submitBtn = document.getElementById('InfoSubmitBtn');

    const siteUrl = document.getElementById('site_url');
    const siteName = document.getElementById('site_name');
    const caseDate = document.getElementById('case_date');
    const siteContent = document.getElementById('site_content');

    const errorMessages = {
        'site_url': document.createElement('div'),
        'site_name': document.createElement('div'),
        'case_date': document.createElement('div'),
        'site_content': document.createElement('div')
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

    function isUrlValid(url) {
        const urlPattern = /^(http:\/\/|https:\/\/)[^\s$.?#].[^\s]*$/;
        return urlPattern.test(url.value.trim());
    }

    function validateField(field) {
        const fieldId = field.id;
        let valid = true;

        if (fieldId === 'site_url') {
            if (isFieldEmpty(field)) {
                showErrorMessage(fieldId, '피싱 사이트 URL을 입력해주세요.');
                valid = false;
            } else if (!isUrlValid(field)) {
                showErrorMessage(fieldId, 'URL 형식이 올바르지 않습니다. http 또는 https로 시작해야 합니다.');
                valid = false;
            }
        } else if (fieldId === 'site_name' && isFieldEmpty(field)) {
            showErrorMessage(fieldId, '피싱 사이트 이름을 입력해주세요.');
            valid = false;
        } else if (fieldId === 'case_date' && isFieldEmpty(field)) {
            showErrorMessage(fieldId, '입금일을 선택해주세요.');
            valid = false;
        } else if (fieldId === 'site_content' && isFieldEmpty(field)) {
            showErrorMessage(fieldId, '사건 개요를 입력해주세요.');
            valid = false;
        }

        if (valid) {
            clearErrorMessage(fieldId);
        }

        return valid;
    }

    function validateForm() {
        let valid = true;
        [siteUrl, siteName, caseDate, siteContent].forEach(field => {
            if (!validateField(field)) {
                valid = false;
            }
        });
        return valid;
    }

    function toggleSubmitButton() {
        submitBtn.disabled = !validateForm();
    }

    [siteUrl, siteName, caseDate, siteContent].forEach(field => {
        field.addEventListener('input', function () {
            clearErrorMessage(field.id);
            toggleSubmitButton();
        });
        field.addEventListener('blur', function() {
            validateField(field);
        });
        field.addEventListener('focus', function() {
            clearErrorMessage(field.id); // 포커스 시 오류 메시지 초기화
            if (field.id === 'site_url') {
                field.setAttribute('title', '피싱 사이트 URL을 입력해주세요.');
            } else if (field.id === 'site_name') {
                field.setAttribute('title', '피싱 사이트 이름을 입력해주세요.');
            } else if (field.id === 'site_content') {
                field.setAttribute('title', '사건 개요를 입력해주세요.');
            }
        });
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        if (validateForm()) {
            alert('양식이 제출되었습니다.');
            form.submit(); // 실제로 폼을 제출하려면 이 줄의 주석을 해제하세요
        } else {
            alert('양식을 다시 작성해주세요.');
        }
    });
});