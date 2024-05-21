document.addEventListener('DOMContentLoaded', function() {
    let customerSupportWindow = null;
    let customerQuestionWindow = null;

    document.getElementById('customer-support-link').addEventListener('click', function(event) {
        event.preventDefault(); // 링크의 기본 동작을 막음

        if (!customerSupportWindow || customerSupportWindow.closed) {
            customerSupportWindow = window.open('', '고객센터', 'width=400,height=200');
        }

        customerSupportWindow.document.body.innerHTML = '<h1>이것은 고객센터다.</h1>';
    });

    document.getElementById('customer-question-link').addEventListener('click', function(event) {
        event.preventDefault(); // 링크의 기본 동작을 막음

        if (!customerQuestionWindow || customerQuestionWindow.closed) {
            customerQuestionWindow = window.open('', '문의 안내', 'width=400,height=200');
        }

        customerQuestionWindow.document.body.innerHTML = '<h1>이메일 보내라: mnzy412@gmail.com</h1>';
    });
});
