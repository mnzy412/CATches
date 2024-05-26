/* '연락처, 계좌번호, 이름' 입력한 값 검증 */
document.addEventListener('DOMContentLoaded', function () {
    const caseListInput = document.getElementById('caseList');
    const submitListBtn = document.getElementById('submitList');
    const listSearchForm = document.getElementById('ListSearchForm');

    // 입력값 검증 함수
    function validateInput() {
        const caseListValue = caseListInput.value.trim();

        // 정규 표현식 검증
        const caseRegex = /^[가-힣]+$/; // 한글만
        const contactRegex = /^\d{11}$/; // 숫자 11자리
        const accountRegex = /^\d{11,14}$/; // 숫자 11~14자리

        const isCaseValid = caseRegex.test(caseListValue);
        const isContactValid = contactRegex.test(caseListValue);
        const isAccountValid = accountRegex.test(caseListValue);

        if (isCaseValid || isContactValid || isAccountValid) {
            submitListBtn.disabled = false;
        } else {
            submitListBtn.disabled = true;
        }
    }

    // 폼 제출 이벤트 핸들러
    listSearchForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const caseListValue = caseListInput.value.trim();

        // 입력값 검증
        const caseRegex = /^[가-힣]+$/; // 한글만
        const contactRegex = /^\d{11}$/; // 숫자 11자리
        const accountRegex = /^\d{11,14}$/; // 숫자 11~14자리

        const isCaseValid = caseRegex.test(caseListValue);
        const isContactValid = contactRegex.test(caseListValue);
        const isAccountValid = accountRegex.test(caseListValue);

        if (!isCaseValid && !isContactValid && !isAccountValid) {
            alert("용의자 이름, 연락처, 계좌 정보 중 하나를 올바르게 입력해주세요.");
            return;
        }

        let searchType;
        if (isCaseValid) {
            searchType = "용의자 이름";
        } else if (isContactValid) {
            searchType = "연락처";
        } else if (isAccountValid) {
            searchType = "계좌번호";
        }

        // 검색 요청을 보낼 로직 작성
        alert(`검색어: ${caseListValue} (검색 타입: ${searchType})`);
    });

    // 입력 필드 이벤트 리스너 추가
    caseListInput.addEventListener('input', validateInput);
});