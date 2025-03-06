// Add event listener to handle dropdown toggle
document.addEventListener('DOMContentLoaded', function() {
    const dropdown = document.querySelector('.dropdown');

    dropdown.addEventListener('click', function() {
        this.classList.toggle('active');
    });
});