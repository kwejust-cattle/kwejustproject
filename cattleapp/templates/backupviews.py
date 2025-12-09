#### A BLOCK OF CODES FOR ADD,EDIT,DELETE MEDICINES ####
@login_required(login_url='login_view')
def medicine_view(request):
    # Just render the template; DataTables will handle AJAX loading
    return render(request, 'medicine.html')

@login_required
def medicine_data(request):
    # DataTables required parameters
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))

    search_value = request.GET.get("search[value]", "")
    # ORDER BY TODAY FIRST (newest entries first)
    queryset = Medicine.objects.all().order_by("-created_at")

    #WITHOUT DATE ORDER
    #queryset = Medicine.objects.all()

    # Searching
    if search_value:
        queryset = queryset.filter(
            Q(name__icontains=search_value) |
            Q(price__icontains=search_value)
        )

    total_records = Medicine.objects.count()
    filtered_records = queryset.count()

    # --- IMPORTANT FIX ---
    # When "Show All" is selected, DataTables sends length = -1
    if length == -1:
        medicines = queryset       # return ALL results
    else:
        medicines = queryset[start:start + length]   # normal pagination
    # ----------------------

    # Convert to list
    data = list(medicines.values("id", "name", "price","created_at"))

    return JsonResponse({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": data
    })


@login_required(login_url='login_view')
@csrf_exempt
def medicine_add(request):
    """Save medicine via AJAX"""
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")

        if not name or not price:
            return JsonResponse({"status": "error", "message": "Missing fields"})

        Medicine.objects.create(name=name, price=price)

        return JsonResponse({"status": "success", "message": "Medicine added successfully!"})

    return JsonResponse({"status": "error", "message": "Invalid request"})

@login_required
@csrf_exempt
def medicine_update(request, id):
    med = Medicine.objects.get(id=id)

    med.name = request.POST.get("name")
    med.price = request.POST.get("price")
    med.save()

    return JsonResponse({"status": "success", "message": "Updated successfully"})


@login_required
@csrf_exempt
def medicine_delete(request, id):
    Medicine.objects.get(id=id).delete()

    return JsonResponse({"status": "success"})

#### A BLOCK OF CODES FOR ADD,EDIT,DELETE MEDICINES ####


