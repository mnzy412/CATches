document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('phishingForm');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // 폼의 기본 제출 동작을 막음

        // 폼 데이터 수집
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        // 유효성 검사
        if (validateForm(data)) {
            // 데이터를 서버로 전송하거나 다른 처리를 수행
            console.log('폼 제출됨:', data);
            alert('폼이 성공적으로 제출되었습니다!');
        } else {
            alert('모든 필드를 올바르게 작성해주세요.');
        }
    });

    function validateForm(data) {
        // 각 필드에 대한 유효성 검사 로직 추가
        // 예: 필드가 비어 있지 않은지 확인
        for (const key in data) {
            if (data[key] === '') {
                return false;
            }
        }
        return true;
    }
});
