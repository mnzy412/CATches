document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('customer-support-link').addEventListener('click', function(event) {
        event.preventDefault();
        document.getElementById('support-modal').style.display = 'block';
    });

    document.getElementById('customer-question-link').addEventListener('click', function(event) {
        event.preventDefault();
        document.getElementById('question-modal').style.display = 'block';
    });

    document.getElementById('info-view-link').addEventListener('click', function() {
        document.getElementById('info-modal').style.display = 'block';
    });

    document.querySelectorAll('.close-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            btn.parentElement.parentElement.style.display = 'none';
        });
    });

    window.addEventListener('click', function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    });
});
