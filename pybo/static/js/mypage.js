document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('customer-support-link').addEventListener('click', function(event) {
        event.preventDefault(); // 링크의 기본 동작을 막음
        window.open('', '고객센터', 'width=400,height=200').document.write('<h1>이것은 고객센터다.</h1>');
    });

    document.getElementById('customer-question-link').addEventListener('click', function(event) {
        event.preventDefault(); // 링크의 기본 동작을 막음
        window.open('', '문의 안내', 'width=400,height=200').document.write('<h1>이메일 보내라: mnzy412@gmail.com</h1>');
    });
});
