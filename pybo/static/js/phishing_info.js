document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const submitBtn = document.getElementById('InfoSubmitBtn');

    const siteUrl = document.getElementById('site_url');
    const siteName = document.getElementById('site_name');
    const caseTypeRadios = document.querySelectorAll('input[name="case_type"]');

    function validateForm() {
        let valid = true;
        if (!siteUrl.value.trim() || !siteName.value.trim()) {
            valid = false;
        }

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

    [siteUrl, siteName].forEach(field => {
        field.addEventListener('input', function () {
            toggleSubmitButton();
        });
    });

    caseTypeRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            toggleSubmitButton();
        });
    });

    form.addEventListener('submit', function (e) {
        if (!validateForm()) {
            e.preventDefault();
            alert('모든 필수 입력란을 채워주세요.');
        }
    });

    toggleSubmitButton();
});
