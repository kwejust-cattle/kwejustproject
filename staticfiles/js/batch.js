$(document).ready(function () {

    /* DataTable */
    $("#batchTable").DataTable({
        pageLength: 10,
        ordering: true,
        language: { search: "Search:" }
    });


    /* ========== ADD BATCH ========== */
    $("#saveBatchBtn").on("click", function () {

        let data = {
            medicine: $("#add_medicine").val(),
            batch_number: $("#add_batchno").val(),
            quantity: $("#add_qty").val(),
            cost_price: $("#add_cost").val(),
            selling_price: $("#add_sell").val(),
            expiry_date: $("#add_expiry").val(),
        };

        $.post(addBatchURL, data, function () {
            showToast("Batch added successfully");
            location.reload();
        });

    });


    /* ========== POPULATE EDIT MODAL ========== */
    $(".editBtn").on("click", function () {

        let tr = $(this).closest("tr");
        let id = tr.data("id");

        $("#edit_id").val(id);
        $("#edit_medicine").val(tr.find("td:eq(0)").data("mid"));
        $("#edit_batchno").val(tr.find("td:eq(1)").text());
        $("#edit_qty").val(tr.find("td:eq(2)").text());
        $("#edit_cost").val(tr.find("td:eq(4)").text());
        $("#edit_sell").val(tr.find("td:eq(5)").text());
        $("#edit_expiry").val(tr.find("td:eq(6)").text());

        new bootstrap.Modal("#editBatchModal").show();
    });


    /* ========== UPDATE BATCH ========== */
    $("#updateBatchBtn").on("click", function () {

        let data = {
            id: $("#edit_id").val(),
            medicine: $("#edit_medicine").val(),
            batch_number: $("#edit_batchno").val(),
            quantity: $("#edit_qty").val(),
            cost_price: $("#edit_cost").val(),
            selling_price: $("#edit_sell").val(),
            expiry_date: $("#edit_expiry").val(),
        };

        $.post(updateBatchURL, data, function () {
            showToast("Batch updated");
            location.reload();
        });

    });


    /* ========== DELETE BATCH ========== */
    $(".deleteBtn").on("click", function () {

        if (!confirm("Delete this batch?")) return;

        let id = $(this).closest("tr").data("id");

        $.post(deleteBatchURL, { id }, function (response) {

            if (response.error === "HAS_SALES") {
                alert("This batch cannot be deleted because sales exist.");
            } 
            else {
                showToast("Batch deleted");
                location.reload();
            }

        });

    });

});
