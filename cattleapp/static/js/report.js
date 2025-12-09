/* ============================================================
   REPORTS & ANALYTICS SCRIPT
   ============================================================ */

let salesChart, profitChart, topChart;


$(document).ready(function () {

    /* DataTable Export */
    $("#inventoryTable").DataTable({
        dom: "Bfrtip",
        buttons: ["excel", "csv", "pdf", "print"]
    });

    loadSalesSummary();
    loadProfit();
    loadTopSelling();

    $("#filterSalesBtn").on("click", function () {
        loadSalesSummary();
    });

});



/* ============================
   SALES SUMMARY CHART
   ============================ */
function loadSalesSummary() {
    let from = $("#fromDate").val();
    let to = $("#toDate").val();

    $.post(salesSummaryURL, { from, to }, function (res) {

        if (salesChart) salesChart.destroy();

        salesChart = new Chart(document.getElementById("salesSummaryChart"), {
            type: "bar",
            data: {
                labels: res.labels,
                datasets: [{
                    label: "Sales Amount",
                    data: res.data,
                    backgroundColor: "#007bff"
                }]
            }
        });

    });
}



/* ============================
   PROFIT ANALYSIS CHART
   ============================ */
function loadProfit() {

    $.get(profitSummaryURL, function (res) {

        if (profitChart) profitChart.destroy();

        profitChart = new Chart(document.getElementById("profitChart"), {
            type: "line",
            data: {
                labels: res.labels,
                datasets: [{
                    label: "Profit",
                    data: res.data,
                    borderColor: "#28a745",
                    backgroundColor: "rgba(40,167,69,0.1)",
                    fill: true
                }]
            }
        });

    });
}



/* ============================
   TOP SELLING MEDICINES CHART
   ============================ */
function loadTopSelling() {

    $.get(topSellingURL, function (res) {

        if (topChart) topChart.destroy();

        topChart = new Chart(document.getElementById("topSellingChart"), {
            type: "pie",
            data: {
                labels: res.labels,
                datasets: [{
                    label: "Units Sold",
                    data: res.data,
                    backgroundColor: [
                        "#ff6384",
                        "#36a2eb",
                        "#ffcd56",
                        "#4bc0c0",
                        "#9966ff"
                    ]
                }]
            }
        });

    });
}