<!--<script>
$(document).ready(function () {

    const csrftoken = "{{ csrf_token }}";

    // Initialize DataTable
    var table = $("#medicineTable").DataTable({
    processing: true,
    serverSide: true,
    pageLength: 10,   // default shown rows
    lengthMenu: [
        [5, 10, 15, 20, 25, 50, 100, -1],
        [5, 10, 15, 20, 25, 50, 100, "All"]
    ],
    dom: 'lBfrtip',   // <-- ADDED FOR BUTTONS
    buttons: [
        {
            extend: 'excelHtml5',
            text: 'Export Excel',
            className: 'btn btn-success',
            exportOptions: {
                 columns: ':not(:last-child)'
            }
        },
        {
            extend: 'pdfHtml5',
            text: 'Export PDF',
            className: 'btn btn-danger',
            orientation: 'portrait',
            pageSize: 'A4',
            exportOptions: {
                 columns: ':not(:last-child)'
            }
        },
        {
            extend: 'print',
            text: 'Print Labels',
            className: 'btn btn-primary',
            exportOptions: {
                 columns: ':not(:last-child)'
            },
            customize: function (win) {
                // PRINT-FRIENDLY LABEL FORMAT
                $(win.document.body).css('font-size', '14px');
                $(win.document.body).prepend('<h3 class="text-center">Medicine Labels</h3>');
            }
        }
    ],
    scrollY: "400px",       // <-- makes the table body scrollable
    scrollCollapse: true,   // <-- allows table to shrink if fewer rows
    paging: true,
    ajax: {
        url: "{% url 'medicine_data' %}",
    type: "GET"
    },

    columns: [
        {
            data: null,
            render: function (data, type, row, meta) {
                return meta.row + meta.settings._iDisplayStart + 1;
            }
        },
        { data: "name" },
        { data: "price" },
        // ADD THIS (optional)
        {
           data: "created_at",
           render: function (data) {
              // return new Date(data).toLocaleDateString(); only returns m/d/y
              if (!data) return "";
              let d = new Date(data);
              let day = String(d.getDate()).padStart(2, '0');
              let month = String(d.getMonth() + 1).padStart(2, '0');
              let year = d.getFullYear();
              return `${day}/${month}/${year}`;
           }
        },
        {
            data: "id",
            render: function (id, type, row) {
                return `
                    <button class="btn btn-warning btn-sm edit-btn"
                            data-id="${id}"
                            data-name="${row.name}"
                            data-price="${row.price}">
                        Edit
                    </button>

                    <button class="btn btn-danger btn-sm delete-btn"
                            data-id="${id}">
                        Delete
                    </button>
                `;
            }
        }
    ]
});


    // ADD MEDICINE
    $("#addMedicineForm").submit(function (e) {
        e.preventDefault();
        
        const name = $("#name").val().trim();
        const price = $("#price").val().trim();

    // Ensure name contains at least one letter
       if (!/[a-zA-Z]/.test(name)) {
            Swal.fire("Error", "Medicine name must contain at least one letter!", "error");
            return;  // stop submission
        }
    // Validation: price must be a number > 0
        if (!price || isNaN(price) || Number(price) <= 0) {
            Swal.fire("Error", "Please enter a valid price!", "error");
            return;
        }

    // If validations pass, send AJAX
        $.ajax({
            url: "{% url 'medicine_add' %}",
            method: "POST",
            data: {
                name: $("#name").val(),
                price: $("#price").val(),
                csrfmiddlewaretoken: csrftoken
            },
            success: function (response) {
                if (response.status === "success") {
                    Swal.fire("Added!", response.message, "success");
                    $("#addModal").modal("hide");
                    $("#addMedicineForm")[0].reset();
                    table.ajax.reload();
                } else {
                    Swal.fire("Error", response.message, "error");
                }
            }
        });
    });


    // OPEN EDIT MODAL
    $("#medicineTable").on("click", ".edit-btn", function () {
        $("#edit_id").val($(this).data("id"));
        $("#edit_name").val($(this).data("name"));
        $("#edit_price").val($(this).data("price"));
        $("#editModal").modal("show");
    });

    // UPDATE MEDICINE
    $("#editMedicineForm").submit(function (e) {
        e.preventDefault();
        
        const name = $("#edit_name").val().trim();
        const price = $("#edit_price").val().trim();

        if (!/[a-zA-Z]/.test(name)) {
            Swal.fire("Error", "Medicine name must contain at least one letter!", "error");
            return;
        }

        if (!price || isNaN(price) || Number(price) <= 0) {
            Swal.fire("Error", "Please enter a valid price!", "error");
            return;
        }
        $.ajax({
            url: "/medicine/update/" + $("#edit_id").val() + "/",
            method: "POST",
            data: {
                name: $("#edit_name").val(),
                price: $("#edit_price").val(),
                csrfmiddlewaretoken: csrftoken
            },
            success: function (response) {
                Swal.fire("Updated!", response.message, "success");

                $("#editModal").modal("hide");
                table.ajax.reload();
            }
        });
    });

    // DELETE MEDICINE
    $("#medicineTable").on("click", ".delete-btn", function () {
        let id = $(this).data("id");

        Swal.fire({
            title: "Are you sure?",
            icon: "warning",
            showCancelButton: true,
            confirmButtonText: "Delete"
        }).then((res) => {
            if (res.isConfirmed) {
                $.ajax({
                    url: "/medicine/delete/" + id + "/",
                    method: "POST",
                    data: {
                        csrfmiddlewaretoken: csrftoken
                    },
                    success: function () {
                        Swal.fire("Deleted!", "Medicine removed", "success");
                        table.ajax.reload();
                    }
                });
            }
        });
    });

});
</script>-->
