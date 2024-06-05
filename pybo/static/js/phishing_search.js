document.addEventListener('DOMContentLoaded', function () {
    const phishingInfoInput = document.getElementById('phishingInfo');
    const phishingSubmitBtn = document.getElementById('PhishingSubmitBtn');
    const phishingSearchForm = document.getElementById('PhishingSearchForm');

    // 입력값 검증 함수
    function validateInput() {
        const phishingInfoValue = phishingInfoInput.value.trim();

        // 정규 표현식 검증
        const urlRegex = /^(https?:\/\/)?([\w-]+\.)+[\w-]+(\/[\w-]*)*$/; // http 또는 https URL 형식
        const nameRegex = /^[가-힣a-zA-Z\s]+$/; // 한글과 영어만

        const isUrlValid = urlRegex.test(phishingInfoValue);
        const isNameValid = nameRegex.test(phishingInfoValue) && !/^\d+$/.test(phishingInfoValue); // 숫자만 입력 방지

        phishingSubmitBtn.disabled = !(isUrlValid || isNameValid);
    }

    // 폼 제출 이벤트 핸들러
    phishingSearchForm.addEventListener('submit', function (event) {
        const phishingInfoValue = phishingInfoInput.value.trim();

        // 입력값 검증
        const urlRegex = /^(https?:\/\/)?([\w-]+\.)+[\w-]+(\/[\w-]*)*$/; // http 또는 https URL 형식
        const nameRegex = /^[가-힣a-zA-Z\s]+$/; // 한글과 영어만

        const isUrlValid = urlRegex.test(phishingInfoValue);
        const isNameValid = nameRegex.test(phishingInfoValue) && !/^\d+$/.test(phishingInfoValue); // 숫자만 입력 방지

        if (!isUrlValid && !isNameValid) {
            alert("URL 형식 또는 올바른 피싱 사이트 이름을 입력해주세요.");
            event.preventDefault();
            return;
        }

        let searchType;
        if (isUrlValid) {
            searchType = "URL";
        } else if (isNameValid) {
            searchType = "피싱 사이트 이름";
        }

        // 검색 요청을 보낼 로직 작성
        alert(`검색어: ${phishingInfoValue} (검색 타입: ${searchType})`);
    });

    // 입력 필드 이벤트 리스너 추가
    phishingInfoInput.addEventListener('input', validateInput);

    // 초기 검증
    validateInput();
});
