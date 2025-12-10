/* ============================================
   MEDICINE PAGE SCRIPT
   ============================================ */

$(document).ready(function() {

    /* ----------------------------------------
       DATATABLE
       ---------------------------------------- */
    $("#medicineTable").DataTable({
        pageLength: 10,
        ordering: true,
        language: {
            search: "Search:"
        }
    });


    /* ----------------------------------------
       ADD MEDICINE
       ---------------------------------------- */
    $("#saveMedicineBtn").on("click", function () {

        let medData = {
            name: $("#add_name").val(),
            category: $("#add_category").val(),
            description: $("#add_desc").val(),
            reorder_level: $("#add_reorder").val(),
        };

        $.post(addMedicineURL, medData, function (response) {
            showToast("Medicine added successfully");
            location.reload();
        });

    });


    /* ----------------------------------------
       OPEN EDIT MODAL
       ---------------------------------------- */
    $(".editBtn").on("click", function () {

        let tr = $(this).closest("tr");
        let id = tr.data("id");

        $("#edit_id").val(id);
        $("#edit_name").val(tr.find("td:eq(0)").text());
        $("#edit_category").val(tr.find("td:eq(1)").text());
        $("#edit_desc").val(tr.find("td:eq(2)").text());
        $("#edit_reorder").val(tr.find("td:eq(3)").text());

        new bootstrap.Modal("#editMedicineModal").show();
    });


    /* ----------------------------------------
       UPDATE MEDICINE
       ---------------------------------------- */
    $("#updateMedicineBtn").on("click", function () {

        let medData = {
            id: $("#edit_id").val(),
            name: $("#edit_name").val(),
            category: $("#edit_category").val(),
            description: $("#edit_desc").val(),
            reorder_level: $("#edit_reorder").val(),
        };

        $.post(updateMedicineURL, medData, function (response) {
            showToast("Medicine updated");
            location.reload();
        });

    });


    /* ----------------------------------------
       DELETE MEDICINE
       ---------------------------------------- */
    $(".deleteBtn").on("click", function () {

        let tr = $(this).closest("tr");
        let id = tr.data("id");

        if (!confirm("Delete this medicine?")) return;

        $.post(deleteMedicineURL, { id }, function () {
            showToast("Medicine deleted");
            tr.remove();
        });

    });


});
