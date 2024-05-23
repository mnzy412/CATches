//자기가 검색한 피싱 사이트와 동일한 URL만 보이도록 함
document.addEventListener('DOMContentLoaded', function () {
    const phishingInfoInput = document.getElementById('phishingInfo');
    const phishingSubmitBtn = document.getElementById('PhishingSubmitBtn');
    const phishingSearchForm = document.getElementById('PhishingSearchForm');

    // 입력값 검증 함수
    function validateInput() {
        const phishingInfoValue = phishingInfoInput.value.trim();

        // 정규 표현식 검증
        const urlRegex = /^(https?:\/\/)?([\w-]+\.)+[\w-]+(\/[\w-]*)*$/; // URL 형식
        const nameRegex = /^[가-힣a-zA-Z\s]+$/; // 한글과 영어만

        const isUrlValid = urlRegex.test(phishingInfoValue);
        const isNameValid = nameRegex.test(phishingInfoValue) && !/^\d+$/.test(phishingInfoValue); // 숫자만 입력 방지

        if (isUrlValid || isNameValid) {
            phishingSubmitBtn.disabled = false;
        } else {
            phishingSubmitBtn.disabled = true;
        }
    }

    // 폼 제출 이벤트 핸들러
    phishingSearchForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const phishingInfoValue = phishingInfoInput.value.trim();

        // 입력값 검증
        const urlRegex = /^(https?:\/\/)?([\w-]+\.)+[\w-]+(\/[\w-]*)*$/; // URL 형식
        const nameRegex = /^[가-힣a-zA-Z\s]+$/; // 한글과 영어만

        const isUrlValid = urlRegex.test(phishingInfoValue);
        const isNameValid = nameRegex.test(phishingInfoValue) && !/^\d+$/.test(phishingInfoValue); // 숫자만 입력 방지

        if (!isUrlValid && !isNameValid) {
            alert("URL 형식 또는 올바른 피싱 사이트 이름을 입력해주세요.");
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
});

//이제 하나의 입력창에서 'URL' 또는 '피싱 사이트 이름' 중 하나를 입력할 수 있으며, 각 값을 올바르게 검증할 수 있습니다.
// 폼이 제출될 때 어떤 타입의 검색어인지도 확인할 수 있습니다.