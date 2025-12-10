/* =========================================================
   SALES PAGE SCRIPT
   ========================================================= */

let cart = [];

/* ------------------------------------
   LOAD BATCHES WHEN MEDICINE SELECTED
   ------------------------------------ */
$("#medicineSelect").on("change", function () {
    let medId = $(this).val();

    $("#batchSelect").html("<option>Loading...</option>");

    $.get(`${batchesURL}?medicine_id=${medId}`, function (data) {
        $("#batchSelect").html('<option value="">Select Batch</option>');
        data.forEach(b => {
            $("#batchSelect").append(`
                <option value="${b.id}"
                        data-price="${b.selling_price}"
                        data-qty="${b.quantity_remaining}">
                    Batch ${b.batch_number} (Exp: ${b.expiry_date})
                </option>
            `);
        });
    });
});


/* ------------------------------------
   WHEN BATCH IS SELECTED
   ------------------------------------ */
$("#batchSelect").on("change", function () {
    let selected = $(this).find("option:selected");

    $("#unitPrice").val(selected.data("price") || "");
    $("#availableQty").val(selected.data("qty") || "");
});


/* ------------------------------------
   ADD TO CART
   ------------------------------------ */
$("#addToCartBtn").on("click", function () {
    let medId = $("#medicineSelect").val();
    let medName = $("#medicineSelect option:selected").text();

    let batchId = $("#batchSelect").val();
    let batchText = $("#batchSelect option:selected").text();

    let price = parseFloat($("#unitPrice").val());
    let available = parseInt($("#availableQty").val());
    let qty = parseInt($("#saleQty").val());

    if (!medId || !batchId || !qty || qty <= 0) {
        showToast("Fill all fields", "error");
        return;
    }

    if (qty > available) {
        showToast("Quantity exceeds available stock", "error");
        return;
    }

    let total = qty * price;

    cart.push({
        medId,
        medName,
        batchId,
        batchText,
        qty,
        price,
        total
    });

    renderCart();
});


/* ------------------------------------
   RENDER CART TABLE
   ------------------------------------ */
function renderCart() {
    let html = "";
    let grand = 0;

    cart.forEach((c, index) => {
        grand += c.total;

        html += `
            <tr>
                <td>${c.medName}</td>
                <td>${c.batchText}</td>
                <td>${c.qty}</td>
                <td>${c.price}</td>
                <td>${c.total}</td>
                <td>
                    <button class="btn btn-sm btn-danger" onclick="removeItem(${index})">
                        <i class="bi bi-x"></i>
                    </button>
                </td>
            </tr>
        `;
    });

    $("#cartBody").html(html);
    $("#grandTotal").text(grand);
}


/* ------------------------------------
   REMOVE ITEM
   ------------------------------------ */
function removeItem(i) {
    cart.splice(i, 1);
    renderCart();
}


/* ------------------------------------
   CHECKOUT BUTTON
   ------------------------------------ */
$("#checkoutBtn").on("click", function () {
    if (cart.length === 0) {
        showToast("Cart is empty", "error");
        return;
    }

    $("#checkoutTotal").text($("#grandTotal").text());
    new bootstrap.Modal(document.getElementById("checkoutModal")).show();
});


/* ------------------------------------
   CONFIRM CHECKOUT
   ------------------------------------ */
$("#confirmCheckoutBtn").on("click", function () {
    let customer = $("#customerName").val();
    let paid = $("#paymentAmount").val();
    let total = parseFloat($("#grandTotal").text());

    if (paid < total) {
        showToast("Payment is less than total", "error");
        return;
    }

    $.ajax({
        url: saveSaleURL,
        method: "POST",
        data: {
            customer_name: customer,
            cart: JSON.stringify(cart),
            total_amount: total,
        },
        success: function (response) {
            showReceipt(customer, paid, total, paid - total);
            showToast("Sale completed");
            cart = [];
            renderCart();
            $("#checkoutModal").modal("hide");
        }
    });
});


/* ------------------------------------
   PRINT RECEIPT
   ------------------------------------ */
function showReceipt(customer, paid, total, change) {

    let date = new Date().toLocaleString();

    $("#receiptDate").text(date);
    $("#receiptCustomer").text(customer);
    $("#receiptPaid").text(paid);
    $("#receiptTotal").text(total);
    $("#receiptChange").text(change);

    let itemsHTML = "";
    cart.forEach(c => {
        itemsHTML += `
            <tr>
                <td>${c.medName} x${c.qty}</td>
                <td class="right">${c.total}</td>
            </tr>
        `;
    });

    $("#receiptItems").html(itemsHTML);

    /* PRINT LOGIC */
    let receiptContent = `
        <html>
            <head>
                <link rel="stylesheet" href="/static/css/receipt.css">
            </head>
            <body>
                ${document.getElementById("receiptPrintArea").innerHTML}
            </body>
        </html>
    `;

    let win = window.open("", "_blank", "width=300,height=600");
    win.document.write(receiptContent);
    win.document.close();
    win.focus();
    win.print();
    setTimeout(() => win.close(), 1000);
}
