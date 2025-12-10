/* =============================
   SIDEBAR TOGGLE
   ============================= */

$(document).ready(function () {
    $("#toggle-btn").on("click", function () {
        $("#sidebar").toggleClass("collapsed");
    });
});

/* =============================
   TOAST SYSTEM
   ============================= */

function showToast(message, type = "success") {
    let toast = $(`
        <div class="custom-toast ${type}">
            ${message}
        </div>
    `);

    $("body").append(toast);
    toast.fadeIn(300);

    setTimeout(() => {
        toast.fadeOut(300, function () {
            $(this).remove();
        });
    }, 3000);
}

/* =============================
   GENERIC HELPERS
   ============================= */

function formatMoney(amount) {
    return new Intl.NumberFormat().format(amount);
}

function confirmDelete(callback) {
    if (confirm("Are you sure you want to delete this item?")) {
        callback();
    }
}

/* =============================
   AJAX DEFAULTS (CSRF)
   ============================= */

function getCSRFToken() {
    let cookieValue = null;
    let cookies = document.cookie.split(";");

    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith("csrftoken=")) {
            cookieValue = cookie.substring("csrftoken=".length);
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!(/^GET|HEAD|OPTIONS|TRACE$/i.test(settings.type))) {
            xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
        }
    }
});
