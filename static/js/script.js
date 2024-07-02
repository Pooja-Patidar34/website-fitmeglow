
// static/js/script.js

document.addEventListener("DOMContentLoaded", function() {
    var coll = document.getElementsByClassName("collapsible");
    for (var i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.display === "block") {
                content.style.display = "none";
            } else {
                content.style.display = "block";
            }
        });
    }


    document.getElementById('clear-filters-btn').addEventListener('click', function() {
        const checkboxes = document.querySelectorAll('#filter-form input[type="checkbox"]');
        checkboxes.forEach(checkbox => checkbox.checked = false);
        document.getElementById('filter-form').submit();
    });
    const filterForm = document.querySelector('#filter-form');
    const productContainer = document.querySelector('.products-section');

    filterForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(this);
        const queryString = new URLSearchParams(formData).toString();

        fetch(`${this.action}?${queryString}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log("Data received from server:", data);
            productContainer.innerHTML = data.html;
        })
        .catch(error => console.error('Error:', error));
    });
});
