/* ============================================
   RECENT SALES DATATABLE
   ============================================ */

$(document).ready(function () {
    $("#recentSalesTable").DataTable({
        pageLength: 5,
        lengthChange: false,
        ordering: true,
        language: {
            search: "Search:"
        }
    });
});


/* ============================================
   SALES CHART (Last 12 Months)
   ============================================ */

document.addEventListener("DOMContentLoaded", function () {

    const ctx = document.getElementById("salesChart");

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: monthlyLabels,
            datasets: [{
                label: "Monthly Sales",
                data: monthlySales,
                backgroundColor: "#0d6efd88",
                borderColor: "#0d6efd",
                borderWidth: 2,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
});
