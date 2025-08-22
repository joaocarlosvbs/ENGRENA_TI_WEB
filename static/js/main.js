document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('login-modal');
    const loginTrigger = document.getElementById('login-trigger');
    const closeButton = document.querySelector('.close-button');

    loginTrigger.onclick = function(e) {
        e.preventDefault();
        modal.style.display = 'block';
    }

    closeButton.onclick = function() {
        modal.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
});