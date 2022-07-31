$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_product_form_data(res){
        $("#customer_id").val(res.shopcart_id);
        $("#product_id").val(res.id);
        $("#product_name").val(res.name);
        $("#product_quantity").val(res.quantity);
        $("#product_price").val(res.price);
    }
    function update_shopcart_form_data(res){
        $("#customer_id").val(res.id);
    }
    /// Clears all form fields
    function clear_form_data() {
        $("#product_id").val("");
        $("#product_name").val("");
        $("#product_quantity").val("");
        $("#product_price").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create A Shop cart with product
    // ****************************************

    $("#create-btn").click(function () {

        let customer_id = $("#customer_id").val();

        let data = {
            "id": customer_id,
            "products":[]
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: `/shopcarts/${customer_id}`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_shopcart_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Retrieve a Shop Cart
    // ****************************************

    $("#retrieve-btn").click(function () {

        let customer_id = $("#customer_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/shopcarts/${customer_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_shopcart_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });
    // ****************************************
    // List Products of a Shop Cart
    // ****************************************
 
    $("#list-btn").click(function () {

        let customer_id = $("#customer_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/shopcarts/${customer_id}/products`,
            contentType: "application/json",
            data: ''
        })
         
        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Quantity</th>'
            table += '<th class="col-md-2">Price</th>'
            table += '</tr></thead><tbody>'
            let firstProduct = "";
            for(let i = 0; i < res.length; i++) {
                let product = res[i];
                table +=  `<tr id="row_${i}"><td>${product.id}</td><td>${product.name}</td><td>${product.quantity}</td><td>${product.price}</td></tr>`;
                if (i == 0) {
                    firstProduct = product;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

                    // copy the first result to the form
            if (firstProduct != "") {
                update_product_form_data(firstProduct)
            }
        
                flash_message("Success")
            });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });
    // ****************************************
    // Clear a Shop Cart
    // ****************************************

    $("#clear-btn").click(function () {

        let customer_id = $("#customer_id").val();
        let data = {
            "id": customer_id,
            "products":[]
        };
        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/shopcarts/${customer_id}/clear`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_shopcart_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Shop Cart
    // ****************************************

    $("#delete-btn").click(function () {

        let customer_id = $("#customer_id").val();
        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/shopcarts/${customer_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Shop Cart has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-form-btn").click(function () {
        $("#customer_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Add a Product
    // ****************************************
 
    $("#add-btn").click(function () {

        let customer_id = $("#customer_id").val();
        let price = $("#product_price").val();
        let quantity = $("#product_quantity").val();
        let name = $("#product_name").val();

        $("#flash_message").empty();

        let data = {
            "shopcart_id": customer_id,
            "name":name,
            "price":price,
            "quantity":quantity,
        };
        let ajax = $.ajax({
            type: "POST",
            url: `/shopcarts/${customer_id}/products`,
            contentType: "application/json",
            data: JSON.stringify(data),
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_product_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // delete a Product
    // ****************************************
 
    $("#delete-product-btn").click(function () {

        let customer_id = $("#customer_id").val();
        let product_id = $("#product_id").val();


        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/shopcarts/${customer_id}/products/${product_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Product has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });

    });

    // ****************************************
    // Update a Product
    // ****************************************
 
    $("#update-btn").click(function () {

        let customer_id = $("#customer_id").val();
        let product_id = $("#product_id").val();
        let price = $("#product_price").val();
        let quantity = $("#product_quantity").val();
        let name = $("#product_name").val();

        $("#flash_message").empty();

        let data = {
            "shopcart_id": customer_id,
            "name":name,
            "price":price,
            "quantity":quantity,
            "id":product_id
        };

        let ajax = $.ajax({
            type: "PUT",
            url: `/shopcarts/${customer_id}/products/${product_id}`,
            contentType: "application/json",
            data: JSON.stringify(data),
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_product_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Update a Shop Cart
    // ****************************************
 
    $("#update-shopcart-btn").click(function () {

        let id = $("#customer_id").val();
        
        let price = $("#product_price").val();
        let quantity = $("#product_quantity").val();
        let name = $("#product_name").val();

        $("#flash_message").empty();


        let data2 = {
            "shopcart_id": id,
            "name":name,
            "price":price,
            "quantity":quantity,
        };

        let data1 = {
            "id": id,
            "products": [data2],
        }

        let ajax = $.ajax({
            type: "PUT",
            url: `/shopcarts/${id}`,
            contentType: "application/json",
            data: JSON.stringify(data1),
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_shopcart_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Search for a Shop Cart based on a product
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#product_name").val();

        if (!name) {
            flash_message("Name needed")
            return;
        }
        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/shopcarts/products/${name}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '</tr></thead><tbody>'
            let firstProduct = "";
            for(let i = 0; i < res.length; i++) {
                let cart = res[i];
                table +=  `<tr id="row_${i}"><td>${cart.customer_id}</td><td>${name}</td></tr>`;
                if (i == 0) {
                    firstProduct = cart;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstProduct != "") {
                update_shopcart_form_data(firstProduct)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
// ****************************************
// List All Shop Cart
// ****************************************

$("#list-shopcart-btn").click(function () {

    $("#flash_message").empty();

    let ajax = $.ajax({
        type: "GET",
        url: `/shopcarts`,
        contentType: "application/json",
        data: ''
    })

    ajax.done(function(res){
        //alert(res.toSource())
        $("#search_results").empty();
        let table = '<table class="table table-striped" cellpadding="10">'
        table += '<thead><tr>'
        table += '<th class="col-md-2">ID</th>'
        table += '</tr></thead><tbody>'
        let firstCart = "";
        for(let i = 0; i < res.length; i++) {
            let cart = res[i];
            table +=  `<tr id="row_${i}"><td>${cart.id}</td></tr>`;
            if (i == 0) {
                firstCart = cart;
            }
        }
        table += '</tbody></table>';
        $("#search_results").append(table);

        // copy the first result to the form
        if (firstProduct != "") {
            update_shopcart_form_data(firstProduct)
        }

        flash_message("Success")
    });

    ajax.fail(function(res){
        flash_message(res.responseJSON.message)
    });

});


