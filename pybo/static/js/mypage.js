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
        fetch('/user_info')
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    document.getElementById('user-name').textContent = data.user_name;
                    document.getElementById('user-phone').textContent = data.user_phone;
                    document.getElementById('info-modal').style.display = 'block';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
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
