// script.js
document.addEventListener('DOMContentLoaded', function () {
    var modal = document.getElementById("contact-us-modal");
    var btn = document.getElementById("contact-btn");
    var span = document.getElementsByClassName("close-button")[0];

    btn.onclick = function() {
        modal.style.display = "block";
    }

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});
